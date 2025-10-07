from datetime import datetime
from models import Cart
from abstractions import IOrderRepository, IReceiptPrinter, IDiscountStrategy

# Clase OrderCalculator (Responsabilidad Única: Lógica Financiera)
class OrderCalculator:
    # CC = 1 (bajo)
    def __init__(self, discount_strategy: IDiscountStrategy, tax_rate: float = 0.15):
        self.discount_strategy = discount_strategy
        self.tax_rate = tax_rate
        
    def calculate_final_total(self, items: list) -> float:
        subtotal = sum(item['price'] * item['quantity'] for item in items)
        
        # OCP: Usa la abstracción inyectada
        discounted_subtotal = self.discount_strategy.apply_discount(subtotal)
        
        return discounted_subtotal * (1 + self.tax_rate)

# Clase OrderService (Responsabilidad Única: Coordinación, DIP aplicado)
class OrderService:
    # CC = 1 (bajo)
    def __init__(self, calculator: OrderCalculator, repository: IOrderRepository, printer: IReceiptPrinter):
        # Inversión de Dependencias (DIP): Depende de abstracciones
        self.calculator = calculator
        self.repository = repository
        self.printer = printer
        
    def checkout(self, cart: Cart, payment_method: str):
        if not cart.get_items():
            return False

        final_total = self.calculator.calculate_final_total(cart.get_items())
        
        order_data = {
            "order_id": str(cart.user_id) + "-" + datetime.now().strftime("%Y%m%d%H%M%S"),
            "user_id": cart.user_id,
            "total": final_total,
            "payment": payment_method
        }
        
        # Uso de la Abstracción
        self.repository.save(order_data)
        self.printer.print_receipt(order_data, final_total)
        
        return True
