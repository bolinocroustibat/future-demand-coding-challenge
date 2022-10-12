from typing import Any

import typer


class CustomLogger:
    def debug(self, message: Any):
        typer.secho(
            f"{str(message)}\n",
            fg=typer.colors.MAGENTA,
        )

    def info(self, message: Any):
        typer.secho(
            f"{str(message)}\n",
            fg=typer.colors.CYAN,
        )

    def success(self, message: Any):
        typer.secho(
            f"{str(message)}\n",
            fg=typer.colors.GREEN,
        )

    def warning(self, message: Any):
        typer.secho(
            f"{str(message)}\n",
            fg=typer.colors.YELLOW,
        )

    def error(self, message: Any):
        typer.secho(
            f"{str(message)}\n",
            fg=typer.colors.RED,
        )
