<!---
Copyright © 2015-2019 the contributors (see Contributors.md).

This file is part of Knora.

Knora is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Knora is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with Knora.  If not, see <http://www.gnu.org/licenses/>.
-->

<!-- # Todos and Questions

Temp. Chapter: [Questions and Remarks for Documentation of GUI](todos_questions.md)

# DSP-METADATA-GUI Metadata Module

The dsp-metadata-gui is Python module and provides a GUI for collecting project specific metadata 
and store it in RDF XML.

## Specific objectives of the metadata module

- Collection of metadata on a scientific project for publication on the DSP
- Acquisition of metadata to create an archived project
- The metadata present the project and make it visible to other researchers
- The metadata follow a metadata schema which is explained under
 [dsp-ontologies](https://github.com/dasch-swiss/dsp-ontologies)


## Features

The metadata module is provided as a tool for recording just one research project or for the 
administration of several projects, for example in an institution. 
There are two windows. First you see a list view. Once you have created a project, you 
can carry on to the tabbed view.
One project, or a list of projects can be edited. 

Once all mandatory data of a project have been entered, the metadata can be validated. 
If the validation is successful, the project metadata (and files) can be uploaded to the DSP server. 

After approval by the DSP administrator, the project with its metadata (and possibly its project files) is publicly 
visible and findable.

For detailed description see  [overview](overview.md) page and follow the links.

## Use of the metadata module

1. Enter your short code, given by DaSCH Client Services 

2. Select a project folder with the project files it contains (the project folder can be empty, the files can be 
   selected later).

3. Select a project in the list and edit the metadata tabs. The following tabs are available: 
   Base Data, Project, Dataset, Person, Organisation, Grant. 
   Fill in the mandatory and possibly the optional fields. 
   
4. Once all mandatory fields are marked green, proceed to "Process selected to XML"

5. Upload the result of the processing file (XML, RDF/XML, Turtle, etc.) to the DaSCH Service Platform servers.
 -->

{!README.md!}
