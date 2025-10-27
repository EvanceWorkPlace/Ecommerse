from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime

from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from store.models import Product, Profile
# import paypal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # unique user id for duplicate

# 🧾 VIEW A SINGLE ORDER (ADMIN ONLY)
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        if request.method == "POST":
            status = request.POST.get('shipping_status')
            now = datetime.datetime.now()

            if status == "true":
                
                order.shipped = True
                order.date_shipped = now
                order.save()
                messages.success(request, "Shipping Status Updated! View the updated table (Not Shipped).")
                return redirect('not_shipped_dash')
            else:
                order.shipped = False
                order.save()
                messages.success(request, "Shipping Status Updated! View the updated table (Shipped).")
                return redirect('shipped_dash')

        return render(request, 'payments/orders.html', {"order": order, "items": items})

    messages.error(request, "Access Denied.")
    return redirect('home')


# 🚚 DASHBOARD: NOT SHIPPED ORDERS
def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.method == "POST":
            num = request.POST.get('num')
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
            messages.success(request, "Shipping Status Updated! View the updated Table (Not Shipped).")
            return redirect('not_shipped_dash')

        return render(request, 'payments/not_shipped_dash.html', {"orders": orders})

    messages.error(request, "Access Denied.")
    return redirect('home')


# 🚚 DASHBOARD: SHIPPED ORDERS
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        if request.method == "POST":
            num = request.POST.get('num')
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
            messages.success(request, "Shipping Status Updated! View the updated Table (Shipped).")
            return redirect('shipped_dash')

        return render(request, 'payments/shipped_dash.html', {"orders": orders})

    messages.error(request, "Access Denied.")
    return redirect('home')


# 💳 PROCESS ORDER (MAIN CHECKOUT FUNCTION)
def process_order(request):
    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Get shipping info from session
        my_shipping = request.session.get('my_shipping')
        if not my_shipping:
            messages.error(request, "Shipping information is missing!")
            return redirect('checkout')

        # Extract shipping details
        full_name = my_shipping.get('shipping_full_name')
        email = my_shipping.get('shipping_email')
        shipping_address = (
            f"{my_shipping.get('shipping_address1')}\n"
            f"{my_shipping.get('shipping_address2')}\n"
            f"{my_shipping.get('shipping_city')}\n"
            f"{my_shipping.get('shipping_state')}\n"
            f"{my_shipping.get('shipping_zipcode')}\n"
            f"{my_shipping.get('shipping_country')}"
        )
        amount_paid = totals

        # Create Order
        if request.user.is_authenticated:
            user = request.user
            order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
        else:
            order = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )

        order.save()

        # Create Order Items
        for product in cart_products:
            product_id = product.id
            price = product.sale_price if product.is_sale else product.price
            quantity = quantities.get(str(product.id), 1)

            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                user=request.user if request.user.is_authenticated else None,
                quantity=quantity,
                price=price
            )

        # ✅ Clear the cart (session + DB)
        cart.clear()

        if 'my_shipping' in request.session:
            del request.session['my_shipping']

        if request.user.is_authenticated:
            Profile.objects.filter(user=request.user).update(old_cart="")

        messages.success(request, "Order placed successfully!")
        return redirect('home')

    messages.error(request, "Access denied.")
    return redirect('home')


# 🧾 BILLING INFORMATION PAGE

