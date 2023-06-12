from django.shortcuts import render, redirect, get_object_or_404
from Sky_store.models import Product, PageView, BlogPost
from django.views.generic import ListView, TemplateView, \
    DetailView, UpdateView, DeleteView, CreateView
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from Sky_store.forms import NewProductForm, ProductEditor
from Sky_store.models import Product, ProdVersion
from django.http import HttpResponse


def edit_product(request, id=id):
    product = Product.objects.get(pk=id)
    current_version = ProdVersion.objects.filter(product=product).latest('created_at')
    version_number = current_version.version_number
    form = ProductForm(instance=product) 
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store', product_id=product.product_id)
    return render(request, 'editor.html', {'form': form, 'product_name': product})

def add_product(request):
    banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                        'бесплатно', 'обман', 'полиция', 'радар']
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)
        name = request.POST.get('product_name')
        description = request.POST.get('product_desc')
        if name not in banned_words and description not in banned_words:
            if form.is_valid():
                form.save()
                return redirect('store')
        else:
            return render(request, 'error.html', {'message':'Используются запрещенные слова, товар небыл добавлен'})
    else:
        form = NewProductForm()
    return render(request, 'new_product.html', {'form': form})




def start_page(request):
    return render(request, 'sky_store/home.html')


def store_visitors():
    subject = ".:. Поздравляем! Вы стали 100-тым посетителем нашего магазина! .:."
    message = "Загляните в письмо, чтобы узнать что вас ждет :)\n" \
              "А ждет вас:\n" \
              "1 бесплатный товар на выбор и пожизненная скидка 10% в нашем магазине!"
    from_email = 'sky_store@rambler.ru'
    recipient_list = ['machodin@yandex.ru'] # Список адресов получателей
    send_mail(subject, message, from_email, recipient_list)


def counted(view_func):
    '''Сооздаем декоратор для обработки просмотров'''
    def wrapper(request, *args, **kwargs):
        page_url = request.get_full_path()
        view = PageView(page_url=page_url)
        view.save()

        page_views = PageView.objects.filter(page_url=page_url).count()

        if page_views == 100:
            pass

        return view_func(request, *args, **kwargs)
    return wrapper


class ProductStore(ListView):
    model = Product

    @method_decorator(counted)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем количество просмотров страницы
        page_url = self.request.path_info
        page_views = PageView.objects.filter(page_url=page_url).count()

        if page_views == 100:
            store_visitors()  # Отправляем письмо

        context['page_views'] = page_views
        return context

class BlogListView(ListView):
    '''
    Список блогов, сортировканный по дате
    '''
    model = BlogPost
    context_object_name = 'posts'
    template_name = 'blog.html'
    queryset = BlogPost.objects.filter(is_published=True)
    ordering = ['-published_date']

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post_detail.html'

    def get(self, request, *args, **kwargs):
        """
        Вызовется при GET запросе к детальной информации поста в блоге.
        """
        self.object = self.get_object()
        # инкрементируем счетчик просмотров
        self.object.views_count += 1
        self.object.save()
        context = self.get_context_data(object=self.object, page_views=self.object.views_count)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        context['page_views'] = kwargs['page_views']
        return context
class BlogPostCreateView(CreateView):
    '''
    Вьюшка создания
    '''
    model = BlogPost
    template_name = 'create_blog_post.html'
    fields = ['title', 'content', 'preview', 'is_published']


class BlogPostUpdateView(UpdateView):
    '''
    Вьюшка редактирования
    '''
    model = BlogPost
    template_name = 'update_blog_post.html'
    fields = ['title', 'content', 'preview', 'is_published']

class BlogPostDeleteView(DeleteView):
    '''
    Вьюшка удаления
    '''
    model = BlogPost
    template_name = 'delete_blog_post.html'
    success_url = reverse_lazy('blog')




# class StoreView(TemplateView):
#     template_name = 'Sky_store/store.html'
# Create your views here.
