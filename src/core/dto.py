from dataclasses import dataclass

@dataclass
class ProductDTO:
    article: str
    price: float
    available: bool
    discount: int