def billing_info(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.method == "POST":
        shipping_form = ShippingForm(request.POST)
        billing_form = PaymentForm(request.POST)

        if shipping_form.is_valid() and billing_form.is_valid():
            shipping_data = shipping_form.cleaned_data
            request.session['my_shipping'] = shipping_data

            my_invoice = str(uuid.uuid4())

            if request.user.is_authenticated:
                order = Order(
                    user=request.user,
                    full_name=shipping_data['shipping_full_name'],
                    email=shipping_data['shipping_email'],
                    shipping_address=(
                        f"{shipping_data['shipping_address1']}\n"
                        f"{shipping_data['shipping_address2']}\n"
                        f"{shipping_data['shipping_city']}\n"
                        f"{shipping_data['shipping_state']}\n"
                        f"{shipping_data['shipping_zipcode']}\n"
                        f"{shipping_data['shipping_country']}"
                    ),
                    amount_paid=totals,
                    invoice=my_invoice
                )
            else:
                order = Order(
                    full_name=shipping_data['shipping_full_name'],
                    email=shipping_data['shipping_email'],
                    shipping_address=(
                        f"{shipping_data['shipping_address1']}\n"
                        f"{shipping_data['shipping_address2']}\n"
                        f"{shipping_data['shipping_city']}\n"
                        f"{shipping_data['shipping_state']}\n"
                        f"{shipping_data['shipping_zipcode']}\n"
                        f"{shipping_data['shipping_country']}"
                    ),
                    amount_paid=totals,
                    invoice=my_invoice
                )

            order.save()
            # Save order items here...

            host = request.get_host()
            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': totals,
                'item_name': 'Book Order',
                'invoice': my_invoice,
                'currency_code': 'ZAR',
                'notify_url': f'https://{host}{reverse("paypal-ipn")}',
                'return_url': f'https://{host}{reverse("payment_success")}',
                'cancel_return': f'https://{host}{reverse("payment_failed")}',
                'no_shipping': '2',
            }

            paypal_form = PayPalPaymentsForm(initial=paypal_dict)

            return render(request, 'payments/billing_info.html', {
                'paypal_form': paypal_form,
                'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_form': shipping_form,
                'billing_form': billing_form
            })

    else:
        shipping_form = ShippingForm()
        billing_form = PaymentForm()

    return render(request, 'payments/billing_info.html', {
        'paypal_form': None,
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_form': shipping_form,
        'billing_form': billing_form
    })
# def billing_info(request):
#     cart = Cart(request)
#     cart_products = cart.get_prods()
#     quantities = cart.get_quants()
#     totals = cart.cart_total()

#     if request.method == "POST":
#         # Save shipping info in session
#         request.session['my_shipping'] = request.POST

#         host = request.get_host()
#         paypal_dict = {
#             'business': settings.PAYPAL_RECEIVER_EMAIL,
#             'amount': totals,
#             'item_name': 'Book Order',
#             'no_shipping': '2',
#             'invoice': str(uuid.uuid4()),
#             'currency_code': 'ZAR',
#             'notify_url': 'https://{}{}'.format(host, reverse('paypal-ipn')),
#             'return_url': 'https://{}{}'.format(host, reverse('payment_success')),
#             'cancel_return': 'https://{}{}'.format(host, reverse('payment_failed')),
#         }

#         paypal_form = PayPalPaymentsForm(initial=paypal_dict)
#         billing_form = PaymentForm()


#         return render(request, 'payments/billing_info.html', {
#             'paypal_form': paypal_form,
#             'cart_products': cart_products,
#             'quantities': quantities,
#             'totals': totals,
#             'shipping_info': request.POST,
#             'billing_form': billing_form
#         })

#     messages.error(request, "Access Denied.")
#     return redirect('home')


# ✅ SUCCESS PAGE
def payment_success(request):
    return render(request, "payments/payment_success.html", {})

def payment_failed(request):
    return render(request, "payments/payment_failed.html", {})

# 🧾 CHECKOUT PAGE
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(user__id=request.user.id).first()
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingForm(request.POST or None)

    return render(request, 'payments/checkout.html', {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form
    })


# 🔒 CUSTOM LOGOUT THAT CLEARS SESSION CART
def custom_logout(request):
    logout(request)
    if 'cart' in request.session:
        del request.session['cart']
    messages.success(request, "Logged out successfully and cart cleared.")
    return redirect('home')


# 🕒 SIGNAL: AUTO-SET SHIPPED DATE WHEN UPDATED
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now
