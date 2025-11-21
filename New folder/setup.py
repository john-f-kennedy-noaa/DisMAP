from setuptools import setup, find_packages

with open('src/version.py') as fin: exec(fin.read())

setup(
    name='nmfs_species_range_metatdata',
    version=__version__,

    package_dir={'':'src'},
    packages=find_packages('src'),
    include_package_data=True,

    # PyPI MetaData
    author='John F. Kennedy',
    author_email='john.f.kennedy@noaa.gov',
    description='Collection of Utilities to Read/Write a Dataset\'s Metadata',
    license='Apache License - 2.0',
    keywords='esri,arcpy,metadata',
    url='https://github.com/john-f-kennedy-noaa/nmfs-species-range-metatdata',
    classifiers=[
        'Development Status :: 0 - Test',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Windows 10',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    zip_safe=False,
)
