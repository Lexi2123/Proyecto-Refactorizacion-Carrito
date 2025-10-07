from models import Cart, BigOrderDiscount
from services import OrderCalculator, OrderService
from implementations import JSONOrderRepository, ConsoleReceiptPrinter

if __name__ == '__main__':
    # === Configuración e Inyección de Dependencias (DIP/OCP) ===
    
    # 1. Elegir estrategia de descuento (fácilmente intercambiable)
    descuento_strategy = BigOrderDiscount() 

    # 2. Configurar el Calculador con la estrategia elegida
    calculator = OrderCalculator(discount_strategy=descuento_strategy)

    # 3. Configurar Implementaciones de I/O (fácilmente intercambiables)
    repo = JSONOrderRepository()
    printer = ConsoleReceiptPrinter()

    # 4. Configurar el Servicio Coordinador inyectando las dependencias
    order_service = OrderService(calculator=calculator, repository=repo, printer=printer)

    # --- Uso del Sistema TO BE ---
    cart = Cart(user_id=200)
    cart.add_item("Producto A", 50.00, 3) # Total > 100 para activar descuento
    
    print("\n--- INICIANDO CHECKOUT TO BE ---")
    order_service.checkout(cart, "Efectivo")
