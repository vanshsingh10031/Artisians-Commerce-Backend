from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Users
from .models import Categories
from .serializers import UsersSerializer
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Products,Orders,Cart, Cartitems,Orderitems
import json
from .serializers import CartSerializer
from django.http import JsonResponse
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Sum, Count
import os

from django.conf import settings
class UsersList(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    def get(self, request, userid):
        user = get_object_or_404(Users, userid=userid)
        serializer = UsersSerializer(user)
        return Response(serializer.data)
    
class UserLogin(APIView):
    def get(self, request):
        phone = request.query_params.get('phone')
        password = request.query_params.get('password')
        
        if not phone or not password:
            return Response({'error': 'Phone and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Users.objects.get(phone=phone)
        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # For now, assuming password is stored as plain text (which is not recommended!)
        if user.password == password:
            return Response({'message': 'Login successful', 'user_id': user.userid, 'role': user.role })
        else:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        



class UserRegistration(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not phone or not email or not password:
            return Response({'error': 'Phone, email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if phone or email already exists
        if Users.objects.filter(phone=phone).exists():
            return Response({'error': 'Phone number already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Users.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the user (save password as-is)
        user = Users.objects.create(
            phone=phone,
            email=email,
            password=password
        )
        
        return Response({'message': 'User registered successfully', 'user_id': user.userid}, status=status.HTTP_201_CREATED)
    


    # Get all products for a given user
@csrf_exempt
def get_products_by_user(request, userid):
    if request.method == 'GET':
        products = Products.objects.filter(userid=userid)
        product_list = []
        for product in products:
            product_list.append({
                'productid': product.productid,
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'stock': product.stock,
                'categoryid': product.categoryid.categoryid if product.categoryid else None,
                'createdat': product.createdat,
                'updatedat': product.updatedat,
                 'imagepath': product.imagepath,
                'tags': product.tags.split(',') if product.tags else []
            })
        return JsonResponse({'products': product_list})
    else:
        return JsonResponse({'error': 'Only GET method allowed'}, status=405)


# Get product details by userid and productid
@csrf_exempt
def get_product_detail(request, userid, productid):
    if request.method == 'GET':
        try:
            product = Products.objects.get(userid=userid, productid=productid)
            product_data = {
                'productid': product.productid,
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'stock': product.stock,
                'categoryid': product.categoryid.categoryid if product.categoryid else None,
                'createdat': product.createdat,
                'updatedat': product.updatedat,
            }
            return JsonResponse({'product': product_data})
        except Products.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only GET method allowed'}, status=405)
    

@csrf_exempt
def create_product(request, userid):
    if request.method == 'POST':
        try:
            user = Users.objects.get(userid=userid)
            
            # POST data
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category_name = request.POST.get('category')
            category_description = request.POST.get('category_description', '')
            tags = request.POST.get('tags', '')  # ✅ Comma-separated tags string

            # Handle category
            category = None
            if category_name:
                category, created = Categories.objects.get_or_create(
                    name=category_name,
                    defaults={'description': category_description}
                )

            # Handle image upload
            uploaded_file = request.FILES.get('image')
            image_path = None
            if uploaded_file:
                media_dir = os.path.join(settings.BASE_DIR, 'media', 'product_images')
                os.makedirs(media_dir, exist_ok=True)
                file_path = os.path.join(media_dir, uploaded_file.name)
                
                with open(file_path, 'wb+') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
                
                # Store relative path for DB
                image_path = f'product_images/{uploaded_file.name}'

            # Create product
            product = Products.objects.create(
                userid=user,
                name=name,
                description=description,
                price=price,
                stock=int(stock) if stock else 0,
                createdat=timezone.now(),
                categoryid=category,
                imagepath=image_path,
                updatedat=timezone.now(),
                tags=tags.strip() if tags else None   # ✅ now saving tags
            )

            return JsonResponse({
                'message': 'Product created successfully',
                'productid': product.productid,
                'image_url': f'/media/{image_path}' if image_path else None
            }, status=201)

        except Users.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


@csrf_exempt
def update_product(request, userid, productid):
    if request.method == "PUT" or request.method == "POST":  # support both
        try:
            user = Users.objects.get(userid=userid)
            product = Products.objects.get(productid=productid, userid=user)

            # Parse form data
            name = request.POST.get("name", product.name)
            description = request.POST.get("description", product.description)
            price = request.POST.get("price", product.price)
            stock = request.POST.get("stock", product.stock)
            category_name = request.POST.get("category")

            # Handle category update if provided
            if category_name:
                category, _ = Categories.objects.get_or_create(
                    name=category_name,
                    defaults={"description": request.POST.get("category_description", "")}
                )
                product.categoryid = category

            # Update fields
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.updatedat = timezone.now()
            # Handle new image upload
            uploaded_file = request.FILES.get("image")
            if uploaded_file:
                media_dir = os.path.join(settings.MEDIA_ROOT, "product_images")
                os.makedirs(media_dir, exist_ok=True)
                file_path = os.path.join(media_dir, uploaded_file.name)

                with open(file_path, "wb+") as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)

                product.imagepath = f"product_images/{uploaded_file.name}"

            product.save()

            return JsonResponse({
                "message": "Product updated successfully",
                "productid": product.productid,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "category": product.categoryid.name if product.categoryid else None,
                "image_url": f"{settings.MEDIA_URL}{product.imagepath}" if product.imagepath else None,
            }, status=200)

        except Users.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Products.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only PUT/POST method allowed"}, status=405)

@csrf_exempt
def delete_product(request, userid, productid):
    if request.method == "DELETE":
        try:
            # ✅ Ensure user exists
            user = Users.objects.get(userid=userid)

            # ✅ Ensure product belongs to that user
            product = Products.objects.get(productid=productid, userid=user)

            # ✅ Optionally delete the image file from storage
            if product.imagepath:
                image_file = os.path.join(settings.MEDIA_ROOT, product.imagepath)
                if os.path.exists(image_file):
                    os.remove(image_file)

            # ✅ Delete product
            product.delete()

            return JsonResponse({"message": "Product deleted successfully"}, status=200)

        except Users.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Products.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only DELETE method allowed"}, status=405)

@csrf_exempt
def register_artisan(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)

        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')
        shop_name = data.get('shopName')
        shop_address = data.get('shopAddress')

        if not all([name, phone, email, password, shop_name, shop_address]):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Check if phone/email already exists
        if Users.objects.filter(phone=phone).exists():
            return JsonResponse({'error': 'Phone number already registered'}, status=400)
        if Users.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)

        # Optional: Handle profile image / documents
        # uploaded_file = request.FILES.get('profile_image')
        # file_path = None
        # if uploaded_file:
        #     media_dir = os.path.join(settings.BASE_DIR, 'media', 'profile_images')
        #     os.makedirs(media_dir, exist_ok=True)
        #     file_path = os.path.join(media_dir, uploaded_file.name)
        #     with open(file_path, 'wb+') as f:
        #         for chunk in uploaded_file.chunks():
        #             f.write(chunk)
        #     file_path = f'profile_images/{uploaded_file.name}'

        # Create new artisan user
        user = Users.objects.create(
            fullname=name,
            phone=phone,
            email=email,
            password=password,  # TODO: hash password using Django's set_password()
            createdat=timezone.now(),
            updatedat=timezone.now(),
            # ShopName=shop_name,
            # Address=shop_address,
            role='artisan'
            # profile_image=file_path
        )

        return JsonResponse({
            'message': 'Artisan registered successfully',
            'user_id': user.userid,
            'name': user.fullname
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# -------------------- DASHBOARD API --------------------
def dashboard_data(request, userid):
    try:
        # Orders for this user
        orders = Orders.objects.filter(userid=userid)

        total_orders = orders.count()
        total_sales = orders.aggregate(total=Sum("totalamount"))["total"] or 0

        # Group by status
        order_status = list(
            orders.values("status").annotate(count=Count("status"))
        )

        # Products for this user
        products = Products.objects.filter(userid=userid)
        total_products = products.count()
        product_list = list(products.values("productid", "name", "price", "stock"))

        data = {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_sales": float(total_sales),
            "order_status": order_status,
            "products": product_list,
        }

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

def get_all_products(request):
    try:
        products = Products.objects.select_related("userid").all()
        data = []
        for p in products:
            data.append({
                "productid": p.productid,
                "name": p.name,
                "price": float(p.price),
                "description": p.description,
                "imagepath": p.imagepath,
                "tags": p.tags.split(",") if p.tags else [],
                "vendor": {
                    "shop_name": p.userid.fullname,
                    "shop_address": getattr(p.userid, "address", "N/A"),
                    "logo": getattr(p.userid, "profilepic", None)
                }
            })
        return JsonResponse({"products": data}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(["POST"])
def add_to_cart(request):
    """
    Add product to cart for a user
    Payload: { "user_id": 1, "product_id": 10, "quantity": 2 }
    """
    user_id = request.data.get("user_id")
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    if not user_id or not product_id:
        return Response({"error": "user_id and product_id required"}, status=status.HTTP_400_BAD_REQUEST)

    # Get or create cart (only userid + createdat stored here)
    cart, created = Cart.objects.get_or_create(
        userid_id=user_id,
        defaults={"createdat": timezone.now()}
    )

    # Add product to CartItems (all details stored here)
    item, item_created = Cartitems.objects.get_or_create(
        cartid=cart,
        productid_id=product_id,
        defaults={"quantity": quantity}
    )

    if not item_created:
        # If already exists, just update quantity
        item.quantity += quantity
        item.save()

    return Response(
        {"message": "Product added to cart", "cart_id": cart.cartid},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def view_cart(request, user_id):
    """
    View cart with all items
    """
    try:
        cart = Cart.objects.get(userid_id=user_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def remove_from_cart(request):
    """
    Remove a cart item
    Payload: { "cartitem_id": 5 }
    """
    cartitem_id = request.data.get("cartitem_id")
    try:
        item = Cartitems.objects.get(cartitemid=cartitem_id)
        item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
    except Cartitems.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    

class PlaceOrder(APIView):
   def post(self, request, userid):
        """
        Creates a new order for a user from their cart.
        Saves data in Orders and OrderItems tables.
        """
        try:
            user = get_object_or_404(Users, userid=userid)
            
            # Fetch cart & items
            cart = get_object_or_404(Cart, userid=user)
            cart_items = Cartitems.objects.filter(cartid=cart)

            if not cart_items.exists():
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total
            total_amount = sum(item.productid.price * item.quantity for item in cart_items)

            with transaction.atomic():  # atomic = rollback if anything fails
                # Create Order
                order = Orders.objects.create(
                    userid=user,
                    orderdate=timezone.now(),
                    status="Pending",
                    totalamount=total_amount
                )

                # Create OrderItems
                for item in cart_items:
                    Orderitems.objects.create(
                        orderid=order,
                        productid=item.productid,
                        quantity=item.quantity,
                        price=item.productid.price
                    )

                # Clear cart after placing order
                cart_items.delete()

            return Response(
                {"message": "Order placed successfully", "order_id": order.orderid},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)