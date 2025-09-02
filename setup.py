"""
Setup configuration for the NACEConverter package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NACEConverter",  # Using the same name as your module
    version="1.0.1",
    author="Jakob Alexandersen",
    author_email="jakob.alexandersen@fsncapital.com",
    description="A Python package for converting NACE codes to descriptions and searching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexandersen01/nace-converter-py",
    packages=["naceconverter"],  # Package directory
    package_data={"naceconverter": ["*.csv"]},  # Include CSV files
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
    keywords="nace codes economic activities classification converter europe",
)
