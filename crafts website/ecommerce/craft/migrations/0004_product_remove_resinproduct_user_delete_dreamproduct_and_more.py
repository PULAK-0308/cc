# Generated by Django 4.2.1 on 2023-06-30 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('craft', '0003_dreamproduct_user_resinproduct_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('category', models.CharField(default='', max_length=50)),
                ('subcategory', models.CharField(default='', max_length=50)),
                ('image', models.ImageField(default='', upload_to='craft/images')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='resinproduct',
            name='user',
        ),
        migrations.DeleteModel(
            name='DreamProduct',
        ),
        migrations.DeleteModel(
            name='ResinProduct',
        ),
    ]
