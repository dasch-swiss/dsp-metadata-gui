# DSP-METADATA-GUI Metadata Module

The `dsp-metadata-gui` is a GUI application written in Python for collecting project specific metadata and turn it into RDF.

As part of the `dsp-tools`, its aim is to enable researchers and project managers who deposit research data on the DaSCH Service Platform (DSP), to add metadata about the project and datasets to the DSP repository. By providing metadata, the project will be searchable on the platform, which is an integral part of the FAIR principles.

The metadata follows the schema defined by the [dsp-ontologies](https://github.com/dasch-swiss/dsp-ontologies).



## Install and run

The module provides a command line entry point to run the GUI. The only requirement is Python 3 and PIP.

The application has only been tested on Python 3.9, but it might work on older versions too.

__Note:__ There have been issues with `conda` installations. If this is the case, consider using a virtual environment.


### Installation via pip

To install the application, run:

```bash
pip install dsp-metadata-gui
```

Or respectively:

```shell
pip3 install dsp-metadata-gui
```

Afterwards, the program can be started by running the command `dsp-metadata` in your terminal of choice.


### Installation from source

Clone [this repo](https://github.com/dasch-swiss/dsp-metadata-gui) and run `make make-and-run`. If you don't use GNU Make, run the commands specified in the `Makefile` manually.

This will package the application, install it to your python environment and run the application.



## Usage

### Collecting Metadata

The application is divided into two windows:

1. The main window lets you organize a list of projects, for which you can collect metadata. Several actions can be performed with projects, e.g. editing or exporting the project.

2. When editing a project, in the project window, the actual metadata can be added, modified and saved.

To add a project, you will need the project short code, which is assigned to you by the DaSCH Client Services.  
A project is always associated with a folder on your local machine. If any files should be included with the metadata import, these files must be within that folder.
Once all metadata are added and valid, and the overall RDF graph of the metadata set validates against the ontology, the project can be exported for upload to the DSP.

All data is locally stored in the file `~/DaSCH/config/repos.data`. for more detail, see [here](https://dasch-swiss.github.io/dsp-metadata-gui/list_view/#local-data-storage).



### Conversion to V2

The metadata generated by the application conforms to the first version of the data model for metadata.  
This corresponds to the data that can currently be viewed in the [DaSCH Metadata Browser](https://meta.dasch.swiss).

The initial datamodel will eventually be replaced by the model V2 which introduces major improvements.  
Metadata V2 will eventually be collected directly in the web interface rather than in this python application.  
In the mean time until the web interface for editing metadata is implemented, this application provides a script to automatically convert V1 `.ttl` files into V2 `.json` files.

> NB: The conversion can not be fully automated, as the model V2 is more rich in information than V1.  
> For convenience, the conversion adds the string `XX` wherever the output can not be determined with sufficient confidence. __Please check those instances manually.__  
> The conversion also does some "guessing" work, as e.g. the language of literal values or the display text for URLs. If the output can be determined with a sufficient level of confidence, the conversion will ___not___ add `XX`. __However it is still advisable to check the entirety of the output for potential errors.__

The most important changes from V1 to V2 include the following additions:

- Support for multi-language literals.

- `howToCite` on project level

- `country` property for addresses.

- Creation and modification timestamps.

- JSON-Schema validation




## Development

### Development Environment

#### Pipenv

Use `pipenv` for a seamless development experience.  
In order to have both dependencies and dev-dependencies installed from the `Pipfile`, set up the virtual environment running
```
pipenv instal --dev
```

`pipenv` will manage dependencies as well as a virtual environment. To install packages, use
```
pipenv install <package-name>
```

To create `requirements.txt`, run 
```
pipenv lock -r > requirements.txt
```

To bring `setup.py` up to date, run
```
pipenv run pipenv-setup sync
```

#### GNU Make

`GNU Make` is used to automatize most tasks.  
Run `make help` for info on the available targets.

__Note:__ All make targets - except `make run` - should be run from within the `pipenv` shell:  
Either by running
```
pipenv run make <target-name>
```
or by opening a virtual pipenv shell by running
```
pipenv shell
make <target-name>
...
exit
```


### Documentation

The documentation is created using `mkdocs` and `mkdocstrings` with `markdown_include.include`. To create the documentation, make sure to install all of these, using pip.

To serve the documentation locally, run `make doc`. To deploy the documentation to github pages, run `make deploy-doc`.


