import sys
from typing import Any
import click
from click.exceptions import Abort
import photo_scanner.utils.message as msg


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
           **kwargs: Any) -> Any:
    try:
        styled_text = click.style(text, fg=fg)
        return click.prompt(styled_text,
                            show_default=False,
                            **kwargs)
    except Abort:
        failure(' QUIT')
        sys.exit(0)


def prompt_default_accept(text: str,
                          **kwargs: Any) -> bool:
    '''
    press <any key> + <Enter>: False
    press <Enter>: False
    press N + <Enter>: True
    '''
    try:
        ans = prompt(text,
                     fg='cyan',
                     default='Y',
                     prompt_suffix=click.style(' ([Y]/n) '),
                     **kwargs)
        # user specificially reject to yield Positive
        choice = str(ans).upper() == 'N'
        return choice
    except Exception as e:
        # default yield True to break while loop
        msg.failure(str(e))
        return True


def prompt_default_reject(text: str,
                          **kwargs: Any) -> bool:
    '''
    press <any key> + <Enter>: True
    press <Enter>: True
    press Y + <Enter>: False
    '''
    try:
        ans = prompt(text,
                     fg='cyan',
                     default='N',
                     prompt_suffix=click.style(' (y/[N]) '),
                     **kwargs)
        # user specificially reject to yield Negative
        choice = str(ans).upper() != 'Y'
        return choice
    except Exception as e:
        # default yield True to break while loop
        msg.failure(str(e))
        return True
