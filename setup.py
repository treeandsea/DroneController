"""
Sets up the project with all the meta information.
"""
from setuptools import setup

setup(
    name='DroneController',
    version='0.1.0',
    packages=['src', 'src.drone_controller', 'test'],
    url='https://www.github.com/treeandsea/DroneController',
    license='GPL-3.0',
    author='Segelzwerg, TreeKid',
    author_email='marcel.haas@hhu.de',
    description='A python module that calculates thrusts for various aircrafts from all sorts of '
                'inputs. '
)
