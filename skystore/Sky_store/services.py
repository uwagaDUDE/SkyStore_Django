from django.conf import settings
from django.core.mail import send_mail

def send_email(user):
    send_mail(
        'Вы наш миллионный посетитель!',
        'Чтобы забрать свою бесплатную картофелину, перейдите по ссылке!'
        'Это точно не вирус! - virus.com', settings.EMAIL_HOST_USER, [user.email]
    )