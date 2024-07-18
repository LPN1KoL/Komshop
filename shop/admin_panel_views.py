from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt


@login_required
def admin_panel(request):
	if request.user.role.access_to_admin_panel:

		return render(request, 'admin_panel/home.html')

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_roles(request):
	if request.user.role.access_to_admin_panel:

		roles = Role.objects.all()

		return render(request, 'admin_panel/roles.html', {
			'roles': roles
		})

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_product_categories(request):
	if request.user.role.access_to_admin_panel:

		categories = Category.objects.all()

		return render(request, 'admin_panel/product_categories.html', {
			'categories': categories
		})

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_tags(request):
	if request.user.role.access_to_admin_panel:

		tags = Tag.objects.all()

		return render(request, 'admin_panel/tags.html', {
			'tags': tags
		})

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_products(request):
	if request.user.role.access_to_admin_panel:

		products = Product.objects.all()

		return render(request, 'admin_panel/products.html', {
			'products': products
		})

	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_products_add(request):
	if request.user.role.access_to_admin_panel:
		form = ProductForm()
		if request.method == 'GET':
			return render(request, 'admin_panel/product_add.html', {
				'form': form
				})
		else:
			form = ProductForm(request.POST, request.FILES)
			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/products')
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_add_tag(request):
	if request.user.role.access_to_admin_panel:
		form = TagForm()
		if request.method == 'GET':
			return render(request, 'admin_panel/tag_add.html', {
					'form': form
				})
		else:
			form = TagForm(request.POST)
			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/tags')
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_add_category(request):
	if request.user.role.access_to_admin_panel:
		form = CategoryForm()
		if request.method == 'GET':
			return render(request, 'admin_panel/category_add.html', {
				'form': form
			})
		else:
			form = CategoryForm(request.POST)
			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/categories')
	else:
		return HttpResponseNotFound(request)


@login_required
def admin_panel_edit_product(request, pid):
	if request.user.role.access_to_admin_panel:

		product = Product.objects.get(id=pid)
		form = ProductForm(instance=product)

		if request.method == 'GET':

			p_tags = [x.tag for x in ProductTag.objects.filter(product=product)]
			ptids = [x.id for x in p_tags]
			all_tags = [x for x in Tag.objects.all() if x.id not in ptids]

			p_cats = [x.category for x in ProductCategory.objects.filter(product=product)]
			pcids = [x.id for x in p_cats]
			all_cats = [x for x in Category.objects.all() if x.id not in pcids]

			return render(request, 'admin_panel/product_edit.html', {
				'form': form,
				'photo_url': product.photo.url,
				'product_tags': p_tags,
				'product_categories': p_cats,
				'all_tags': all_tags,
				'all_categories': all_cats,
				'pid': product.id
			})
		elif request.method == 'POST':
			form = ProductForm(request.POST, request.FILES, instance=product)

			if form.is_valid:
				form.save()
				return HttpResponseRedirect('/admin_panel/products')
	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_remove_product_tag(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			product = Product.objects.get(id=int(request.POST.get('pid')))
			tag = Tag.objects.get(id=int(request.POST.get('tid')))

			ProductTag.objects.filter(product=product, tag=tag).delete()

			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_add_product_tag(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			product = Product.objects.get(id=int(request.POST.get('pid')))
			tag = Tag.objects.get(id=int(request.POST.get('tid')))

			if ProductTag.objects.filter(product=product, tag=tag).count() == 0:
				ProductTag.objects.create(product=product, tag=tag)

				return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_remove_product_cat(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			product = Product.objects.get(id=int(request.POST.get('pid')))
			cat = Category.objects.get(id=int(request.POST.get('cid')))

			ProductCategory.objects.filter(product=product, category=cat).delete()

			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_add_product_cat(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			product = Product.objects.get(id=int(request.POST.get('pid')))
			cat = Category.objects.get(id=int(request.POST.get('cid')))

			if ProductCategory.objects.filter(product=product, category=cat).count() == 0:
				ProductCategory.objects.create(product=product, category=cat)

				return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def delete_product(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			Product.objects.filter(id=int(request.POST.get('pid'))).delete()
			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_delete_category(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			cid = int(request.POST.get('cid'))

			Category.objects.filter(id=cid).delete()
			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)


@csrf_exempt
@login_required
def admin_panel_delete_tag(request):
	if request.user.role.access_to_admin_panel:
		if request.method == 'POST':

			cid = int(request.POST.get('tid'))

			Tag.objects.filter(id=cid).delete()
			return JsonResponse({}, status=200)

	else:
		return HttpResponseNotFound(request)
