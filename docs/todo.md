# Pending Tasks

## Programming

### minor changes / fixes

- [x] fix layout issue in dataset tab
- [x] unify capitalization in GUI
- [x] make end date optional
- [x] fix to-string of Grant class
- [x] relative URI of DMP is only `<DMP>` which is not unique
- [x] change names to string instead of list
- [x] change `@base` and IRIs to work correctly
- [ ] layout:
    - [ ] long abstract etc. hides buttons
    - [ ] rethink tabs order
    - [ ] make RDF preview scale with window size
    - [ ] ... (anythng else?)

### medium size changes

- [ ] check validity before export
- [ ] for URLs (including place), get more reasonable propertyID values
- [x] ensure that RDF is up to date when exporting
- [ ] store .ttl upon change/save instead of creating it on the fly all the time
- [ ] switching qualified attribution should change role too
- [ ] add language tag to string properties
- [ ] allow deleting last Person/Organization/Dataset
- [ ] rework export function: let user decide what they want (file format, where to store, entire zip, ...)
- [ ] avoid adding persons/etc to graph, if not referenced anywhere

### major changes

- [ ] have versioning in pickles
- [ ] try to handle pickles from older versions
- [ ] implement upload to DSP functionality
- [ ] implement import from RDF functionality


## Documentation

### Usage Documentation

- [x] minimum python version
- [x] note on issues with conda
- [x] note on venv recommendation
- [ ] Update UML diagram
- [ ] Include UML diagram
- [x] Restructure documentation
- [x] document import pickle function
- [ ] Write documentation files:
    - [x] index
    - [x] Readme
    - [x] Usage_overview
    - [x] list_view
    - [x] tab_view
    - [ ] Changelog
- [ ] fix link in readme so it works both in readme and in docs
- [ ] document all classes (explain properties, tab by tab)


### API Reference

- [ ] Add docstring to all classes
- [ ] Think about how to handle private methods in documentation
- [ ] Manually write documentation for `collectMetadata.md`


## Others

- [x] get doc theme to work
- [ ] fix issue with dependencies not installing automatically
- [ ] find out what the real minimum python version is (3.9 is rather high)
- [ ] investigate issue on windows
- [ ] investigate `ssl.SSLCertVerificationError`
- [ ] look into `__init__.py`
- [ ] have another look at imports and why it doesn't run directly from script, only with installation

## Nice to Have
- [ ] rdf graph visualization
- [ ] Proper Menu
  - [ ] Options
    - [ ] Save on Tab-Change
  - [ ] Help
- [ ] when adding a project, allow selecting an existing DSP project and get metadata from there, if any.
