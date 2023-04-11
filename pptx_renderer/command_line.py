import json
from pathlib import Path
import click
from pptx_renderer import PPTXRenderer


@click.command()
@click.argument("template_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
@click.option(
    "--fail_on_error",
    is_flag=True,
    help="By default, the renderer will not stop when it encouters an error while"
    " rendering a placeholder. Setting this flag will cause it to stop at the"
    " first error.",
)
@click.option(
    "-i",
    "--input",
    type=click.Path(exists=True),
    help=(
        "Path to a json file with key value pairs of variables used in the template"
    ),
)
def main(template_path, output_path, fail_on_error, input):
    """Generate a powerpoint presentation from a template

    TEMPLATE_PATH: Path to the template file with placeholders

    OUTPUT_PATH: Path to the rendered output ppt
    """
    if input:
        input = Path(input)
    p = PPTXRenderer(template_path)
    extra_variables = json.loads(input.read_text()) if input else {}
    p.namespace.update(extra_variables)
    p.render(output_path, {}, skip_failed=not (fail_on_error))


if __name__ == "__main__":
    main()
