from pathlib import Path
from typing import Any
from logging import warning
from PIL import Image
from .exceptions import RenderError


def image(
    context: dict,
    preserve_aspect_ratio=True,
    remove_shape=True,
    horizontal_alignment="left",
    vertical_alignment="top",
):
    result = str(context["result"])
    slide = context["slide"]
    shape = context["shape"]
    if not Path(result).exists():
        raise RenderError(f"Image '{result}' not found.")
    with Image.open(result) as img:
        im_width, im_height = img.size
    ar_image = im_width / im_height
    ar_shape = shape.width / shape.height
    if not preserve_aspect_ratio:
        width = shape.width
        height = shape.height
    elif ar_image >= ar_shape:
        width = shape.width
        height = shape.width / ar_image
    else:
        width = shape.height * ar_image
        height = shape.height
    if horizontal_alignment == "left":
        left = shape.left
    elif horizontal_alignment == "center":
        left = shape.left + (shape.width - width) / 2
    elif horizontal_alignment == "right":
        left = shape.left + shape.width - width
    if vertical_alignment == "top":
        top = shape.top
    elif vertical_alignment == "center":
        top = shape.top + (shape.height - height) / 2
    elif vertical_alignment == "bottom":
        top = shape.top + shape.height - height
    slide.shapes.add_picture(
        result,
        left,
        top,
        width,
        height,
    )
    # Delete the shape after image is inserted
    if remove_shape:
        sp = shape._sp
        sp.getparent().remove(sp)


def video(
    context: dict,
    preserve_aspect_ratio=True,
    remove_shape=True,
    horizontal_alignment="left",
    vertical_alignment="top",
    poster_image=None,
    mime_type="video/mp4",
):
    result = str(context["result"])
    slide = context["slide"]
    shape = context["shape"]
    if not Path(result).exists():
        raise RenderError(f"Image '{result}' not found.")
    with Image.open(result) as img:
        im_width, im_height = img.size
    ar_image = im_width / im_height
    ar_shape = shape.width / shape.height
    if not preserve_aspect_ratio:
        width = shape.width
        height = shape.height
    elif ar_image >= ar_shape:
        width = shape.width
        height = shape.width / ar_image
    else:
        width = shape.height * ar_image
        height = shape.height
    if horizontal_alignment == "left":
        left = shape.left
    elif horizontal_alignment == "center":
        left = shape.left + (shape.width - width) / 2
    elif horizontal_alignment == "right":
        left = shape.left + shape.width - width
    if vertical_alignment == "top":
        top = shape.top
    elif vertical_alignment == "center":
        top = shape.top + (shape.height - height) / 2
    elif vertical_alignment == "bottom":
        top = shape.top + shape.height - height
    slide.shapes.add_movie(
        result,
        left,
        top,
        width,
        height,
        poster_frame_image=poster_image,
        mime_type=mime_type,
    )
    # Delete the shape after image is inserted
    if remove_shape:
        sp = shape._sp
        sp.getparent().remove(sp)


def table(
    context: dict,
    first_row=True,
    first_col=False,
    last_row=False,
    last_col=False,
    horizontal_banding=True,
    vertical_banding=False,
    remove_shape=True,
):
    result = context["result"]
    shape = context["shape"]
    slide = context["slide"]
    all_rows = list(result)
    first_row_list = list(all_rows[0])
    table_shape = slide.shapes.add_table(
        len(all_rows),
        len(first_row_list),
        shape.left,
        shape.top,
        shape.width,
        shape.height,
    )
    table_shape.table.first_row = first_row
    table_shape.table.first_col = first_col
    table_shape.table.last_row = last_row
    table_shape.table.last_col = last_col
    table_shape.table.horz_banding = horizontal_banding
    table_shape.table.vert_banding = vertical_banding

    for row, row_data in enumerate(result):
        for col, val in enumerate(row_data):
            table_shape.table.cell(row, col).text = str(val)
    if remove_shape:
        sp = shape._sp
        sp.getparent().remove(sp)
