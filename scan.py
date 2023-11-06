import subprocess


NAME = '.raw.jpg'
EXE = r'/mnt/c/Program Files/NAPS2/NAPS2.Console.exe'
PROFILE = 'jpg300'


def scan(savename: str,
         exe: str = EXE,
         profile: str = PROFILE,) -> None:
    '''
    scan using NAPS2 console executable
    '''
    # cmd
    cmd = [exe, '-p', profile, '-o', savename, '--progress', '--force']

    # run
    _ = subprocess.run(cmd)


if __name__ == '__main__':
    name = input('Output file name? ')
    scan(name)
