from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name = 'pyHelialux',
    packages = ['helialux'],
    install_requires=['requests'],
    version = '0.1.0',
    description = 'A library to communicate with with Juwel\'s HeliaLux Controller',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Maarten Hoogendoorn',
    url='https://github.com/moretea/pyHelialux',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)
