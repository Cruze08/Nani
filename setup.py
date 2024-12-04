from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in nani_foods/__init__.py
from nani_foods import __version__ as version

setup(
	name="nani_foods",
	version=version,
	description="Nani Agro Foods",
	author="Simpel",
	author_email="simpelerp@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
