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
    - [ ] long abstract hides buttons
    - [ ] rethink tabs order
    - [ ] ... (anythng else?)

### medium size changes

- [ ] check validity before export
- [ ] ensure that RDF is up to date when exporting
- [ ] store .ttl upon change/save instead of creating it on the fly all the time
- [ ] switching qualified attribution should change role too
- [ ] add language tag to string properties
- [ ] allow deleting last Person/Organization/Dataset

### major changes

- [ ] have versioning in pickles
- [ ] try to handle pickles from older versions
- [ ] implement upload to DSP functionality
- [ ] implement import from functionality


## Documentation

### Usage Documentation

- [ ] minimum python version
- [ ] note on issues with conda
- [ ] note on venv recommendation
- [ ] Update UML diagram
- [ ] Include UML diagram
- [x] Restructure documentation
- [ ] document import pickle function
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

## Nice to Have
- [ ] rdf graph visualization
- [ ] Proper Menu
  - [ ] Options
    - [ ] Save on Tab-Change
  - [ ] Help
- [ ] when adding a project, allow selecting an existing DSP project and get metadata from there, if any.
