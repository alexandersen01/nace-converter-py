"""
Setup configuration for the naceconverter package.
"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="naceconverter",
    version="1.0.0",
    author="Jakob Alexandersen",
    author_email="jakob.alexandersen@fsncapital.com",
    description="A Python package for converting NACE codes to descriptions and searching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/naceconverter",
    py_modules=['NACEConverter', '__init__'],
    package_data={
        '': ['nacecodes.csv'],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    keywords="nace codes economic activities classification converter europe",
)