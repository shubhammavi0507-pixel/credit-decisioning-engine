from pathlib import Path
import json
from pdf_extractor import PDFExtractor

class DataPipeline:

    def __init__(self):
        self.extractor = PDFExtractor()

    def process_pdf(self, pdf_path: Path, output_path: Path):

        extracted = self.extractor.extract_from_pdf(pdf_path)

        financials = self.extractor.extract_financial_values(extracted)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(financials, f, indent=2)

        return financials
