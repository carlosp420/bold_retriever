from distutils.core import setup


setup(
    name='bold_retriever',
    version='0.0.7',
    url="https://github.com/carlosp420/bold_retriever",
    author="Carlos Pena",
    author_email="mycalesis@gmail.com",
    maintainer="Carlos Pena",
    maintainer_email="mycalesis@gmail.com",
    contact="Carlos Pena",
    contact_email="mycalesis@gmail.com",
    license="GPL v3",
    description="get barcoded info from BOLD",
    long_description=open('README.md').read(),
    platforms="any",
    download_url="",
    classifiers=[
        "Programming Language :: Python",
        ("Topic :: Scientific/Engineering :: Bio-Informatics"),
        ("Intended Audience :: Science/Research"),
        ("License :: OSI Approved :: GNU General Public License v3 (GPLv3)"),
        ("Operating System :: OS Independent"),
        ("Environment :: Console"),
    ],
    packages=['bold_retriever'],
)
