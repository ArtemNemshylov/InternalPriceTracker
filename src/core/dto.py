from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductDTO:
    name: str
    price: float
    available: bool
    discount: int
