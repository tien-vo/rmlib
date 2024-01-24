import os
import subprocess
from os.path import splitext, basename

import click
import fitz

from rmlib.io import WORK_DIR


def compile_pdf():
    src_dir = WORK_DIR / "templates" / "src"
    for tex_file in src_dir.iterdir():
        if not tex_file.match("*.tex"):
            continue

        output = subprocess.run(["tectonic", tex_file])
        if output.returncode != 0:
            continue

    pdf_list = []
    for file in src_dir.iterdir():
        if not file.match("*.pdf"):
            continue

        pdf_list.append(file)

    return pdf_list


def process_pdf(file: os.PathLike, width=1872, height=1404):
    base_name = splitext(basename(file))[0]
    page = fitz.open(file)[0]
    rect = page.rect

    # ---- Calculate cropbox
    zoom_factor = width / rect.width
    crop_height = height / zoom_factor
    offset = (rect.height - crop_height) / 2
    page.set_cropbox(fitz.Rect(0, offset, rect.width, offset + crop_height))
    page.set_rotation(-90)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))

    pix.save(WORK_DIR / "templates" / f"{base_name}.png")
    os.remove(file)


@click.command
def make_template():
    for pdf in compile_pdf():
        process_pdf(pdf)
