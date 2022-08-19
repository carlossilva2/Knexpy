import os
import sys

from setuptools import find_packages, setup

if sys.argv[-1] == "build":
    os.system("python setup.py sdist")
    sys.exit()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist")
    os.system("twine upload dist/*")
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Carlos Silva",
    author_email="carlos.miguel.silva@protonmail.com",
    name="knexpy",
    description="A KnexJS like module for abstracting Python's SQLite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.1",
    url="https://github.com/carlossilva2/Knexpy",
    packages=find_packages(),
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pychalk",
    ],
    package_data={},
    project_urls={
        "Source": "https://github.com/carlossilva2/Knexpy",
        "Documentation": "https://knexpy.readthedocs.io",
    },
)
