# Usage Overview

## Installation

Be sure to have Python 3 installed.

{==

__Note:__

Due to some issues with the automatic installation of dependencies, the following three packages must be installed manually, before installing the tool itself:

- `validators`
- `isodate`
- `wxPython`

To install the application from there, run:

```shell
pip install validators isodate wxPython
```

or

```shell
pip3 install validators isodate wxPython
```

==}

To install the application, run:

```bash
pip install dsp-metadata-gui
```

Or respectively:

```shell
pip3 install dsp-metadata-gui
```

{==

__Note:__

Until the first release of the tool, it is available only on the [PYPI test instance](https://test.pypi.org/project/dsp-metadata-gui/).

To install the application from there, run:

```shell
pip install -i https://test.pypi.org/simple/ dsp-metadata-gui
```

or

```shell
pip3 install -i https://test.pypi.org/simple/ dsp-metadata-gui
```

==}


## Run

Once installed, you can start the tool from your terminal:
```shell
dsp-metadata
```


## Collect metadata

The application is divided into two main parts: [Project Organization](list_view.md) and the [Form for collecting Metadata](tabs_overview.md).

In the [Project Organization](list_view.md), you can organize all projects, for which you want to collect metadata.  
At first, you will need to add a new project. For that you need the project shortcode, which is provided by the DaSCH Client Services. (If you don't have your shortcode yet, [get in touch](mailto:info@dasch.swiss).)  
After adding at least one project, you can select a project in the list and perform several actions, like editing the data or exporting an RDF serialization of the project metadata.

When editing a project the [form for collecting metadata](tabs_overview.md) opens up.  
There are multiple tabs, where data can be entered for several classes like:

- Project
- Dataset(s)
- Person(s)
- etc.
