from setuptools import setup, find_packages


setup(
    name="sploinkd",
    version='1.0',
    description=(
        "Useful command line scripts"
    ),
    packages=find_packages(include=["sploinkd", "sploinkd.*"]),
    author="Euan Mills",
    author_email="euab.mills@gmail.com"
)
