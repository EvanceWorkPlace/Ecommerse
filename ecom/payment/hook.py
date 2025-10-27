# from paypal.standard.models import ST_PP_COMPLETED
# from paypal.standard.ipn.signals import valid_ipn_received
# from django.dispatch import receiver
# from django.conf import settings
# import time
# from .models import Order

# @receiver(valid_ipn_received)
# def paypal_payment_received(sender, **kwargs):
#     paypal_obj = sender

#     my_Invoice = str(paypal_obj.invoice)

#     my_Order = Order.objects.get(invoice=my_Invoice)
    
#     my_Order.paid = True

#     my_Order.save()
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Order

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender  # The IPN object

    # Only process completed payments
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        invoice_id = ipn_obj.invoice  # The invoice you sent in PayPalPaymentsForm

        try:
            order = Order.objects.get(my_invoice=invoice_id)  # Use the correct field
        except Order.DoesNotExist:
            return  # No order found for this invoice

        # Mark the order as paid
        order.paid = True
        order.save()
    