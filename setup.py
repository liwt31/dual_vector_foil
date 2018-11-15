#!/usr/bin/env python
import os
from setuptools import setup, find_packages


long_description = open(os.path.join(os.path.dirname(__file__), "README.md")).read()


setup(
    name="dvf",
    author="liwt31",
    author_email="liwt31@163.com",
    version="0.1.2",
    license="MIT",
    url="https://github.com/liwt31/dual_vector_foil",
    description="A dual vector foil (二向箔) that squashes any Python objects into your console.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("."),
    install_requires=["print_tree2", "colorama", "termcolor"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
)
