import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, '../README.md')) as f:
    README = f.read()

install_requires = [
    'matplotlib',
    'numpy',
]

tests_require = ['mock',
                 'xmlrunner',
                 'discover']

setup_requires = []

setup(name='jshadobf',
      version='0.2',
      description='JShadobf',
      long_description=README + '\n\n',
      classifiers=[
          "Programming Language :: Python",
          "Topic :: JAVASCRITP :: OBFUSCATION"],
      author='Benoit Bertholon',
      author_email='benoit@bertholon.info',
      url='https://www.jshadobf.com',
      keywords='javascript obfuscation',
      packages=find_packages(),
      package_data={},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      setup_requires=setup_requires,
      test_suite="jshadobf",
      entry_points={
          'console_scripts': ['obfuscate = jshadobf.tool.obfuscate:main']
      }
      )

