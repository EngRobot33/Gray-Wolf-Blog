from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from account.models import User
from extensions.utils import jalali_converter


class PostManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children', verbose_name='زیردسته')
    title = models.CharField(max_length=256, verbose_name='عنوان دسته‌بندی')
    slug = models.SlugField(max_length=256, unique=True, verbose_name='آدرس دسته‌بندی')
    status = models.BooleanField(default=True, verbose_name='نمایش داده شود')
    position = models.IntegerField(verbose_name='موقعیت')

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Post(models.Model):
    STATUS_CHOICE = (
        ('p', 'منتشر شده'),
        ('d', 'پیش‌نویس'),
        ('i', 'در حال بررسی'),
        ('b', 'برگشت داده شده'),
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='posts', verbose_name='نویسنده')
    title = models.CharField(max_length=256, verbose_name='عنوان پست')
    slug = models.SlugField(max_length=256, unique=True, verbose_name='آدرس پست')
    category = models.ManyToManyField(Category, verbose_name='دسته‌بندی', related_name='posts')
    body = models.TextField(verbose_name='محتوای پست')
    thumbnail = models.ImageField(upload_to="images", verbose_name='تصویر پست')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name='پست ویژه')
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'
        ordering = ['-publish']  # ordering posts in webpage

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("account:home")

    def jpublish(self):
        return jalali_converter(self.publish)

    jpublish.short_description = 'زمان انتشار'

    def thumbnail_tag(self):
        return format_html("<img width=100 style='border-radius: 5px;' src={}>".format(self.thumbnail.url))

    thumbnail_tag.short_description = ' عکس'

    def category_to_string(self):
        return " - ".join([category.title for category in self.category.active()])

    category_to_string.short_description = 'دسته‌بندی'

    objects = PostManager()
