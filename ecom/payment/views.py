from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User

def process_order(request):
    if request.method == "POST":
        # Initialize cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()  # calculate total amount

        # Get shipping info from session
        my_shipping = request.session.get('my_shipping')
        if not my_shipping:
            messages.error(request, "Shipping information is missing!")
            return redirect('checkout')

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

        # Create the order
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

        # Create order items
        for product in cart_products:
            qty = quantities.get(str(product.id), 1)
            price = product.sale_price if product.is_sale else product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                price=price,
                quantity=qty
            )

        # Clear the cart after order
        

        # Clear shipping info session
        if 'my_shipping' in request.session:
            del request.session['my_shipping']

        messages.success(request, "Order placed successfully!")
        return redirect('home')

    else:
        messages.error(request, "Access denied.")
        return redirect('home')



def billing_info(request):

    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        #create session  with shipping
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        #check to see if user is logged in
        if request.user.is_authenticated:
            # get the billing
            billing_form = PaymentForm()
            return render(request, 'payments/billing_info.html', {"cart_products":cart_products , "quantities":quantities , "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        else:
            # not logged in
            billing_form = PaymentForm()
            return render(request, 'payments/billing_info.html', {"cart_products":cart_products , "quantities":quantities , "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        shipping_form = request.POST
        return render(request, 'payments/billing_info.html', {"cart_products":cart_products , "quantities":quantities , "totals":totals, "shipping_form":shipping_form})

    else:
        messages.success(request, "Access Denied")
        return redirect('home')

    
# Create your views here.
def payment_success(request):
    
    return render(request, "payments/payment_success.html", {})    
# Create your views here.
def checkout(request):
    #get the cart 

    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(user__id=request.user.id).first()
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payments/checkout.html', {"cart_products":cart_products , "quantities":quantities , "totals":totals, "shipping_form":shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payments/checkout.html', {"cart_products":cart_products , "quantities":quantities , "totals":totals, "shipping_form":shipping_form})

    
