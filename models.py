from abstractions import IDiscountStrategy

# Clase Cart (Responsabilidad Única: Estado)
class Cart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []
        
    def add_item(self, product_name: str, price: float, quantity: int = 1):
        self.items.append({'name': product_name, 'price': price, 'quantity': quantity})

    def get_items(self):
        return self.items

# Estrategia Concreta de Descuento (OCP)
class BigOrderDiscount(IDiscountStrategy):
    def apply_discount(self, subtotal: float) -> float:
        # Complejidad Ciclomática (CC) = 2 (bajo)
        if subtotal > 100:
            return subtotal * 0.90
        return subtotal

# Estrategia Concreta de Descuento (Extensión fácil)
class VIPDiscount(IDiscountStrategy):
    def apply_discount(self, subtotal: float) -> float:
        # CC = 1 (bajo)
        return subtotal * 0.85
