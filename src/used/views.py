# from django.views import ListView
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from carts.models import Cart

from .models import UsedProduct
from .forms import UsedForm


class ProductFeaturedListView(ListView):
    template_name = "newu/newz.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return UsedProduct.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    queryset = UsedProduct.objects.all().featured()
    template_name = "used/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()



class ProductListView(ListView):
    template_name = "newu/newz.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return UsedProduct.objects.all()


def product_list_view(request):
    queryset = UsedProduct.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "newu/newz.html", context)



class ProductDetailSlugView(DetailView):
    queryset = UsedProduct.objects.all()
    template_name = "used/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = UsedProduct.objects.get(slug=slug, active=True)
        except UsedProduct.DoesNotExist:
            raise Http404("Not found..")
        except UsedProduct.MultipleObjectsReturned:
            qs = UsedProduct.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance



class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "used/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)


def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk, featured=True) #id
    # instance = get_object_or_404(Product, pk=pk, featured=True)
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('no product here')
    #     raise Http404("Product doesn't exist")
    # except:
    #     print("huh?")

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")
    #print(instance)
    # qs  = Product.objects.filter(id=pk)

    # #print(qs)
    # if qs.exists() and qs.count() == 1: # len(qs)
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")

    context = {
        'object': instance
    }
    return render(request, "used/detail.html", context)


def AddUsedView(request):
    print 'watashiii ga kitta #### 1 ####'
    if request.method == 'POST':
        formset = UsedForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('http://127.0.0.1:8000/used/')
    else:
        print 'watashiii ga kitta'
        formset = UsedForm()
    return render(request, 'used_p.html', {'formset': formset})