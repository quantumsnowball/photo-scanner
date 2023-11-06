import subprocess


EXECUTABLE = r'/mnt/c/Program Files/NAPS2/NAPS2.Console.exe'
PROFILE = 'fast'

output = input('Output file name? ')
cmd = [EXECUTABLE, '-p', PROFILE, '-o', output, ]

result = subprocess.run(cmd)
