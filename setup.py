from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dsp-metadata-gui",
    version="1.2.1",
    description="Python GUI tool to collect metadata for DSP projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dasch-swiss/dsp-metadata-gui",
    author="Balduin Landolt",
    author_email="balduin.landolt@dasch.swiss",
    license="GPLv3",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9.0",
    install_requires=[
        "attrs==21.2.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "beautifulsoup4==4.10.0",
        "certifi==2021.5.30",
        "charset-normalizer==2.0.6; python_version >= '3.0'",
        "click==8.0.1; python_version >= '3.6'",
        "decorator==5.1.0; python_version >= '3.5'",
        "guess-language-spirit==0.5.3",
        "idna==3.2; python_version >= '3.0'",
        "isodate==0.6.0",
        "joblib==1.0.1; python_version >= '3.6'",
        "jsonschema==4.0.0",
        "langdetect==1.0.9",
        "langid==1.1.6",
        "nltk==3.6.3; python_version >= '3.6'",
        "numpy==1.21.2; python_version >= '3.0'",
        "owlrl==5.2.3",
        "pillow==8.3.2; python_version >= '3.6'",
        "pyenchant==3.2.1",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pyrsistent==0.18.0; python_version >= '3.6'",
        "pyshacl==0.17.0.post2",
        "rdflib==6.0.1; python_version >= '3.7'",
        "regex==2021.9.24",
        "requests==2.26.0",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "soupsieve==2.2.1; python_version >= '3.6'",
        "textblob==0.15.3",
        "tqdm==4.62.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.26.7; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_full_version < '4.0.0'",
        "validators==0.18.2",
        "wxpython==4.1.1",
    ],
    entry_points={
        "console_scripts": [
            "dsp-metadata=dspMetadataGUI.collectMetadata:collectMetadata"
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
