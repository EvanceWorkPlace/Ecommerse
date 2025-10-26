from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        # get requst
        self.request = request
        #Get the Session Key if it exists
        cart = self.session.get('session_key')

        #if the user is now, no session key! create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure cart is available in all sites 
        self.cart = cart
    def db_add(self,product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3':1 , '2': 1} {"3":1 , "2": 1}
            #convert 
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the profile Model
            current_user.update(old_cart=str(carty))
    

    def add(self, product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3':1 , '2': 1} {"3":1 , "2": 1}
            #convert 
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the profile Model
            current_user.update(old_cart=str(carty))
    
    def cart_total(self):
        #Get product id
        product_ids = self.cart.keys()
        # loookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        #start counting at 0
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * int(value)
                    else:
                        total += product.price * int(value)
        return total
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

        if hasattr(self, 'request') and hasattr(self.request, 'user') and self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3':1 , '2': 1} {"3":1 , "2": 1}
            #convert 
            carty = str(self.cart)
            carty = carty.replace("'","\"")
            # Save carty to the profile Model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing
    def delete(self, product):
        product_id = str(product)

        deletecart = self.cart
        #delete the cart

        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # {'3':1 , '2': 1} {"3":1 , "2": 1}
            #convert 
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the profile Model
            current_user.update(old_cart=str(carty))
    
    def clear(self):
        """Remove all items from the cart."""
        self.session['session_key'] = {}
        self.session.modified = True

