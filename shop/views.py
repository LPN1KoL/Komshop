from random import choice
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
from django.http import JsonResponse

# Create your views here.



def home(request):
	ps = Product.objects.all()
	p1 = choice(ps)
	p2 = choice(ps)
	p3 = choice(ps)
	p4 = choice(ps)
	p5 = choice(ps)
	p6 = choice(ps)
	categories = Category.objects.all()

	return render(request, 'new_ui/home.html', {
		'name_1': p1.name, 'price_1': p1.price, 'image_1': p1.photo.url,
		'name_2': p2.name, 'price_2': p2.price, 'image_2': p2.photo.url,
		'name_3': p3.name, 'price_3': p3.price, 'image_3': p3.photo.url,
		'name_4': p4.name, 'price_4': p4.price, 'image_4': p4.photo.url,
		'name_5': p5.name, 'price_5': p5.price, 'image_5': p5.photo.url,
		'name_6': p6.name, 'price_6': p6.price, 'image_6': p6.photo.url,
		'categories': categories
	})


def login_view(request):
	if request.method == 'GET':
		return render(request, 'base/login.html', {
			'form': LoginForm()
		})

	elif request.method == 'POST':
		login_ = request.POST.get('login')
		password_ = request.POST.get('password')

		usr = authenticate(request, username=login_, password=password_)

		if usr is not None:
			user_login(request, usr)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'base/login.html', {
				'form': LoginForm(request.POST)
			})


def reg_view(request):
	if request.method == 'GET':
		return render(request, 'base/register.html', {
			'form': RegForm()
		})
	else:
		form = RegForm(request.POST)
		error = ''

		login = request.POST.get('login')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		email = request.POST.get('email')

		if form.is_valid():
			if password != password2:
				error = 'Введённые пароли не совпадают!\n'
			if CustomUser.objects.filter(email=email).exists():
				error = 'Введённый адрес электронной почты занят!\n'
			if CustomUser.objects.filter(username=login).exists():
				error = 'Пользователь с таким логином уже существует!\n'

			if error:
				return render(request, 'base/register.html', {
					'form': form,
					'error': error
				})

			else:
				new_user = CustomUser.objects.create(
					username=login,
					email=email
				)

				new_user.set_password(password)
				new_user.save()

				return HttpResponseRedirect('/login')


def logout(request):
	user_logout(request)
	return HttpResponseRedirect('/')


def catalog(request):
	products = []
	search = request.POST.get('FD1')
	print(request.POST)
	cat_name = request.GET.get('cat')
	price_start = request.POST.get('price_start')
	price_end = request.POST.get('price_end')
	category = Category.objects.filter(name=cat_name)
	product_cat = ProductCategory.objects.filter(category=category[0])
	if search:
		for prod_c in product_cat:
			if prod_c.product.name.startswith(search):
				if price_start or price_end:
					if price_start and price_end:
						if prod_c.product.price >= float(price_start) and prod_c.product.price <= float(price_end):
							products.append(prod_c.product.to_json())

					elif price_start and not price_end:
						if prod_c.product.price >= float(price_start):
							products.append(prod_c.product.to_json())

					elif price_end and not price_start:
						if prod_c.product.price <= float(price_end):
							products.append(prod_c.product.to_json())

				else:
					products.append(prod_c.product.to_json())

			else:
				product_tags = ProductTag.objects.filter(product=prod_c.product)
				for p_tag in product_tags:
					if p_tag.tag.name.startswith(search):
						if price_start or price_end:
							if price_start and price_end:
								if prod_c.product.price >= float(price_start) and prod_c.product.price <= float(price_end):
									products.append(prod_c.product.to_json())

							elif price_start and not price_end:
								if prod_c.product.price >= float(price_start):
									products.append(prod_c.product.to_json())

							elif price_end and not price_start:
								if prod_c.product.price <= float(price_end):
									products.append(prod_c.product.to_json())

						else:
							products.append(prod_c.product.to_json())
	else:
		if price_start or price_end:
			if price_start and price_end:
				for prod_c in product_cat:
					if prod_c.product.price >= float(price_start) and prod_c.product.price <= float(price_end):
						products.append(prod_c.product.to_json())

			elif price_start and not price_end:
				for prod_c in product_cat:
					if prod_c.product.price >= float(price_start):
						products.append(prod_c.product.to_json())

			elif price_end and not price_start:
				for prod_c in product_cat:
					if prod_c.product.price <= float(price_end):
						products.append(prod_c.product.to_json())

		else:
			for prod_c in product_cat:
				products.append(prod_c.product.to_json())

	return render(request, 'base/catalog.html', {'cat_name': cat_name, 'products': products, 'search': search})



