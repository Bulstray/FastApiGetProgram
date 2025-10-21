from typer import Typer

from .tokens import app as token_app

app = Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.callback()
def callback() -> None:
    """
    Some ClI management commands
    """


app.add_typer(token_app)
