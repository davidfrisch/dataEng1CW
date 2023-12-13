""" Setup file for the pipeline package. """
from setuptools import setup, find_packages

setup(
    name='pipeline',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'biopython',
        'boto3',
        'sqlalchemy',
        'psycopg2-binary',
        'sqlalchemy_utils',
        'python-dotenv',
        'pyspark',
        'torch',
        'flask',
        'flask-cors',
        'gunicorn',
        'requests',
    ]
)
