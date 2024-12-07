# PPTX Renderer

This package let's you run your powerpoint presentations like a jupyter-notebook.
You can insert placeholders in the ppt and also write python code in the ppt's
notes and use either a python function or an equivalent commandline tool to
convert it into an output rendered presentation.

## Installation
```console
pip install pptx-renderer
```

## Usage
Below is a simple example.

```python
from pptx_renderer import PPTXRenderer
p = PPTXRenderer("template.pptx")

someval = "hello"
def mymethod(abc):
    return f"{abc} " * 5

myimage = r"is_it_worth_the_time.png"
mytable = [["a", "b", "c", "d", "e"]] * 10
p.render(
    "output.pptx", 
    {
        "someval": someval, "mymethod": mymethod, "myimage": myimage,
        "mytable": mytable,
    }
)
```

This will convert this

![Before](docs/_src/_static/before.png)

to this.

![After](docs/_src/_static/after.png)


You can define some functions within the ppt itself by writing python code in
the notes section of slides. And the variables and functions in this code
can be used in the main ppt.

For example: write the following in one of the slide's notes.

<pre>
```python
def myfunc(input):
    return input * 42
```
</pre>

Now you can, for example, add the placeholder `{{{myfunc(42)}}}` in your slides.


If the template ppt is a self contained python script ie: if it does not require
variable values and function definition to be passed from outside, you can
generate the output ppt directly from the commandline using the following
command.

```console
pptx-renderer input_template.pptx output_file.pptx
```

## Placeholders
You can have placeholders for text, image or a table. Placeholders can be added
inside text boxes and shapes. All placeholders should be enclosed within a pair
of triple braces (`{{{` and `}}}`).

### Text
Any placeholder which can be evaluated into a string can act as a text placeholder.

For example: `{{{"hello " * 10/2}}}` or `{{{abs(-2)}}}`

### Image
if you have added `:image()` as a suffix to the python statement, the renderer will
try to convert the value of python statement to a file location and insert an
image from that file location.

For example: `{{{"c:\temp\myimage.png":image()}}}`

### Table
Tables are similar to images, but only that instead of a string, the python
statement should evaluate to a list of lists. Then you can add `:table()` as a
suffix and it will be convert to a table inside the ppt.

For example: `{{{[["col1", "col2", "col3"],[1, 2, 3]]:table()}}}` will render to

|col1 | col2 | col3|
|-----|------|-----|
|1    |2     |3    |

## Code in slide notes
You can write regular python code in the slide notes but enclosed between
`` ```python `` and `` ``` ``.

For example: Create a new pptx and write the following in the first slide's notes

<pre lang="python">
```python
import numpy as np
myarr = np.array([[1, 2], [3, 4]])
```
</pre>

And in the slide, create a rectangluar shape and add the text `{{{myarr:table()}}}`
and a text box with the text `The determinant of the array is {{{np.linalg.det(myarr)}}}`

## Repeating slides

If you define `loop_groups` keyword argument as part of render method, you can
repeat groups of slides. The value of `loop_groups` should be a list of dictionaries.
Each dictionary should have the following keys
- `start`: The slide number where the loop should start
- `end`: The slide number where the loop should end
- `iterable`: The iterable which should be looped over.
- `variable`: The name of the variable which will be available inside the loop.

For example, if you want to insert all images from a folder into a ppt, one image
per slide, you can do the following.

Create a template ppt with a single slide which contains a rectangle shape where
the image should be inserted. Then insert a placeholder text in the format
`{{{path_to_image:image()}}}` inside the shape. Then you can use the following

```python
from pathlib import Path
from pptx_renderer import PPTXRenderer
p = PPTXRenderer("template.pptx")

images = Path("path/to/images").glob("*.png")
loop_groups = [
    {
        "start": 0,
        "end": 0,
        "iterable": images,
        "variable": "path_to_image"
    }
]

p.render(
    "output.pptx",
    loop_groups = loop_groups
)
```

This will create a new ppt with each image from the folder inserted into a new slide.
