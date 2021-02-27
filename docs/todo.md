# Roadmap

## Initial Release

### Programming

- [x] switching qualified attribution should change role too
- [x] fix: remove correct item when removing one of multiple of top level classes (person, organization etc.)
- [x] allow deleting last Person/Organization/Dataset
- [x] avoid adding persons/etc to graph, if not referenced anywhere


### Documentation

#### Usage Documentation

- [x] fix link in readme so it works both in readme and in docs
- [x] document all classes (explain properties, tab by tab)
- [x] update doc to new tab order
- [x] update images

#### API Reference

- [x] Add docstring to all classes
- [x] Manually write documentation for `collectMetadata.md`


### Others

- [ ] test on windows
- [ ] test on linux
- [ ] investigate `ssl.SSLCertVerificationError`


## Next Major Version

### Programming

#### Smaller Features

- [ ] remove all error-catching for backwards-compatibility
- [ ] rework export function: let user decide what they want (file format, where to store, entire zip, ...)
  - [ ] check validity before export
- [ ] in attribution, ensure same person can have multiple roles, rather than having multiple attributions with same person
- [ ] add language tag to string properties

#### Bigger Features

- [ ] have versioning in pickles(?)
- [ ] try to handle pickles from older versions(?)
- [ ] implement upload to DSP functionality
- [ ] implement download from DSP
- [ ] implement import from RDF functionality
- [ ] regular json support


#### Necessities
- [ ] add unit tests


## Nice to Have / Ideas

- [ ] rdf graph visualization
- [ ] Proper Menu
  - [ ] Options
    - [ ] Save on Tab-Change
  - [ ] Help


