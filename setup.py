import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open('vapory/version.py').read()) # loads __version__

setup(name='Vapory',
      version=__version__,
      author='Zulko',
    description='3D rendering with Python and POV-Ray',
    long_description=open('README.rst').read(),
    license='see LICENSE.txt',
    keywords="3D POV-Ray Photo-realistic ray-tracing",
    packages= find_packages(exclude='docs'))
