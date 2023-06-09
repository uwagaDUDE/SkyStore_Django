# Generated by Django 4.2.1 on 2023-06-19 12:06

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('Sky_store', '0013_alter_product_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
            },
        ),
        migrations.AlterModelOptions(
            name='prodversion',
            options={'ordering': ['-version']},
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('versions', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='version_num',
        ),
        migrations.AddField(
            model_name='prodversion',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prodversion',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='prodversion',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/products'),
        ),
        migrations.AddField(
            model_name='prodversion',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prodversion',
            name='version',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='version_cur',
            field=models.BooleanField(default=True, verbose_name='Текущая версия'),
        ),
        migrations.AlterField(
            model_name='prodversion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='prodversion',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='Sky_store.product'),
        ),
        migrations.AlterField(
            model_name='prodversion',
            name='version_num',
            field=models.IntegerField(null=True),
        ),
    ]
