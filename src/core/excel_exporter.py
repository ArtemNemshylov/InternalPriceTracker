from dataclasses import asdict
from typing import List
from openpyxl import Workbook
from datetime import datetime
from pathlib import Path
from src.core.dto import ProductDTO

class ExcelExporter:
    @staticmethod
    def export(products: List[ProductDTO], filename_prefix: str, output_dir: Path) -> Path:
        wb = Workbook()
        ws = wb.active
        ws.title = "Products"

        ws.append(["Артикул", "Цена", "Наличие", "Скидка", "Ссылка"])

        for product in products:
            ws.append([
                product.article,
                product.price,
                "В наличии" if product.available else "Не в наличии",
                product.discount,
                product.url
            ])

        now = datetime.now()
        filename = f"{filename_prefix}_{now.year}_{now.month:02}_{now.day:02}.xlsx"
        file_path = output_dir / filename
        wb.save(file_path)

        return file_path
