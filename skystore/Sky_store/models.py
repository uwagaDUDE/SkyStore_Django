from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, verbose_name='Название')
    product_desc = models.CharField(max_length=1000, verbose_name='Описание')
    product_pic = models.ImageField(verbose_name='Картинка', null=True, blank=True, upload_to='media/products')
    product_cat = models.CharField(max_length=100, verbose_name='Категория')
    product_price = models.IntegerField(verbose_name='Цена')
    product_mk = models.CharField(max_length=100, verbose_name='Дата создания')
    product_ed = models.CharField(max_length=100, verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.product_name} {self.product_price} {self.product_cat}'

    class Meta:
        verbose_name = 'Продукты'


class ProdVersion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_num = models.IntegerField()
    version_cur = models.BooleanField(default=True)

class PageView(models.Model):
    page_url = models.URLField()
    view_date = models.DateTimeField(auto_now_add=True)

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

