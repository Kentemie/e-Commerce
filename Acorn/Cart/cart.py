from django.conf import settings

from Inventory.models import ProductInventory

from Delivery.models import DeliveryOptions


class Cart:

    """
    A base Cart class, providing some default behaviors that 
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(settings.BASKET_SESSION_ID, {})
    
    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products.
        """
        product_ids = self.cart.keys()
        cart = self.cart.copy()

        products = ProductInventory.objects.filter(
            id__in=product_ids
        )

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["total_price"] = item["store_price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Get the cart data and count the quantity of items.
        """
        return sum(item["quantity"] for item in self.cart.values())
    

    def add(self, product, product_qty):
        """
        Adding and updating the users cart session data.
        """

        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]["quantity"] = int(product_qty)
        else:
            self.cart[product_id] = {
                "store_price": float(product.store_price),
                "quantity": int(product_qty)
            }

        self.save()
    
    def delete(self, product):
        """
        Delete item from session data
        """
        if product in self.cart:
            del self.cart[product]
        

        self.save()

    def update(self, product_id, product_qty):
        """
        Update values in session data
        """
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = int(product_qty)

        self.save()


    def get_subtotal_price(self):
        return sum(item["quantity"] * item["store_price"] for item in self.cart.values())

    def cart_update_delivery(self, delivery_price=0.00):
        subtotal = self.get_subtotal_price()
        return subtotal + delivery_price

    def get_delivery_price(self):
        newprice = 0

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice
    
    def get_total_price(self):
        newprice = self.get_delivery_price()
        subtotal = self.get_subtotal_price()

        return float(subtotal) + float(newprice)



    def clear(self):
        # Remove cart from session
        for key in [settings.BASKET_SESSION_ID, "purchase"]:
            del self.session[key]
            
        self.save()

    def save(self):
        self.session.modified = True
    