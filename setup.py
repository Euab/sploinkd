import os
from setuptools import setup, find_packages


def copy_dir():
    base_dir = os.path.join("sploinkd/templates", "create-cpp-app")
    for dirpath, _, files in os.walk(base_dir):
        for f in files:
            print(os.path.join(dirpath.split('/', 1)[1], f))
            yield os.path.join(dirpath.split('/', 1)[1], f)


setup(
    name="sploinkd",
    version='1.0',
    description=(
        "Useful command line scripts"
    ),
    packages=find_packages(include=["sploinkd", "sploinkd.*"]),
    author="Euan Mills",
    author_email="euab.mills@gmail.com",
    package_data= {
        '' : [f for f in copy_dir()]
    }
)
