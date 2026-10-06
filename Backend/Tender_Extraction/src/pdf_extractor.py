from pathlib import Path
from typing import Any

import pymupdf


class PDFExtractionError(Exception):
    """Raised when PDF extraction fails."""


class PDFExtractor:
    """
    Extracts text, text blocks, and tables from a PDF.

    The extractor preserves page-level information so that every
    extracted item can later be traced back to its source page.
    """

    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Expected a PDF file, got: {self.pdf_path.suffix}"
            )

    def extract(self) -> dict[str, Any]:
        """
        Extract complete document information.

        Returns:
            {
                "file_name": str,
                "page_count": int,
                "pages": [...]
            }
        """

        try:
            document = pymupdf.open(self.pdf_path)

            result = {
                "file_name": self.pdf_path.name,
                "page_count": len(document),
                "pages": []
            }

            for page_index, page in enumerate(document):
                page_data = self._extract_page(
                    page,
                    page_index + 1
                )

                result["pages"].append(page_data)

            document.close()

            return result

        except Exception as exc:
            raise PDFExtractionError(
                f"Failed to extract PDF '{self.pdf_path}': {exc}"
            ) from exc

    def _extract_page(
        self,
        page: pymupdf.Page,
        page_number: int
    ) -> dict[str, Any]:
        """Extract all supported information from one page."""

        text = self._extract_text(page)
        blocks = self._extract_blocks(page)
        tables = self._extract_tables(page)

        return {
            "page": page_number,
            "text": text,
            "blocks": blocks,
            "tables": tables
        }

    @staticmethod
    def _extract_text(page: pymupdf.Page) -> str:
        """
        Extract page text while preserving natural reading order
        as much as possible.
        """

        return page.get_text(
            "text",
            sort=True
        ).strip()

    @staticmethod
    def _extract_blocks(page: pymupdf.Page) -> list[dict[str, Any]]:
        """
        Extract text blocks together with their coordinates.

        Coordinates are useful later for:
        - heading detection
        - reading order
        - table/layout analysis
        - header/footer detection
        """

        raw_blocks = page.get_text(
            "blocks",
            sort=True
        )

        blocks = []

        for block_id, block in enumerate(raw_blocks):
            if len(block) < 5:
                continue

            x0, y0, x1, y1, text = block[:5]

            if not text.strip():
                continue

            blocks.append({
                "block_id": block_id,
                "bbox": {
                    "x0": round(x0, 2),
                    "y0": round(y0, 2),
                    "x1": round(x1, 2),
                    "y1": round(y1, 2)
                },
                "text": text.strip()
            })

        return blocks

    @staticmethod
    def _extract_tables(page: pymupdf.Page) -> list[dict[str, Any]]:
        """
        Extract tables using PyMuPDF's table detection.

        If table detection is unavailable or fails for a particular
        page, return an empty list instead of failing the entire PDF.
        """

        tables = []

        try:
            if not hasattr(page, "find_tables"):
                return tables

            table_finder = page.find_tables()

            for table_id, table in enumerate(
                table_finder.tables
            ):
                extracted = table.extract()

                if not extracted:
                    continue

                rows = []

                for row in extracted:
                    rows.append([
                        cell.strip() if isinstance(cell, str) else cell
                        for cell in row
                    ])

                tables.append({
                    "table_id": table_id,
                    "bbox": {
                        "x0": round(table.bbox[0], 2),
                        "y0": round(table.bbox[1], 2),
                        "x1": round(table.bbox[2], 2),
                        "y1": round(table.bbox[3], 2)
                    },
                    "rows": rows
                })

        except Exception:
            # Table extraction failure should not stop text extraction.
            return tables

        return tables