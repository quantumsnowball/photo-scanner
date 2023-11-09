from typing import Any
import click


def welcome(fg: str = 'blue') -> None:
    click.secho((
        '###################################\n'
        '########## photo-scanner ##########\n'
        '###################################'
    ), fg=fg)


def success(text: str) -> None:
    click.secho(text, fg='green')


def failure(text: str) -> None:
    click.secho(text, fg='red')


def info(text: str) -> None:
    click.secho(text, fg='yellow')


def prompt(text: str,
           *,
           fg: str,
           **kwargs: Any) -> None:
    styled_text = click.style(text, fg=fg)
    return click.prompt(styled_text,
                        show_default=False,
                        **kwargs)


def prompt_default_accept(text: str,
                          **kwargs: Any) -> bool:
    try:
        ans = prompt(text,
                     fg='cyan',
                     default='Y',
                     prompt_suffix=click.style(' ([Y]/n) ', fg='cyan'),
                     **kwargs)
        # user specificially reject to yield Positive
        choice = str(ans).upper() == 'N'
        return choice
    except Exception:
        # default yield True
        return True
