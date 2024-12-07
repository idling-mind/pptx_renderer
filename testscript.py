from pathlib import Path
from pptx_renderer import PPTXRenderer

p = PPTXRenderer("template.pptx")

someval = "hello"


def mymethod(abc):
    return f"{abc} " * 5


myimage = Path("docs/_src/_static/is_it_worth_the_time.png")
mytable = [["a", "b", "c", "d", "e"]] * 10
p.render(
    "output.pptx",
    {
        "someval": someval,
        "mymethod": mymethod,
        "myimage": myimage,
        "mytable": mytable,
    },
)
