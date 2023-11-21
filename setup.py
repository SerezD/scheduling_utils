from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='scheduling_utils',
      version='0.2.3',
      description='implementation of LR scheduling functions in c++, binded using ctypes',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/SerezD/scheduling_utils',
      author='DSerez',
      license='MIT',
      packages=find_packages(),
      package_data={'scheduling_utils': ['cpp_extensions/schedulers.so', 'cpp_extensions/schedulers_win.dll']},
      zip_safe=False,
      include_package_data=True)
