from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Product, Lesson
from .serializers import *


@api_view(['POST'])
def get_full_user_products(request):
    user_id = request.data.get('user_id')

    if not user_id:
        return Response({"result": False, "error": "ID пользователя не найдено"})

    try:
        user = User.objects.get(id=user_id)
        products = user.products_access.all()
        serialized_product = ProductSerializer(products, many=True, context={'request': request})

        return Response({"result": True, "products": serialized_product.data})

    except User.DoesNotExist:
        return Response({"result": False, 'error': 'Такого пользователя не существует'})

@api_view(['POST'])
def get_user_lesson_by_product(request):
    user_id = request.data.get('user_id')
    product_id = request.data.get('product_id')

    if not user_id or not product_id:
        return Response({"result": False, "error": "ID пользователя или продукта не найдено"})

    try:
        user = User.objects.get(id=user_id)
        products = Product.objects.filter(id=product_id, access=user)
        lessons = Lesson.objects.filter(products__in=products)

        if not products or not lessons:
            return Response({"result": False, 'error': 'Такого продукта не существует или у пользователя нет доступа к нему'})

        serialized_lessons = LessonSerializer(lessons, many=True, context={'request': request})

        return Response({"result": True, "lessons": serialized_lessons.data})

    except User.DoesNotExist:
        return Response({"result": False, 'error': 'Такого пользователя не существует'})


@api_view(['GET'])
def get_all_products(requests):
    products = Product.objects.all()

    if not products:
        return Response(
            {"result": False, 'error': 'Нет ни одного продукта'})

    serialized_products = ProductsSerializer(products, many=True)
    return Response({"result": True, "products": serialized_products.data})


