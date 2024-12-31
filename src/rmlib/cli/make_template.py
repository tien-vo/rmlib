import os
import subprocess
from os.path import basename, splitext

import click
import fitz

from rmlib.io import WORK_DIR


def compile_pdf():
    src_dir = WORK_DIR / "templates" / "src"
    for tex_file in src_dir.iterdir():
        if not tex_file.match("*.tex"):
            continue

        output = subprocess.run(["tectonic", "-c", "minimal", tex_file])
        if output.returncode != 0:
            continue

    pdf_list = []
    for file in src_dir.iterdir():
        if not file.match("*.pdf"):
            continue

        pdf_list.append(file)

    return pdf_list


def process_pdf(file: os.PathLike, width=1872, height=1404, landscape=False):
    base_name = splitext(basename(file))[0]
    page = fitz.open(file)[0]
    rect = page.rect
    if landscape:
        rotation = -90
    else:
        rotation = 0

    # ---- Calculate cropbox
    if landscape:
        rotation = -90
        zoom_factor = width / rect.width
        crop_height = height / zoom_factor
        offset = (rect.height - crop_height) / 2
        crop = fitz.Rect(0, offset, rect.width, offset + crop_height)
    else:
        width, height = height, width
        rotation = 0
        zoom_factor = height / rect.height
        crop_width = width / zoom_factor
        offset = (rect.width - crop_width) / 2
        crop = fitz.Rect(offset, 0, offset + crop_width, rect.height)
    page.set_cropbox(crop)
    page.set_rotation(rotation)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))

    pix.save(save_name := WORK_DIR / "templates" / f"{base_name}.png")
    os.remove(file)
    return save_name


@click.command
def make_template():
    for pdf in compile_pdf():
        process_pdf(pdf)
