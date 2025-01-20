from django.http import JsonResponse
from .models import *
from .utils import *
from .consts import *
import json
from django.views.decorators.csrf import csrf_exempt


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
