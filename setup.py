from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in biometric_integration_ftp/__init__.py
from biometric_integration_ftp import __version__ as version

setup(
	name="biometric_integration_ftp",
	version=version,
	description="Biometric Integration",
	author="ajogdand@dexciss.com",
	author_email="ajogdand@dexciss.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
