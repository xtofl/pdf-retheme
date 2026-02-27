#!/usr/bin/env python3
"""Convert a PDF to black text on white background."""

import sys
from pathlib import Path
import io

import fitz  # PyMuPDF
from PIL import Image
import typer

cli = typer.Typer()


@cli.command()
def convert_to_bw(input_path: str, output_path: str, dpi: int = 150) -> None:
    """Convert PDF to black text on white background."""
    doc = fitz.open(input_path)
    output_doc = fitz.open()

    total_pages = len(doc)

    for page_num in range(total_pages):
        print(f"Processing page {page_num + 1}/{total_pages}...")

        page = doc[page_num]

        # Render page to image
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)

        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Convert to grayscale then threshold to pure black/white
        gray = img.convert("L")
        # Threshold: pixels brighter than 200 become black, rest becomes white
        bw = gray.point(lambda x: 0 if x > 200 else 255, "1")

        # Save as 1-bit black/white with TIFF format and CCITT Group 4 compression
        # This is the most efficient compression for black/white documents
        img_bytes = io.BytesIO()
        bw.save(img_bytes, format="TIFF", compression="group4")
        img_bytes.seek(0)

        # Create new page with same dimensions
        new_page = output_doc.new_page(
            width=page.rect.width,
            height=page.rect.height
        )

        # Insert the processed image
        new_page.insert_image(new_page.rect, stream=img_bytes.read())

    # Save with compression and optimization
    output_doc.save(
        output_path,
        garbage=4,  # Maximum garbage collection
        deflate=True,  # Compress content streams
        clean=True,  # Clean unused objects
    )
    output_doc.close()
    doc.close()

    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    cli()
