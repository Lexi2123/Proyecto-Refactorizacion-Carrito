from abc import ABC, abstractmethod

# Abstracción para Persistencia (DIP)
class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order_data: dict):
        pass

# Abstracción para Output (DIP)
class IReceiptPrinter(ABC):
    @abstractmethod
    def print_receipt(self, order_data: dict, total: float):
        pass

# Abstracción para Descuentos (OCP)
class IDiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, subtotal: float) -> float:
        pass
