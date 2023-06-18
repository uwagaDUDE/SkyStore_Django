import django.contrib.auth.base_user
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
# Create your models here.

class ProductVersionManager(models.Manager):
    def current(self):
        return self.filter(version_cur=True).order_by('-id').first()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, verbose_name='Название')
    product_desc = models.CharField(max_length=1000, verbose_name='Описание')
    product_pic = models.ImageField(verbose_name='Картинка', null=True, blank=True, upload_to='media/products')
    product_cat = models.CharField(max_length=100, verbose_name='Категория')
    product_price = models.IntegerField(verbose_name='Цена')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             blank=True, null=True)
    product_mk = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    product_ed = models.DateTimeField(default=timezone.now, verbose_name='Дата изменения')
    version_cur = models.BooleanField(default=True, verbose_name='Текущая версия')
    versions = ProductVersionManager()

    def __str__(self):
        return f"{self.product_name} - {self.version_cur}"

    class Meta:
        verbose_name = 'Продукты'


class ProductEditor(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'product_desc', 'product_pic', 'product_cat', 'product_price',)


class ProdVersionManager(models.Manager):
    def current(self):
        return self.filter(version_cur=True).order_by('-id').first()


class ProdVersion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    version = models.PositiveIntegerField()
    version_num = models.IntegerField(null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='media/products', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    version_cur = models.BooleanField(default=True)  # Флаг текущей версии
    objects = ProdVersionManager()

    def set_current(self):
        """
        Отключает флаг version_cur для всех старых версий и включает его для текущей версии.
        """
        self.product.versions.exclude(id=self.id).update(version_cur=False)
        self.version_cur = True
        self.save()
    class Meta:
        ordering = ['-version']  # Сортируем версии в обратном порядке


class PageView(models.Model):
    page_url = models.URLField()
    view_date = models.DateTimeField(auto_now_add=True)


class ProductCategory(models.Model):
    category = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'

class BlogPost(models.Model):
    '''
    Создаем модель блога
    '''
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, editable=False, blank=False, null=False)
    preview = models.ImageField(verbose_name='Картинка', null=True, blank=True, upload_to='media/')
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def generate_slug(self):
        '''
        Генератор SLUG ссылки
        :return:
        '''
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while BlogPost.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'slug': self.slug})

