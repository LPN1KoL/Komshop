from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import *

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Role(models.Model):
	name = models.CharField(max_length=100, verbose_name='Название', null=False)
	access_to_admin_panel = models.BooleanField(default=False, verbose_name='Доступ к панели управления')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Роль'
		verbose_name_plural = 'Роли'


class CustomUser(AbstractBaseUser):
	username = models.CharField(verbose_name='Имя пользователя', max_length=150, null=False, default=None, unique=True)
	email = models.EmailField(unique=True, null=True, default=None, blank=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	name = models.CharField(verbose_name='Имя', max_length=150, null=True, default=None)
	surname = models.CharField(verbose_name='Фамилия', max_length=150, null=True, default=None, blank=True)

	role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, default=None, blank=True, verbose_name='Роль')

	objects = CustomUserManager()
	USERNAME_FIELD = 'username'

	def has_perm(self, perm, obj=None):
		return self.is_superuser

	def has_module_perms(self, app_label):
		return self.is_superuser

	def get_privs(self):
		return []

	def get_name(self):
		return f'{self.name} {self.surname}'

	class Meta:
		db_table = 'auth_user'
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return f'{self.name} {self.surname}'


class Tag(models.Model):
	name = models.CharField(verbose_name='Тэг товара', max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Тэг товара'
		verbose_name_plural = 'Тэги товаров'


class Category(models.Model):
	name = models.CharField(verbose_name='Категория товара', max_length=150)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Категория товара'
		verbose_name_plural = 'Категории товаров'


class Product(models.Model):
	product_code = models.CharField(max_length=50, verbose_name='Код товара', null=False)
	name = models.CharField(max_length=255, verbose_name='Наименование товара', null=False)
	age_start = models.PositiveIntegerField(verbose_name='Возраст (от)', null=True, blank=True)
	age_end = models.PositiveIntegerField(verbose_name='Возраст (до)', null=True, blank=True)
	photo = models.ImageField(verbose_name='Общий вид', upload_to='products_images', null=True, blank=True)
	height = models.PositiveIntegerField(verbose_name='Высота', null=True, blank=True)
	width = models.PositiveIntegerField(verbose_name='Ширина', null=True, blank=True)
	length = models.PositiveIntegerField(verbose_name='Длина', null=True, blank=True)
	params = models.TextField(verbose_name='Дополнительные параметры', null=True, default=None, blank=True)
	weight = models.FloatField(verbose_name='Вес', null=True, blank=True)
	concrete = models.FloatField(verbose_name='Бетон', null=True, blank=True)
	installation_time = models.FloatField(verbose_name='Время установки', null=True, blank=True)
	price = models.FloatField(verbose_name='Цена')


	def __str__(self):
		return f'{self.name} ({self.product_code})'

	def to_json(self):
		return {'name': self.name, 'id': self.id, 'product_code': self.product_code, 'price': self.price, 'installation_time': self.installation_time, 'concrete': self.concrete, 'weight': self.weight, 'length': self.length, 'width': self.width, 'height': self.height, 'photo': self.photo.url, 'age_start': self.age_start, 'age_end': self.age_end}

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'


class ProductTag(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тэг')

	class Meta:
		verbose_name = 'Товар-тег'


class ProductCategory(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

	class Meta:
		verbose_name = 'Товар-категория'


# Receivers
@receiver(post_save, sender=CustomUser)
def after_user_create(sender, instance, created, **kwargs):
	if created:
		if not Role.objects.filter(name='Клиент').exists():
			Role.objects.create(name='Клиент', access_to_admin_panel=False)
		if not Role.objects.filter(name='Администратор').exists():
			Role.objects.create(name='Администратор', access_to_admin_panel=True)

		if instance.is_superuser:
			instance.role = Role.objects.get(name='Администратор')
		else:
			instance.role = Role.objects.get(name='Клиент')

		instance.save()
