from setuptools import find_packages, setup

setup(
    name="lsystem",
    packages=find_packages(),
    entry_points={"console_scripts": ["lsystem=lsystem.main:main"]},
)
