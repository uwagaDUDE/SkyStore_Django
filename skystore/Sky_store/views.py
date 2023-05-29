from django.shortcuts import render
from Sky_store.models import Product, PageView
from django.views.generic import ListView, TemplateView
from django.core.mail import send_mail
from django.utils.decorators import method_decorator


def start_page(request):
    return render(request, 'sky_store/home.html')


def send_email():
    subject = "ВЫ НАШ 100 ПОСЕТИТЕЛЬ!"
    message = "ПОЗДРАВЛЯЕМ! ВЫ НАШ 100 ПОКУПАТЕЛЬ! ВАМ ДАЕТСЯ СКИДКА В 100% НА ЛЮБОЙ ТОВАР!"
    from_email = 'puvir00@gmail.com'
    recipient_list = ['puvir@yandex.ru'] # Список адресов получателей
    send_mail(subject, message, from_email, recipient_list)


def counted(view_func):
    '''Сооздаем декоратор для обработки просмотров'''
    def wrapper(request, *args, **kwargs):
        page_url = request.get_full_path()
        view = PageView(page_url=page_url)
        view.save()

        page_views = PageView.objects.filter(page_url=page_url).count()

        if page_views == 50:
            send_email()

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
            send_email()  # Отправляем письмо

        context['page_views'] = page_views
        return context






# class StoreView(TemplateView):
#     template_name = 'Sky_store/store.html'
# Create your views here.
