""" Setup file for the python_client package. """
from setuptools import setup, find_packages

setup(
    name='client_python',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'requests',
    ]
)
