"""
Definition of models.
"""

from django.db import models

# Create your models here.
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse


class Blog(models.Model):
	title = models.CharField(max_length = 100, unique_for_date = 'posted', verbose_name = 'Заголовок')
	description = models.TextField(verbose_name = 'Краткое содержание')
	content = models.TextField(verbose_name = 'Полное содержание')
	posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = 'Опубликовано')
	author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
	image = models.FileField(default = 'temp.jpg', verbose_name = 'Путь к картинке')

	def get_absolute_url(self):
		return reverse('blogpost', args=[str(self.id)])

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'Posts'
		ordering = ['posted']
		verbose_name = 'Статья блога'
		verbose_name_plural = 'Статьи блога'



class Comment(models.Model):
	text = models.TextField(verbose_name = 'Комментарий')
	date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = 'Дата')
	author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
	post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья")


	def __str__(self):
		return 'Комментарий %s к %s' % (self.author, self.post)

	class Meta:
		db_table = 'Comments'
		ordering = ['-date']
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии к статьям блога'


class UserProfile(models.Model):
	ROLES = (
		('client', 'Клиент'),
		('moder','Модераток'),
		('admin','Администратор')
	)

	SIDES = (
		('angel','Кровавые ангелы'),
		('tiran','Тираниды'),
		('none', 'Не выбрано')
		
		)

	user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Пользователь")
	role = models.CharField(max_length = 300, choices = ROLES, verbose_name = "Роль")
	choosedSide = models.CharField(max_length = 300, choices = SIDES, verbose_name = "Сторона")


	def __str__(self):
		return 'Пользователь'

	class Meta:
		db_table = 'UserProfile'
		ordering = ['user']
		verbose_name = 'Профили'
		verbose_name_plural = 'Профили'

class Shop(models.Model):

	SIDES = (
		('angel','Кровавые ангелы'),
		('tiran','Тираниды'),
		('none', 'Не выбрано')
		
		)
	CATEGORY = (
		('models','Модельки'),
		('books','Книги'),
		('lands','Поля'),
		('add','Дополнительные детали'),
		('tshirt','Футболки'),
		('shirt','Толстовки'),
		('cosplay','Косплей'),
		('figurki','Фигурки'),
		
		)
	name = models.CharField(max_length = 300, verbose_name = "Название")
	category = models.CharField(max_length = 300, verbose_name = 'Категория', choices = CATEGORY)
	desc = models.TextField(verbose_name = "Описание")
	price = models.IntegerField(verbose_name = "Цена")
	side = models.CharField(max_length = 300, choices = SIDES, verbose_name = "Сторона")
	image = models.FileField(default = 'temp.jpg', verbose_name = 'Путь к картинке')

	class Meta:
		db_table = 'Shop'
		ordering = ['id']
		verbose_name = 'Товары'
		verbose_name_plural = 'Товары'

class Orders(models.Model):
	STATUS = (
		('incart', 'В корзине'),
		('check', 'Проверяется'),
		('indeliver', 'Доставляется'),
		('delivered', 'Доставлен')
	)
	holder = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Покупатель')
	status = models.CharField(verbose_name = 'Статус', choices = STATUS, max_length=300)
	total_price = models.IntegerField(default = 0, verbose_name = 'Итоговая стоимость')


	def __str__(self):
		return 'Заказ %s' % (self.id)

	class Meta:
		db_table = 'Orders'
		ordering = ['holder']
		verbose_name = 'Заказы'
		verbose_name_plural = 'Заказы'

class SubOrders(models.Model):
	order = models.ForeignKey(Orders, on_delete = models.CASCADE, verbose_name = 'Заказ')
	product = models.ForeignKey(Shop, on_delete = models.CASCADE, verbose_name = 'Товар')
	quantity = models.IntegerField(default = 1, verbose_name = 'Количество')
	price = models.IntegerField(default = 0, verbose_name = 'Стоимость товаров')
	


	def __str__(self):
		return 'Товар %s к заказу %s' % (self.product, self.order)

	class Meta:
		db_table = 'SubOrders'
		ordering = ['order']
		verbose_name = 'Товары'
		verbose_name_plural = 'Товары заказа'




admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Shop)
admin.site.register(Orders)
admin.site.register(SubOrders)