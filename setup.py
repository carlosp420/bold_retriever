# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='bold_retriever',
    version='1.0.0',
    description='It queries the BOLD database to get identification of taxa ' \
                'based on COI sequences',
    long_description=readme + '\n\n' + history,
    author='Carlos Pena',
    author_email='mycalesis@gmail.com',
    maintainer='Carlos Pena',
    url='https://github.com/carlosp420/bold_retriever',
    packages=[
        'bold_retriever',
    ],
    package_dir={'bold_retriever':
                 'bold_retriever'},
    include_package_data=True,
    license="GPL v3",
    zip_safe=False,
    keywords='bold_retriever',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
    ],
)
