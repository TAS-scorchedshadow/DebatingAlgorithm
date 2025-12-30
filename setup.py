"""
Setup script for debate-algorithm package.

This allows the package to be installed with: pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="debate-algorithm",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "inquirer>=3.0.0",
    ],
    python_requires=">=3.8",
)
