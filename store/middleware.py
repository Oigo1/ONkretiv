from django.utils.deprecation import MiddlewareMixin
from .models import Order, OrderItem

class CartTransferMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and hasattr(request, 'session'):
            session_key = request.session.session_key
            if session_key:
                session_order = Order.objects.filter(session_key=session_key, complete=False).first()
                if session_order:
                    customer_order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
                    
                    for item in session_order.orderitem_set.all():
                        existing_item = customer_order.orderitem_set.filter(product=item.product).first()
                        if existing_item:
                            existing_item.quantity += item.quantity
                            existing_item.save()
                        else:
                            item.order = customer_order
                            item.save()
                    
                    session_order.delete()
                    request.session['cart'] = {}