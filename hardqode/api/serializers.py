from rest_framework import serializers
from .models import Lesson, Views, User, Product


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['title', 'descr', 'link', 'duration', 'status', 'time']

    def get_status(self, obj):
        request = self.context.get('request')
        if not request:
            return 'Нет данных'
        data = request.data
        try:

            user = User.objects.get(id=data['user_id'])
            view = Views.objects.get(user=user, lesson=obj)
            duration_coefficient = view.duration.total_seconds() / obj.duration.total_seconds()
            if duration_coefficient > 0.8:
                return 'Просмотрено'
            else:
                return 'Не просмотрено'

        except Views.DoesNotExist:
            return 'Нет данных'

    def get_time(self, obj):
        request = self.context.get('request')
        if not request:
            return 'Нет данных'
        data = request.data
        try:
            user = User.objects.get(id=data['user_id'])
            view = Views.objects.get(user=user, lesson=obj)
            return view.date

        except Views.DoesNotExist:
            return 'Нет данных'


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'descr', 'owner', 'lessons']

    def get_owner(self, obj):
        return obj.owner.name


class ProductsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    percent_purchase = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'descr', 'owner', 'total_views', 'total_time', 'total_users', 'percent_purchase']


    def get_total_views(self, obj):
        total_views = 0

        for lesson in obj.lessons.all():
            total_views += lesson.views.count()

        return total_views

    def get_total_time(self, obj):
        total_time = 0

        for lesson in obj.lessons.all():
            for views in lesson.lesson_views.all():
                total_time += views.duration.total_seconds()

        return total_time

    def get_total_users(self, obj):
        return obj.access.count()


    def get_percent_purchase(self, obj):
        users = User.objects.all().count()
        purchase = obj.access.count()

        percent = round((purchase / users) * 100, 2)
        return f'{percent}%'

    def get_owner(self, obj):
        return obj.owner.name
