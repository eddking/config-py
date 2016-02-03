from setuptools import setup
from release import assert_clean, get_version

assert_clean()

setup(
    name='config',
    version=get_version(),
    packages=['config'],
    description='a utility library for dealing with configuration',
    author='Edmund King',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ]
)
