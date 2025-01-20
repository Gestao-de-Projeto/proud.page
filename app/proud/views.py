import os

from django.http import JsonResponse
from .models import *
from .utils import *
from .consts import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail

@csrf_exempt
def index(request):
    dados = {'mensagem': 'Olá'}
    return JsonResponse(dados, status=OK)


@csrf_exempt
def products(request):
    if request.method == 'GET':
        # obter todos os produtos
        products = Product.objects.all()
        product_list = list(products.values())
        return JsonResponse({'products': product_list}, status=OK)
    elif request.method == 'POST':
        # criar produto
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(invalid_json_message(), status=BAD_REQUEST)

        validation_error = np_data_validation(data)

        if validation_error:
            return JsonResponse(validation_error, status=BAD_REQUEST)

        try:
            product = Product.objects.create(
                price=data['price'],
                name=data['name'],
                type=data['type'],
                stock=data['stock'],
                description=data['description'],
                exclusivity=data['exclusivity'],
                size=data['size']
            )
        except Exception as e:
            return JsonResponse(internal_server_error_message(str(e)), status=INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'Product successfully created', 'product_id': product.id}, status=CREATED)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)


@csrf_exempt
def product(request, product_id):
    if request.method == 'GET':
        product = get_product_by_id(product_id)
        if product is None:
            return JsonResponse(product_not_found_message(product_id), status=NOT_FOUND)
        else:
            product = Product.objects.get(id=product_id)
            product_details = {
                'id': product.id,
                'price': product.price,
                'name': product.name,
                'type': product.type,
                'stock': product.stock,
                'description': product.description,
                'exclusivity': product.exclusivity,
                'size': product.size
            }
            return JsonResponse({'product': product_details}, status=OK)
    elif request.method == 'PUT':
        product = get_product_by_id(product_id)
        if product is None:
            return JsonResponse(product_not_found_message(product_id), status=NOT_FOUND)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(invalid_json_message(), status=BAD_REQUEST)

        validation_error = ep_data_validation(data, product)

        if validation_error:
            return JsonResponse(validation_error, status=BAD_REQUEST)

        try:
            Product.objects.filter(id=product_id).update(
                price=data['price'],
                name=data['name'],
                type=data['type'],
                stock=data['stock'],
                description=data['description'],
                exclusivity=data['exclusivity'],
                size=data['size']
            )
        except Exception as e:
            return JsonResponse(internal_server_error_message(str(e)), status=INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'Product successfully updated'}, status=OK)
    elif request.method == 'DELETE':
        product = get_product_by_id(product_id)
        if product is None:
            return JsonResponse(product_not_found_message(product_id), status=NOT_FOUND)

        try:
            product.delete()
        except Exception as e:
            return JsonResponse(internal_server_error_message(str(e)), status=INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'Product successfully deleted'}, status=OK)
    else:
        return JsonResponse(invalid_http_method(), status=METHOD_NOT_ALLOWED)
    
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"error": "Email and password are required"}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid email or password"}, status=400)

            if check_password(password, user.password):
                return JsonResponse({"message": "Login successful", "user_uuid": str(user.uuid)}, status=200)
            else:
                return JsonResponse({"error": "Invalid email or password"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def create_newsletter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        print(email)
        if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"error": "Invalid email format"}, status=400)

        if Newsletter.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered in the newsletter list"}, status=400)

        try:
            Newsletter.objects.create(email=email)
            return JsonResponse({"message": "Email successfully registered"}, status=200)
        except:
            return JsonResponse({"error": "An error has occurred"}, status=500)


@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject = data.get('subject')
        message = data.get('message')
        emails_to = data.get('emails_to') #TODO: TEM DE SER UMA LISTA vinda do front-end

        if not subject or not message:
            return JsonResponse({"error": "Subject, message and email are required"}, status=400)

        for email in emails_to:
            if validate_email(email) == False:
                return JsonResponse({"error": "Invalid email format"}, status=400)
        try:
            send_mail(
                subject,
                message,
                os.getenv('EMAIL_HOST_USER'),
                emails_to,
                fail_silently=False,
            )
            return JsonResponse({"message": "Email sent successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)