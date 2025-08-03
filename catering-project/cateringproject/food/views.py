from datetime import date
from django.shortcuts import render
from rest_framework import permissions, routers, serializers, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django.db import transaction

from users.models import Role, User

from .models import Dish, Order, OrderItem, OrderStatus, Restaurant
from .enums import DeliveryProvider

# Create your views here.
class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"

class RestaurantSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=20)

    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    items = OrderItemSerializer(many=True)
    eta = serializers.DateField()
    total = serializers.IntegerField(min_value=1, read_only=True)
    status = serializers.ChoiceField(OrderStatus.choices(), read_only=True)
    delivery_provider = serializers.CharField()

    class Meta:
        model = Order
        fields = "__all__"

    @property
    def calculated_total(self) -> int:
        total = 0

        for item in self.validated_data["items"]:
            dish: Dish = item["dish"]
            quantity: int = item["quantity"]
            total += dish.price * quantity

        return total

    def validate_eta(self, value: date):
        if (value - date.today()).days < 1:
            raise ValidationError("ETA must be min 1 day after today.")
        else:
            return value

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        assert type(request.user) == User
        user: User = request.user
        if user.role == Role.ADMIN:
            return True
        else:
            return False

class FoodAPIViewSet(viewsets.GenericViewSet):
    queryset = Restaurant.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'create_dish':
            return [IsAdmin()]
        return super().get_permissions()

    @action(methods=["post"], detail=False, url_path=r"orders")
    def create_order(self, request: Request) -> Response:
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assert type(request.user) is User

        with transaction.atomic():
            order = Order.objects.create(
                status=OrderStatus.NOT_STARTED,
                user=request.user,
                delivery_provider="uklon",
                eta=serializer.validated_data["eta"],
                total=serializer.calculated_total,
            )

            items = serializer.validated_data["items"]
            for dish_order in items:
                # raise ValueError("some error occured")
                instance = OrderItem.objects.create(
                    dish=dish_order["dish"],
                    quantity=dish_order["quantity"],
                    order=order,
                )
                print(f"New Dish Order Item is created: {instance.pk}")

        print(f"New Food Order is created: {order.pk}. ETA: {order.eta}")

        # TODO: Run scheduler

        return Response(OrderSerializer(order).data, status=201)

    # @action(methods=["get"], detail=False)
    # def dishes(self, request: Request) -> Response:
    #     restaurants = Restaurant.objects.all()
    #     serializer = RestaurantSerializer(restaurants, many=True)
    #     return Response(data=serializer.data)

    @action(methods=["post", "get"], detail=False, url_path=r"dishes")
    def dishes(self, request: Request) -> Response:
        if request.method == "POST":
            if not IsAdmin().has_permission(request, self):
                return Response({"detail": "You do not have permission to perform this action."}, status=403)

            serializer = DishSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(DishSerializer(serializer.instance).data, status=201)

        if request.method == "GET":
            restaurants = Restaurant.objects.all()
            serializer = RestaurantSerializer(restaurants, many=True)
            return Response(data=serializer.data)


router = routers.DefaultRouter()
router.register(prefix="", viewset=FoodAPIViewSet, basename="food")