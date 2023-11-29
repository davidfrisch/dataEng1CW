""" Setup file for the pipeline package. """
from setuptools import setup, find_packages

setup(
    name='comp0235_pipeline',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'biopython',
        'boto3',
        'sqlalchemy',
        'python-dotenv',
        'pyspark',
        'torch',
    ]
)
