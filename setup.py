from setuptools import setup, find_packages

setup(
    name="proxin",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "proxin=proxin.main:main",
        ],
    },
)