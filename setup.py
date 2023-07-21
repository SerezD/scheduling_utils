from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(name='scheduling_utils',
      version='0.1.2',
      description='implementation of scheduling function utils',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/SerezD/scheduling_utils',
      author='DSerez',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True)
