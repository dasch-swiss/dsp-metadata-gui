import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dsp-metadata-gui',
    version='0.3.9',
    description='Python GUI tool to collect metadata for DSP projects.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dasch-swiss/dsp-metadata-gui',
    author='Balduin Landolt',
    author_email='balduin.landolt@dasch.swiss',
    license='GPLv3',
    packages=['dspMetadataGUI',
              'dspMetadataGUI.util'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.0',
    install_requires=[
        'certifi',
        'chardet',
        # 'decorator',
        'idna',
        'isodate',
        'numpy',
        'owlrl',
        'Pillow',
        'pyparsing',
        'pyshacl',
        'rdflib',
        'rdflib-jsonld',
        'requests',
        'six',
        'urllib3',
        'validators',
        'wxpython'
    ],
    entry_points={
        'console_scripts': [
            'dsp-metadata=dspMetadataGUI.collectMetadata:collectMetadata'
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
