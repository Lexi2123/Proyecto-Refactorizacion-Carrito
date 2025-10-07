import json
import os
from datetime import datetime

# Archivo de persistencia acoplada (Violación DIP)
PERSISTENCE_FILE = "orders_data.json"

class ShoppingCartManager:
    """
    Clase monolítica que maneja gestión de ítems, cálculo, persistencia y reporte.
    Viola intencionalmente los principios SOLID.
    """
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []
        self.tax_rate = 0.15 
        self.discount_applied = False
        
    # === Lógica de Gestión de Artículos (Responsabilidad 1) ===
    def add_item(self, product_name: str, price: float, quantity: int = 1):
        if price <= 0 or quantity <= 0:
            return
        self.items.append({'name': product_name, 'price': price, 'quantity': quantity})
        
    # === Lógica de Cálculo y Negocio (Responsabilidad 2 & Violación OCP) ===
    def calculate_total(self) -> float:
        # Complejidad ciclomática (CC) aumenta aquí debido al if
        subtotal = sum(item['price'] * item['quantity'] for item in self.items)
        
        # Lógica de negocio acoplada (Violación OCP: si la regla cambia, modificamos este método)
        if subtotal > 100: 
            subtotal *= 0.90 # 10% de descuento por gran compra
            self.discount_applied = True
        
        tax_amount = subtotal * self.tax_rate
        return subtotal + tax_amount

    # === Lógica de Persistencia y Output (Responsabilidad 3 & Violación DIP) ===
    def checkout_and_save(self, payment_method: str) -> bool:
        """
        Método de alto CC que mezcla Persistencia (save) y Output (receipt) (Violación SRP).
        """
        if not self.items:
            print("El carrito está vacío. Checkout abortado.")
            return False

        final_total = self.calculate_total()
        
        # 1. Persistencia: Implementación concreta (Violación DIP)
        order_data = {
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": self.user_id,
            "total": final_total,
            "payment": payment_method
        }
        self._save_order_to_json(order_data)
        
        # 2. Output: Generación del recibo en consola (Violación SRP)
        self._generate_receipt(final_total)

        return True

    def _save_order_to_json(self, data):
        """Implementación de bajo nivel de guardar en JSON, acoplada a la clase."""
        # ... Lógica de manejo de archivos ...
        if os.path.exists(PERSISTENCE_FILE):
            with open(PERSISTENCE_FILE, 'r') as f:
                orders = json.load(f)
        else:
            orders = []
            
        orders.append(data)
        
        with open(PERSISTENCE_FILE, 'w') as f:
            json.dump(orders, f, indent=4)
        print("✅ Orden guardada exitosamente en JSON.")

    def _generate_receipt(self, total: float):
        """Genera el recibo en la consola."""
        # ... Lógica de impresión a la consola ...
        print("\n========================================")
        print(f"TOTAL FINAL A PAGAR: ${total:.2f}")
        print("========================================")

if __name__ == '__main__':
    # Uso del sistema AS IS
    cart_grande = ShoppingCartManager(user_id=101)
    cart_grande.add_item("Monitor 4K", 350.00, 1)
    cart_grande.checkout_and_save("VISA")
