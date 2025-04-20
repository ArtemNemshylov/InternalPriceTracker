from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductDTO:
    name: str
    price: float
    available: bool
    url: str
    image_url: str
    discount: Optional[float] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    composition: Optional[str] = None
