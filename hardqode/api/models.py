from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)


class Product(models.Model):
    title = models.CharField(max_length=50, blank=False)
    descr = models.TextField(blank=False)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owned_products')
    access = models.ManyToManyField('User', through='Access', related_name='products_access')


class Lesson(models.Model):
    title = models.CharField(max_length=50, blank=False)
    descr = models.TextField(blank=False)
    link = models.SlugField()
    duration = models.DurationField()
    products = models.ManyToManyField('Product', related_name='lessons')
    views = models.ManyToManyField('User', through='Views', related_name='lesson_views')


class Views(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='viewed_lessons')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='lesson_views')
    duration = models.DurationField()
    date = models.DateTimeField(auto_now_add=True)


class Access(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='accessed_products')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_access')
    value = models.BooleanField(default=False)
