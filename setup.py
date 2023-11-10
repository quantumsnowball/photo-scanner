from setuptools import setup

setup(
    name='photo-scanner',
    version='0.1.0',
    description='photo-scanner - convert printed photos into digital format',
    url='https://github.com/quantumsnowball/photo-scanner',
    author='Quantum Snowball',
    author_email='quantum.snowball@gmail.com',
    license='MIT',
    packages=['photo_scanner'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'photo-scanner=photo_scanner.cli:photo_scanner',
        ]
    }
)
