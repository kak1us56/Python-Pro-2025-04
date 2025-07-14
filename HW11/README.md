
1. figure out the idea
2. setup the project
3. for iteration in iterations:
    - implement the feature
    - test feature


---


1. BLOG (easy)
    - Django official documentation
    - Django Girls
    - database, cache
2. SOCIAL NETWORK (medium)
    - multiple user roles (admin, user)
    - relations between users
    - like, repost, ...
    - database, cache
3. TECHNICAL SUPPORT (medium)
    - kanban board for managing issues from users
    - multiple user roles (admin, manager, customer)
    - different types of permissions
    - background worker for archiving ISSUES
    - database, cache, python
4. CATERING (hard)
    - event driven system
    - a core engine that will process the queue with tasks in a background
    - time-sensitive
    - multiple user roles (admin, driver, restaurant, customer)
    - aggregate multiple integrations of external APIs
    - different types of permissions
    - database, cache, python



---

- REST API (or websockets, GraphQL)
    - cache
    - layered system
    - unified interface
    - client-server
    - stateless
    - code on-demand
    - HTTP interface
        - HTTP GET /orders    -> [{}, {}, {}]
        - HTTP POST /orders
        - HTTP PUT /orders/ID
        - HTTP PATCH /orders/ID
        - HTTP DELETE /orders/ID
        - HTTP GET /orders/ID
    - Other
        - pagination
        - resource naming
        - filtering, ordering
        - security
            - CORS
            - AUTH
- CORE
- Menu
    - restaurants integrations
        - PRODUCTS = list of all products with availability status
- WHO ARE THE USERS?
    - ROLES: Customer, Manager, Admin
- Authorization
    - registration for Customer
    - registration for Driver
    - Admin creates Manager
    - Admin is created manually
- Orders
    - Can driver have multiple orders?
        NO
    - Structure
        - type: for-customer, for-facility
    - Minimal order?
        - NO. forbid empty orders
    - Product is not available for delivery
        - SOLUTION 1: cancel order, refund
        - SOLUTION 2: edit order (specify another product)
            - POSTPONE
            - Silpo has a kitchen (with products)
- Payment System
    - V2
- Scalability
    - can we add more rests?
        - YES
    - can we add more logistic integrations?
        - YES



