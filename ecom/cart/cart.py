from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        #Get the Session Key if it exists
        cart = self.session.get('session_key')

        #if the user is now, no session key! create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure cart is available in all sites 
        self.cart = cart

    def add(self, product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = str(product_qty)
        self.session.modified = True
    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        #get is from cart
        product_ids = self.cart.keys()
        #use ids to lookup products in database
        products = Product.objects.filter(id__in=product_ids)
        #returm those lookup up products
        return products
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product,quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #Get the card

        ourcart = self.cart
        #update Dictionary/cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        thing = self.cart
        return thing

