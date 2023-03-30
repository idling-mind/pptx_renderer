.. _command-line:

Running from command line
=========================

You can run the command ``pptx-renderer`` from the commandline to convert an
input template into an output presentation.

The following is the syntax of the command.

.. click:: pptx_renderer.command_line:main
    :prog: pptx-renderer
    :nested: full

Example
-------

.. code-block::

    pptx-renderer input_template.pptx output_file.pptx