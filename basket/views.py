from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product
from django.contrib import messages

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, "basket/basket_summary.html", {"basket": basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        messages.add_message(request, messages.SUCCESS, "Added item to your basket")
        return JsonResponse({"qty": basketqty})


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        messages.add_message(request, messages.ERROR, "Removed item from your basket")
        return JsonResponse({"qty": basketqty, "subtotal": baskettotal})


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        messages.add_message(request, messages.SUCCESS, "Update item in your basket")
        return JsonResponse({"qty": basketqty, "subtotal": baskettotal})
