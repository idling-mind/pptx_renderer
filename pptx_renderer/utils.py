def para_text_replace(para, find_string, replace_string):
    """Function to replace text in a paragraph

    This function replaces text in a paragraph while respecting the formatting.

    Args:
        para (pptx.shapes.paragraph.Paragraph): Paragraph to replace text in.
        find_string (str): String to find in the paragraph.
        replace_string (str): String to replace the find_string with.

    Returns:
        None
    """
    find_string = str(find_string)
    replace_string = str(replace_string)
    starting_pos = para.text.find(find_string)
    if starting_pos == -1:
        return  # text not in paragraph
    txt_prev = ""
    for run in para.runs:
        if len(txt_prev) <= starting_pos < len(txt_prev) + len(run.text):
            if run.text.find(find_string) != -1:  # text in run, replace
                run.text = run.text.replace(find_string, replace_string)
                return
            else:  # text no in "run"
                txt_prev = txt_prev + run.text
                run.text = run.text[: starting_pos - len(txt_prev)] + replace_string
        elif starting_pos < len(txt_prev) and starting_pos + len(find_string) >= len(
            txt_prev
        ) + len(run.text):
            txt_prev = txt_prev + run.text
            run.text = ""
        elif (
            len(txt_prev)
            < starting_pos + len(find_string)
            < len(txt_prev) + len(run.text)
        ):
            txt_prev = txt_prev + run.text
            run.text = run.text[starting_pos + len(find_string) - len(txt_prev) :]
        else:
            txt_prev += run.text


def fix_quotes(input_string: str) -> str:
    """Replace unicode quotes (inserted by powerpoint) with ascii quotes.

    Args:
        input_string (str): String to fix quotes in.
    
    Returns:
        str: String with fixed quotes.
    """
    return (
        input_string.replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
    )
