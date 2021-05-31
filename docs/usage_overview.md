# Usage Overview

## Installation

Be sure to have Python 3 installed.

__Note:__ The application has only been tested on Python 3.9, but it might work on older versions too.

If you encounter any issues, see the troubleshoot section [below](#troubleshoot).

To install the application, run:

```bash
pip install dsp-metadata-gui
```

Or respectively:

```shell
pip3 install dsp-metadata-gui
```


## Run

Once installed, you can start the tool from your terminal:
```shell
dsp-metadata
```


## Collect metadata

The application is divided into two main parts: [Project Organization](list_view.md) and the [Form for collecting Metadata](tab_view.md).

In the [Project Organization](list_view.md), you can organize all projects, for which you want to collect metadata.  
At first, you will need to add a new project. For that you need the project shortcode, which is provided by the DaSCH Client Services. (If you don't have your shortcode yet, [get in touch](mailto:info@dasch.swiss).)  
After adding at least one project, you can select a project in the list and perform several actions, like editing the data or exporting an RDF serialization of the project metadata.

When editing a project the [form for collecting metadata](tab_view.md) opens up.  
There are multiple tabs, where data can be entered for several classes like:

- [Organization](organization.md)
- [Person](person.md)
- [Grant](grant.md)
- [Dataset](dataset.md)
- [Project](project.md)

_Note: The order may seem counter intuitive, not starting from the project and dataset. However, following the order of the tabs is recommended, as e.g. person depends on organization, etc._


## Troubleshoot

There is a number of known issues. In these cases, please try the following workarounds.

* There have been issues with `conda` installations. If this is the case, consider using a virtual environment.

* In some instances (typically on Mac OS, when python has _not_ been installed with Homebrew), installation works but when running the tool, a SSL error occurs.  
In that case you can either locate your python installation in `Applications > Python 3.9` and double-click the file `Install Certificates.command`. Alternatively, it should work if you install python via Homebrew.

* On Mac M1 Silicon devices, `Pillow` may cause issues. ...

If you encounter any further issues, do not hesitate to get in touch or open a GitHub issue.
