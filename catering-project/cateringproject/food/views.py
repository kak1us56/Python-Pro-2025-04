import csv
import io
from datetime import date
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import permissions, routers, serializers, viewsets, filters
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django.db import transaction
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework

from users.models import Role, User

from .models import Dish, Order, OrderItem, OrderStatus, Restaurant
from .enums import DeliveryProvider

# Create your views here.
class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"

class RestaurantSerializer(serializers.ModelSerializer):
    dishes = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_dishes(self, obj):
        request = self.context.get('request')

        dishes = obj.dishes.all()

        search_query = request.query_params.get('search')
        if search_query:
            dishes = dishes.filter(name__icontains=search_query)

        paginator = LimitOffsetPagination()
        paginator.limit_param = 2

        page = paginator.paginate_queryset(dishes, request, view=self)

        return DishSerializer(page, many=True).data

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

class RestaurantFilters(rest_framework.FilterSet):
    class Meta:
        model = Restaurant
        fields = ['name']

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, 'role', None) == Role.ADMIN

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

            filtered_queryset = RestaurantFilters(request.GET, queryset=restaurants).qs

            serializer = RestaurantSerializer(filtered_queryset, many=True, context={"request": request})
            return Response(data=serializer.data)

# @api_view(["POST"])
# @permission_classes([IsAdmin])
def import_dishes(request):
    if not IsAdmin().has_permission(request, view=None):
        return Response({"detail": "You do not have permission to perform this action."}, status=403)

    if request.method != "POST":
        raise ValueError("Only POST requests are allowed.")

    csv_file = request.FILES.get("file")
    if csv_file is None:
        raise ValueError("CSV file not found.")

    decoded = csv_file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    total = 0

    for row in reader:
        restaurant_name = row["restaurant"]
        try:
            rest = Restaurant.objects.get(name__icontains=restaurant_name.lower())
        except Restaurant.DoesNotExist:
            print("Skipping restaurant " + restaurant_name)
        else:
            print(f"{restaurant_name} not found.")

        Dish.objects.create(name=row["name"], restaurant=rest, price=int(row["price"]))
        total += 1

    print(f"{total} restaurants uploaded to the database.")

    return redirect(request.META.get("HTTP_REFERER", "/"))


router = routers.DefaultRouter()
router.register(prefix="", viewset=FoodAPIViewSet, basename="food")