from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, ProductFormManagers
from catalog.models import Category, Product, Blog, Version


class IndexView(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Электроника- Главная'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]
        return context_data


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Blog.objects.get(pk=self.kwargs.get('pk'))
        context_data['pk'] = category_item.pk,
        context_data['title'] = f'{category_item.title}'

        return context_data


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Электроника - Территория низких цен!'
    }


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'), status_of_product=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = f'{category_item.name}'

        return context_data


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(sign_publication=True)
        return queryset

    extra_context = {
        'title': 'Блог'
    }


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = {'title', 'description', 'creation_data', 'sign_publication', 'preview'}
    success_url = reverse_lazy('catalog:blogs')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = {'title', 'description', 'creation_data', 'sign_publication', 'preview'}

    def get_success_url(self):
        return reverse_lazy('catalog:blog_detail', args=[self.object.pk])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blogs')


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:categories')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'catalog.change_product'
    form_class = ProductForm

    def get_form_class(self):
        if (self.request.user.is_staff and not self.request.user.is_superuser
                and self.object.owner != self.request.user):
            return ProductFormManagers
        else:
            return ProductForm

    def get_success_url(self):
        return reverse('catalog:categories')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data["formset"] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        self.object.owner = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        else:
            return self.form_invalid(form)

        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Страница товара'
    }


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:categories')

# def index(request):
#    context = {
#        'object_list': Category.objects.all()[:3],
#        'title': 'Электроника- Главная'
#    }
#    return render(request, 'catalog/index.html', context)

# def categories(request):
#    context = {
#        'object_list': Category.objects.all(),
#        'title': 'Электроника - Территория низких цен!'
#    }
#    return render(request, 'catalog/category_list.html', context)


# def electronic_category(request, pk):
#    category_item = Category.objects.get(pk=pk)
#    context = {
#        'object_list': Product.objects.filter(category_id=pk),
#        'title': f'{category_item.name}'
#    }
#    return render(request, 'catalog/product_list.html', context)

# def contacts(request):
#    if request.method == 'POST':
#        name = request.POST.get('name')
#        phone = request.POST.get('phone')
#        message = request.POST.get('message')
#        print(f"Имя: {name}, Номер телефона: {phone}, Сообщение: {message}")
#    return render(request, 'catalog/contacts.html')


# def blog_detail(request, pk):
#    category_item = Blog.objects.get(pk=pk)
#    context = {
#        'object_list': Blog.objects.filter(pk=pk),
#        'title': f'{category_item.title}'
#    }
#    return render(request, 'catalog/blog_detail.html', context)
