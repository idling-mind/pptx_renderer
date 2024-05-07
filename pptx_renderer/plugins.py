from __future__ import annotations
from pathlib import Path
from PIL import Image
from .exceptions import RenderError


def image(
    context: dict,
    preserve_aspect_ratio: bool = True,
    remove_shape: bool = True,
    horizontal_alignment: str = "left",
    vertical_alignment: str = "top",
    crop: dict | None = None,
):
    """Insert an image into the slide at the location of the placeholder.

    Args:
        context (dict): Dictionary containing the following keys:
            - result: The result of evaluating the python statement.
            - shape: The pptx shape object where the placeholder is present.
            - slide: The pptx slide object where the placeholder is present.
            - presentation: The output pptx presentation object.
            - slide_no: The slide number where the placeholder is present.
        preserve_aspect_ratio (bool, optional): Preserve the aspect ratio of the image.
            Defaults to True.
        remove_shape (bool, optional): Remove the shape after the image is inserted.
            Defaults to True.
        horizontal_alignment (str, optional): Horizontal alignment of the image.
            Can be 'left', 'center', 'right'. Defaults to 'left'.
        vertical_alignment (str, optional): Vertical alignment of the image.
            Can be 'top', 'center', 'bottom'. Defaults to 'top'.
        crop (dict, optional): Dictionary containing the crop values for the image.
            The keys can be 'left', 'right', 'top', 'bottom'. Defaults to None.
            The values are given in percentage of the image size.
    """
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
        height = None
    else:
        width = None
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
    image = slide.shapes.add_picture(
        result,
        left,
        top,
        width,
        height,
    )
    if crop:
        image.crop_left = crop.get("left", 0)
        image.crop_right = crop.get("right", 0)
        image.crop_top = crop.get("top", 0)
        image.crop_bottom = crop.get("bottom", 0)
    # Delete the shape after image is inserted
    if remove_shape:
        sp = shape._sp
        sp.getparent().remove(sp)


def video(
    context: dict,
    poster_image=None,
    mime_type="video/mp4",
    remove_shape=True,
):
    """Insert a video into the slide at the location of the placeholder.

    Args:
        context (dict): Dictionary containing the following keys:
            - result: The result of evaluating the python statement.
            - shape: The pptx shape object where the placeholder is present.
            - slide: The pptx slide object where the placeholder is present.
            - presentation: The output pptx presentation object.
            - slide_no: The slide number where the placeholder is present.
        poster_image (str, optional): Path to the poster image for the video.
            Defaults to None.
        mime_type (str, optional): Mime type of the video. Defaults to 'video/mp4'.
        remove_shape (bool, optional): Remove the shape after the video is inserted.
            Defaults to True.
    """
    result = str(context["result"])
    slide = context["slide"]
    shape = context["shape"]
    slide.shapes.add_movie(
        result,
        shape.left,
        shape.top,
        shape.width,
        shape.height,
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
    """Insert a table into the slide at the location of the placeholder.

    Args:
        context (dict): Dictionary containing the following keys:
            - result: The result of evaluating the python statement.
            - shape: The pptx shape object where the placeholder is present.
            - slide: The pptx slide object where the placeholder is present.
            - slide_no: The slide number where the placeholder is present.
        first_row (bool, optional): Show the first row as header. Defaults to True.
        first_col (bool, optional): Show the first column as header. Defaults to False.
        last_row (bool, optional): Show the last row as footer. Defaults to False.
        last_col (bool, optional): Show the last column as footer. Defaults to False.
        horizontal_banding (bool, optional): Show horizontal banding. Defaults to True.
        vertical_banding (bool, optional): Show vertical banding. Defaults to False.
        remove_shape (bool, optional): Remove the shape after the table is inserted.
            Defaults to True.
    """
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
