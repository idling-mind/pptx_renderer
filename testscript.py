from pathlib import Path
from pptx_renderer import PPTXRenderer

p = PPTXRenderer("newtemplate.pptx")

someval = "hello"


def mymethod(abc):
    return f"{abc} " * 5


myimage = Path("docs/_src/_static/is_it_worth_the_time.png")
mytable = [["a", "b", "c", "d", "e"]] * 10
p.render(
    "output.pptx",
    {
        "heading": "This is a heading",
        "title": "This is a title",
        "myimage": myimage,
    },
    loop_groups=[{"start": 3, "end": 3, "var": "i", "iterable": range(5)}],
)
