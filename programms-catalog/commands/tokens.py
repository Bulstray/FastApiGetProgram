from typing import Annotated

import typer
from rich import print as rich_print
from rich.markdown import Markdown
from service.auth.redis_tokens_helper import redis_tokens as tokens

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    name="token",
    help="Tokens management",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to check",
        ),
    ],
) -> None:
    rich_print(
        (
            f"Token [bold]{token}[/bold] [green]exists[/green]"
            if tokens.token_exists(token)
            else f"{token} [red]does not exist[/red]"
        ),
    )


@app.command(name="list")
def get_tokens() -> None:
    rich_print(Markdown("# Available API Tokens"))
    rich_print(Markdown("\n- ".join(tokens.get_tokens())))
    rich_print()


@app.command()
def create() -> None:
    new_token = tokens.generate_and_save_token()
    rich_print(f"New token [bold]{new_token}[/bold] saved to db.")


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(help="The token to add"),
    ],
) -> None:
    """
    Add the provided token to db.
    """
    tokens.add_token(
        token,
    )
    rich_print(f"Token [bold]{token}[/bold] added to db.")


@app.command(name="rm")
def delete(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to delete",
        ),
    ],
) -> None:
    """
    Delete the provide token from db.
    """

    if not tokens.token_exist(token):
        rich_print(f"Token [bold]{token} [red]does not exist[/red][/bold].")
        return

    tokens.delete_token(token)
    rich_print(f"Token [bold]{token}[/bold] removed from db.")

    return
