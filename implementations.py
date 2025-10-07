from abstractions import IOrderRepository, IReceiptPrinter

# Implementación de Persistencia (DIP)
class JSONOrderRepository(IOrderRepository):
    # CC = 1 (bajo)
    def save(self, order_data: dict):
        # Lógica específica de guardado en JSON (puede ser SQL, MongoDB, etc.)
        print(f"✅ Guardando la orden {order_data['user_id']} en JSON.")

# Implementación de Output (DIP)
class ConsoleReceiptPrinter(IReceiptPrinter):
    # CC = 1 (bajo)
    def print_receipt(self, order_data: dict, total: float):
        # Lógica específica de impresión a la consola
        print("\n========================================")
        print(f"RECIBO GENERADO - Usuario: {order_data['user_id']}")
        print(f"TOTAL FINAL (TO BE): ${total:.2f}")
        print("========================================")
