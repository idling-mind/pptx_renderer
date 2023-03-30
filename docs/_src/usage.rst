Using PPTXRenderer
==================

PPTXRenderer allows you to write python code inside a presentation and execute
it like a script. The output is rendered as a new presentation. You can use the
following types of python code inside the input template.

Simple python expressions
-------------------------

You can write simple python expressions inside any text field which gets evaluated
at render time.

For example, you can write ``{{{5.566*3.456}}}`` or ``{{{sum([1123, 123, 123, 4])}}}``


Substituting variable values and function results
-------------------------------------------------

You can write expressions like ``{{{variable_name}}}`` or function call like
``{{{my_function("arg")}}}`` in the presentation. These variables and functions
should be passed in as arguments to the render function.

For example:

If there is a template ppt which contains ``{{{my_variable}}}`` in a text box,
and there is a function call ``{{{calculate_square(my_variable)}}}`` in another
(or same) text box.  You can pass in the input like below.

.. code-block:: python

   from pptx_renderer import PPTXRenderer
   p = PPTXRenderer("template.pptx")

   def sqr(input):
       return input*input

   p.render(
      "output.pptx", 
      {
         "my_variable": 100,
         "calculate_square": sqr
      }
   )


Inserting images
----------------

You can replace shape placeholders with images using ``PPTXRenderer``.
To insert an image, create a rectangle shape which will define where the image
should be placed and the boundaries of the image. Then insert a placeholder
text in the format ``{{{path_to_image:image()}}}`` where ``path_to_image`` is a variable
whose value is the path to the image to be inserted.

As you can see, ``image`` is a function. You can pass in the following arguments
to the function. All of these are optional.

* | ``preserve_aspect_ratio``: If set to ``True``, the image will be resized to fit
  | the shape. If set to ``False``, the image will be stretched to fit the shape.
  | Default is ``True``.
* | ``remove_shape``: If set to ``True``, the shape will be removed after the image
  | is inserted. Default is ``True``.
* | ``horizontal_alignment``: The horizontal alignment of the image inside the shape.
  | Can be one of ``left``, ``center``, ``right``. Default is ``left``.
* | ``vertical_alignment``: The vertical alignment of the image inside the shape.
  | Can be one of ``top``, ``center``, ``bottom``. Default is ``top``.

Inserting Videos
----------------

Insert a video in the same height and width as the shape. The placeholder
should evaluate to a path to the video file. The placeholder should be specified
as ``{{{path_to_video:video()}}}``.

* | ``remove_shape``: If set to ``True``, the shape will be removed after the image
  | is inserted. Default is ``True``.


Inserting tables
----------------

Similar to images, you can replace shape placeholders with tables.
To create a table, create a rectangle shape which will define where the table
should be placed. Then insert a placeholder text in the format 
``{{{table_data:table()}}}`` where ``table_data`` is a variable whose value is a
list of lists. Just like ``image``, ``table`` is also a function. You can pass
in the following arguments to the function. All of these are optional.

* | ``first_row``: If set to ``True``, the first row of the table will be treated
  | as the header row. Default is ``True``.
* | ``first_column``: If set to ``True``, the first column of the table will be
  | treated as the header column. Default is ``False``.
* | ``last_row``: If set to ``True``, the last row of the table will be treated
  | as the footer row. Default is ``False``.
* |  ``last_column``: If set to ``True``, the last column of the table will be
  |  treated as the footer column. Default is ``False``.
* |  ``horizontal_banding``: If set to ``True``, the table will have horizontal
  |  banding. Default is ``True``.
* |  ``vertical_banding``: If set to ``True``, the table will have vertical
  |  banding. Default is ``False``.
* |  ``remove_shape``: If set to ``True``, the shape will be removed after the table
  |  is inserted. Default is ``True``.



Writing code in notes
---------------------

Apart from using python expressions inside text boxes, you can write more
elaborate code inside the slide notes surrounded by triple back ticks followed
by ``python`` keyword as shown below.

.. code-block::

   ```python
   # python code
   ```

The code inside this block will get executed before the slide is evaluated.
So, for example, you can define a function side the notes like below.

.. code-block::

   ```python
   def doubler(input):
      return input*input
   ```

Then you can write ``{{{doubler(100)}}}`` inside one of the text boxes in the same
slide or any slide which comes after this slide.

Custom plugins
--------------
The ``image`` and ``table`` functions are implemented as plugins. You can write
your own plugins and use them in the presentation. To write a plugin, do the
following steps

1. | Create a plugin function: Create a function which accepts one or more
   | arguments. The first argument will be the a dictionary containing the
   | following key, value pairs.

* | ``result``: The result of the expression which was evaluated inside the
  | placeholder text. For example, if the placeholder text is ``{{{5*6}}}``,
  | the result will be ``30``.
* ``shape``: The shape object where the placeholder was found.
* ``slide``: The slide object where the shape was found.
* ``slide_no``: The slide number where the shape was found. (First slide is 0)
* ``presentation``: The presentation object where the slide was found.

The rest of the arguments will be passed in as arguments to the plugin function
during execution.

For example, the ``image`` plugin function's signature is as follows.

.. code-block:: python

  def image(
    context,
    preserve_aspect_ratio=True,
    remove_shape=True,
    horizontal_alignment="left",
    vertical_alignment="top",
  )

and an example usage is as follows.

.. code-block:: python

  {{{path_to_image:image(preserve_aspect_ratio=True, horizontal_alignment="center")}}}


2. | Register the plugin: Register the plugin function using the ``register_plugin``
   | method of the ``PPTXRenderer`` class. The first argument to this method is the
   | name of the plugin. The second argument is the plugin function.

.. code-block:: python

  from pptx_renderer import PPTXRenderer
  p = PPTXRenderer("template.pptx")

  def multiplier(context, factor):
    """This is a plugin function which multiplies the input by a factor
    and sets the text of the shape to the result."""
    shape = context["shape"]
    result = context["result"]
    shape.text = str(result * factor)

  p.register_plugin("multiplier", multiplier)

  p.render(
    "output.pptx", 
    {
      "my_variable": 100,
    }
  )

Now you can use the plugin ``multiplier`` in the presentation like below.

.. code-block:: python

  {{{my_variable:multiplier(10)}}}