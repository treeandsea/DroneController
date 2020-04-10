"""
Sets up the project with all the meta information.
"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='DroneController',
    version='1.1.0',
    packages=find_packages(),
    keywords='drone flying controller aviation',
    url='https://www.github.com/treeandsea/DroneController',
    download_url='https://github.com/treeandsea/DroneController/releases',
    license='GPL-3.0',
    author='Segelzwerg, TreeKid',
    author_email='marcel.haas@hhu.de',
    description='A python module that calculates thrusts for various aircrafts from all sorts of '
                'inputs. ',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',

    install_requires='numpy',
)
