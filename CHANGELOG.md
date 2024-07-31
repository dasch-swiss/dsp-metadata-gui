# Changelog

## [8.4.1](https://github.com/dasch-swiss/dsp-metadata-gui/compare/v8.4.0...v8.4.1) (2024-07-31)


### Maintenance

* update readme ([dd89752](https://github.com/dasch-swiss/dsp-metadata-gui/commit/dd897521d161602c097997b1611337527698ec64))

## [8.4.0](https://github.com/dasch-swiss/dsp-metadata-gui/compare/v8.3.0...v8.4.0) (2024-07-31)


### Enhancements

* add conversion to v2 datamodel (DSP-1419) ([#13](https://github.com/dasch-swiss/dsp-metadata-gui/issues/13)) ([f1f90bf](https://github.com/dasch-swiss/dsp-metadata-gui/commit/f1f90bff7b4d66f5ba646f71691e1d28fb71ad02))
* add undefined validity ([5c71077](https://github.com/dasch-swiss/dsp-metadata-gui/commit/5c71077bd854856fb2218b8eec030ef3c66d6f47))
* **data-model-v2:** add conversion from json to rdf for new data model (DSP-1731) ([#19](https://github.com/dasch-swiss/dsp-metadata-gui/issues/19)) ([46993e2](https://github.com/dasch-swiss/dsp-metadata-gui/commit/46993e284487f9821d420ef310579df24e2427d5))
* **datamodel-v2:** change conversion according to new data model (DSP-1731) ([#17](https://github.com/dasch-swiss/dsp-metadata-gui/issues/17)) ([6741397](https://github.com/dasch-swiss/dsp-metadata-gui/commit/6741397d3ba8a44587de0d3d5a99ba7b6eea4091))
* exclude non-connected stuff from graph ([72801d5](https://github.com/dasch-swiss/dsp-metadata-gui/commit/72801d5f912cb7b78c7d9965601e930193ad56fa))
* improve IRI handling ([9bcb2a3](https://github.com/dasch-swiss/dsp-metadata-gui/commit/9bcb2a3ffc51e65d2a215cef730b807c06e70ff9))
* make RDF conversion accessible thorugh CLI entry point ([#22](https://github.com/dasch-swiss/dsp-metadata-gui/issues/22)) ([aebb6ca](https://github.com/dasch-swiss/dsp-metadata-gui/commit/aebb6cab232e4ed6c1bce892be2b3db3df7a8aed))
* simplify JSON model ([#30](https://github.com/dasch-swiss/dsp-metadata-gui/issues/30)) ([1a57de8](https://github.com/dasch-swiss/dsp-metadata-gui/commit/1a57de89b31df0c12f9bee5b7177a169b188a4e4))


### Bug Fixes

* adding attribution resets textfield ([e00ad39](https://github.com/dasch-swiss/dsp-metadata-gui/commit/e00ad39024df6f25be685bde50cdd09c5eb822b1))
* bug causing the application not to start on windows ([21996ef](https://github.com/dasch-swiss/dsp-metadata-gui/commit/21996ef5278b3c48d2dfbaa162faaea0b2169f05))
* copy paste error - wrong datatype for a property ([5c45b18](https://github.com/dasch-swiss/dsp-metadata-gui/commit/5c45b1891021536beb97bdffbdde3f3637dcbf80))
* correct graph for Place ([19153be](https://github.com/dasch-swiss/dsp-metadata-gui/commit/19153be3febb275069fcf1e113cf52eb35e2e7fd))
* correct object gets deleted ([158ba7f](https://github.com/dasch-swiss/dsp-metadata-gui/commit/158ba7f4a5dcecef46bb987b84151a58c771b00a))
* don't hide buttons when description is overly long ([721a4ce](https://github.com/dasch-swiss/dsp-metadata-gui/commit/721a4ce77a4f15937172c408df6b5370922319ac))
* encoding issue on windows. output is not utf-8 ([dad98d7](https://github.com/dasch-swiss/dsp-metadata-gui/commit/dad98d70d22048866914ae5a8915ea48db822aa7))
* Error when opening help popup ([dfe6c34](https://github.com/dasch-swiss/dsp-metadata-gui/commit/dfe6c3427d6a61c6bb055d4881dc714badd7e25c))
* error with propertyID in URLs ([c365eb5](https://github.com/dasch-swiss/dsp-metadata-gui/commit/c365eb54a3c3081c43e062d7be330147a4ceb05e))
* failing to select stuff; Feature: add data with enter ([7acbb95](https://github.com/dasch-swiss/dsp-metadata-gui/commit/7acbb95963e3e6b32e561a8821de877df30bfd97))
* fit help texts in help popup ([023e38a](https://github.com/dasch-swiss/dsp-metadata-gui/commit/023e38a9889ac739dab01446b769354fe54aae35))
* fix layout issue with rdf preview ([6591f90](https://github.com/dasch-swiss/dsp-metadata-gui/commit/6591f9079def35f5f1dffc6c171aabb66a827fd6))
* installation not possible with current pip version ([#24](https://github.com/dasch-swiss/dsp-metadata-gui/issues/24)) ([4090007](https://github.com/dasch-swiss/dsp-metadata-gui/commit/409000791673367741c285fb5e6e69283e8cfddb))
* installation still fails on later pip versions ([#26](https://github.com/dasch-swiss/dsp-metadata-gui/issues/26)) ([0eb253a](https://github.com/dasch-swiss/dsp-metadata-gui/commit/0eb253a7ccd1772e1d8689c0065578ef8b95150d))
* issue with IRIs ([91a4d7d](https://github.com/dasch-swiss/dsp-metadata-gui/commit/91a4d7dfe6fcd51fdeff9d8f3a8c409035bb340e))
* issues with RDF to json conversion ([#28](https://github.com/dasch-swiss/dsp-metadata-gui/issues/28)) ([4801f95](https://github.com/dasch-swiss/dsp-metadata-gui/commit/4801f95cf82035fffb815cd9a2e034ad1034c52d))
* layout in dataset tab ([60525e1](https://github.com/dasch-swiss/dsp-metadata-gui/commit/60525e1ccfaf87d4661c40fa0cff35fb2244dc58))
* Layout issues with overly long texts ([dcbf6a3](https://github.com/dasch-swiss/dsp-metadata-gui/commit/dcbf6a31b7c9ab3bc21f733e146c189550bed965))
* layout problem in project tab ([ac5c59b](https://github.com/dasch-swiss/dsp-metadata-gui/commit/ac5c59b9c45ced806239eb95df6609ee9bd09be1))
* make email string instead of IRI ([6936b52](https://github.com/dasch-swiss/dsp-metadata-gui/commit/6936b52c9cc5dc793ba2765c496846dd5dbced67))
* make IRIs valid ([853b982](https://github.com/dasch-swiss/dsp-metadata-gui/commit/853b982ad83d75595328546a450a34c711d70632))
* module not found when installing from PyPI (DSP-1731) ([#20](https://github.com/dasch-swiss/dsp-metadata-gui/issues/20)) ([097bf24](https://github.com/dasch-swiss/dsp-metadata-gui/commit/097bf2475ef33541285f7563ae279a534d43daec))
* NPE ([911d99d](https://github.com/dasch-swiss/dsp-metadata-gui/commit/911d99ded5a745e60a0e146e1e25bc8a2007ed51))
* NPE; Feature: make DMP IRI unique ([8a831a9](https://github.com/dasch-swiss/dsp-metadata-gui/commit/8a831a9ce6852d0fa565d2392aa3be0613ba8680))
* Null pointer exception ([5812cb4](https://github.com/dasch-swiss/dsp-metadata-gui/commit/5812cb43bb9edf310b6deac292ddef0ad8da279b))
* problem with finding person/organization by its string ([b9dba23](https://github.com/dasch-swiss/dsp-metadata-gui/commit/b9dba23bc209a06bdf4a2419bbfee1745166ca4d))
* remove base again ([1e85bf7](https://github.com/dasch-swiss/dsp-metadata-gui/commit/1e85bf7792dee7dc3df2af4f49074bdd70c2de03))
* some cosmetics in UI ([2c146a5](https://github.com/dasch-swiss/dsp-metadata-gui/commit/2c146a5ebb50837a34edb7fa8c29be484cd5d506))
* some serialization problems ([b9ddad6](https://github.com/dasch-swiss/dsp-metadata-gui/commit/b9ddad6a8736d0ab2956c6ff8e52de29501aba59))
* some wrong cardinalities, missing serialization ([b061eab](https://github.com/dasch-swiss/dsp-metadata-gui/commit/b061eab6d5ff191784a36082ae91346aebb8b9ba))
* strip whitespace from input (DSP-1681) ([#16](https://github.com/dasch-swiss/dsp-metadata-gui/issues/16)) ([132878d](https://github.com/dasch-swiss/dsp-metadata-gui/commit/132878dceb6490086c7647cfc0c77692ceb338ed))
* **UI:** remove unused button ([9d5dad2](https://github.com/dasch-swiss/dsp-metadata-gui/commit/9d5dad240eb8535353f85f40b6f5e4aff796392a))
* update doc according to new structure ([6f6a862](https://github.com/dasch-swiss/dsp-metadata-gui/commit/6f6a8629e27224aecae5e4c1764e74262944255e))
* update Grants list correctly when adding/removing ([738dc77](https://github.com/dasch-swiss/dsp-metadata-gui/commit/738dc7710d352a286aa495ead1e9684469763f98))
* Validation issues ([84c9cff](https://github.com/dasch-swiss/dsp-metadata-gui/commit/84c9cffc517bf5f4ec6fe8d5e4c84effedce0bc4))
* wrong cardinality ([d43c19e](https://github.com/dasch-swiss/dsp-metadata-gui/commit/d43c19ed87db20d4f168df349d6f316ff6e2da5e))
* wrong function name ([2ad5ba1](https://github.com/dasch-swiss/dsp-metadata-gui/commit/2ad5ba195e86478cc66d1bdaace702749ff0d3a7))
* wrong validation pattern for short code ([cf92762](https://github.com/dasch-swiss/dsp-metadata-gui/commit/cf92762b65fbb2e98666943dbc3b2e425b03cb29))


### Maintenance

* adjust requirements and pump to rc3 ([35381d5](https://github.com/dasch-swiss/dsp-metadata-gui/commit/35381d5b0141f8821d49fc069a5bb1b3ea36fa7c))
* adjust version numbering to regulart pypi versioning ([6402fdb](https://github.com/dasch-swiss/dsp-metadata-gui/commit/6402fdb1a5ebd0b6a18c95910bb719d4fe78c4c9))
* attempt to fix PyPI release ([#32](https://github.com/dasch-swiss/dsp-metadata-gui/issues/32)) ([d226321](https://github.com/dasch-swiss/dsp-metadata-gui/commit/d22632153f5ebe7ea56ef7c41c447f604e39e490))
* bump to rc6 ([fc5c9fb](https://github.com/dasch-swiss/dsp-metadata-gui/commit/fc5c9fb92cc7c5512ee3f5b8b18e9e61a7f2b709))
* bump version to 0.3.9 ([94c6933](https://github.com/dasch-swiss/dsp-metadata-gui/commit/94c69331ffedde62b585cedd077937149cf5b9aa))
* bump version to 1.0 ([b568458](https://github.com/dasch-swiss/dsp-metadata-gui/commit/b5684587a0058a4dfc71a2840b17018b28f8b863))
* bump version to rc4 ([a80104e](https://github.com/dasch-swiss/dsp-metadata-gui/commit/a80104ea8683f1b739af24948a0f6411635fd24f))
* bump version to rc5 ([174f322](https://github.com/dasch-swiss/dsp-metadata-gui/commit/174f3229228c500c2e65a939c3dd663bc59d0443))
* bump version to rc7 ([79fedcb](https://github.com/dasch-swiss/dsp-metadata-gui/commit/79fedcb24479a038cb62cc16decfe9debe106e41))
* comment out unused code ([2bda342](https://github.com/dasch-swiss/dsp-metadata-gui/commit/2bda3421ca0e4a0c5638ab21e0b9eb51f8ded6bd))
* delegate initial values to refresh method ([f34efd6](https://github.com/dasch-swiss/dsp-metadata-gui/commit/f34efd60052fd5ab7c667257594ae502b61e083e))
* don't call refresh/update on tab1 ([c413418](https://github.com/dasch-swiss/dsp-metadata-gui/commit/c413418fe07a7b51b1dda358ab385b7bf9f8e848))
* fix release please action (DSP-1530) ([#7](https://github.com/dasch-swiss/dsp-metadata-gui/issues/7)) ([ba16a56](https://github.com/dasch-swiss/dsp-metadata-gui/commit/ba16a56cb12d98acbc68749343bd44901a2d79ad))
* fix release-please setup ([a86147a](https://github.com/dasch-swiss/dsp-metadata-gui/commit/a86147a90cde463563d3ee64f792cfc31bd1d62d))
* improve PR title check (DSP-1530) ([#9](https://github.com/dasch-swiss/dsp-metadata-gui/issues/9)) ([ec8cc31](https://github.com/dasch-swiss/dsp-metadata-gui/commit/ec8cc31324341b53785d4e520e39afaf85d6869e))
* improve relative import stuff ([8b57453](https://github.com/dasch-swiss/dsp-metadata-gui/commit/8b574536dc892bf43016887a5edf606b4d29067d))
* info popup string ([e44cf0e](https://github.com/dasch-swiss/dsp-metadata-gui/commit/e44cf0e5530b8a8ee8e45122a7c5e7528c69a2ac))
* move calendar to main gui file to get rid of helper file ([2da8895](https://github.com/dasch-swiss/dsp-metadata-gui/commit/2da88956f04e97b0a9374f7e8ca79bec10e11338))
* move rdf generation into specific class ([24fbafb](https://github.com/dasch-swiss/dsp-metadata-gui/commit/24fbafb9d2db7b4bfd6948a9939f36f497e003a3))
* move some files to correct folder ([c5ead8b](https://github.com/dasch-swiss/dsp-metadata-gui/commit/c5ead8bf0aaa519b1e3fcf6456337be38361a901))
* order classes more logically ([a37423d](https://github.com/dasch-swiss/dsp-metadata-gui/commit/a37423d46373403391f2ea396fbb4ad01cdde046))
* prepare release 1.0.3 ([#10](https://github.com/dasch-swiss/dsp-metadata-gui/issues/10)) ([a29e7f8](https://github.com/dasch-swiss/dsp-metadata-gui/commit/a29e7f8fcd887200f550a6ca6b37c0ba071193f0))
* release 1.0.4 ([#12](https://github.com/dasch-swiss/dsp-metadata-gui/issues/12)) ([34400ae](https://github.com/dasch-swiss/dsp-metadata-gui/commit/34400aef3e7ab45ea673b81f8b7820d461e2f8fe))
* release 1.1.0 ([#14](https://github.com/dasch-swiss/dsp-metadata-gui/issues/14)) ([344cd30](https://github.com/dasch-swiss/dsp-metadata-gui/commit/344cd3056686a8f672e4a7f8928174bdf3115b9b))
* release 1.2.0 ([#18](https://github.com/dasch-swiss/dsp-metadata-gui/issues/18)) ([ac3f29a](https://github.com/dasch-swiss/dsp-metadata-gui/commit/ac3f29af1e61ed68ade9cc146155b54e794ccbba))
* release 1.2.1 ([#21](https://github.com/dasch-swiss/dsp-metadata-gui/issues/21)) ([28ce353](https://github.com/dasch-swiss/dsp-metadata-gui/commit/28ce353119864924485d550695a2ff58975a7718))
* release 1.3.0 ([#23](https://github.com/dasch-swiss/dsp-metadata-gui/issues/23)) ([cff463a](https://github.com/dasch-swiss/dsp-metadata-gui/commit/cff463a5e0517820c73affbd1d9880b9ea2158a2))
* release 1.3.1 ([#25](https://github.com/dasch-swiss/dsp-metadata-gui/issues/25)) ([61ef6c6](https://github.com/dasch-swiss/dsp-metadata-gui/commit/61ef6c6461552d973fae9251785f6c163803958d))
* release 1.3.2 ([#27](https://github.com/dasch-swiss/dsp-metadata-gui/issues/27)) ([c5d9b3f](https://github.com/dasch-swiss/dsp-metadata-gui/commit/c5d9b3fcf305e207972b1c6d5e69369216ca31e0))
* release 1.3.3 ([#29](https://github.com/dasch-swiss/dsp-metadata-gui/issues/29)) ([aed3254](https://github.com/dasch-swiss/dsp-metadata-gui/commit/aed3254f08c0a2cc2ce2076b0176bbb4c6eb8acb))
* release 1.4.0 ([#31](https://github.com/dasch-swiss/dsp-metadata-gui/issues/31)) ([de1ae9e](https://github.com/dasch-swiss/dsp-metadata-gui/commit/de1ae9e7d679bc828864f3379959f9cba263c897))
* release 1.4.1 ([#33](https://github.com/dasch-swiss/dsp-metadata-gui/issues/33)) ([6ff1387](https://github.com/dasch-swiss/dsp-metadata-gui/commit/6ff1387dfc6df84d59b14b5bcee095c70e901a95))
* release 1.4.2 ([#35](https://github.com/dasch-swiss/dsp-metadata-gui/issues/35)) ([4638f2f](https://github.com/dasch-swiss/dsp-metadata-gui/commit/4638f2fc8afb13fa235c28937f26787b193fe9d3))
* remove obsolete code ([e72bbc7](https://github.com/dasch-swiss/dsp-metadata-gui/commit/e72bbc78fb084e1d4441d2a5119666ee7f74bbb0))
* remove redundant code ([9c39534](https://github.com/dasch-swiss/dsp-metadata-gui/commit/9c39534427f12118e80cfb473de7125387fd17a9))
* remove some old code; add todos ([5bdae9a](https://github.com/dasch-swiss/dsp-metadata-gui/commit/5bdae9a5ca5825edae7bd979baa0f87167ec1c75))
* rename some methods ([a3a32bf](https://github.com/dasch-swiss/dsp-metadata-gui/commit/a3a32bfdf959db786446b770ac81c946b29ac393))
* replace pipenv with poetry ([#34](https://github.com/dasch-swiss/dsp-metadata-gui/issues/34)) ([17e1dd2](https://github.com/dasch-swiss/dsp-metadata-gui/commit/17e1dd28f71d0acc850db879b7ec715dfea1dc6c))
* restructure file and folder structure of the repo ([5191884](https://github.com/dasch-swiss/dsp-metadata-gui/commit/519188430d642f2e58f0e5cda8d35e16ed6dc1dc))
* Rework how updating data and refreshing UI works ([14be3f1](https://github.com/dasch-swiss/dsp-metadata-gui/commit/14be3f1809ce47899e8c526f8474b1e92511136d))
* set up GitHub actions (DSP-1530) ([#6](https://github.com/dasch-swiss/dsp-metadata-gui/issues/6)) ([f219a21](https://github.com/dasch-swiss/dsp-metadata-gui/commit/f219a211a088a6fcae5aeee4ea91c555163912c6))
* tag HEAD as 1.0.3 release ([#8](https://github.com/dasch-swiss/dsp-metadata-gui/issues/8)) ([080ff47](https://github.com/dasch-swiss/dsp-metadata-gui/commit/080ff470746634ffa6ea847d817bea45257eaf8d))
* tidy up some code ([8c3de5c](https://github.com/dasch-swiss/dsp-metadata-gui/commit/8c3de5c11bd99fc31a0a5a15231741a2621eaa12))
* tidy up some code ([212b91c](https://github.com/dasch-swiss/dsp-metadata-gui/commit/212b91cf7800229ee0aa36c95da9db555c6484e8))
* tidy up some code ([7cfb62c](https://github.com/dasch-swiss/dsp-metadata-gui/commit/7cfb62c0529c50b988649d7d0c541ede4f350e63))
* Tidy up some code ([6b6e9b7](https://github.com/dasch-swiss/dsp-metadata-gui/commit/6b6e9b770abcfb7ef26f94b30959c705d00f0674))
* tidy up some old code ([f5d72cc](https://github.com/dasch-swiss/dsp-metadata-gui/commit/f5d72ccb86e4fb8bb457e753f86a770a7975ac44))
* update dependencies ([2acf61b](https://github.com/dasch-swiss/dsp-metadata-gui/commit/2acf61b9bb3185761805e40834c94e10c34d1a1c))
* update makefile ([e4fade6](https://github.com/dasch-swiss/dsp-metadata-gui/commit/e4fade6e5c4a7187ab2e3aeb080cac698b496fb4))
* update packaging ([b9b09d8](https://github.com/dasch-swiss/dsp-metadata-gui/commit/b9b09d82e1009bd145d7b6a635d17e200eb3db4b))
* update release-please setup ([fb8853c](https://github.com/dasch-swiss/dsp-metadata-gui/commit/fb8853c890d44072c5c9d9681e82c77b23397925))


### Documentation

* add troubleshoot section to documentation (DSP-1683) ([#15](https://github.com/dasch-swiss/dsp-metadata-gui/issues/15)) ([c310b4e](https://github.com/dasch-swiss/dsp-metadata-gui/commit/c310b4ed6bee5df6b0aed4f38ad3a6d268f5e893))
* finish API documentation ([d02fc7e](https://github.com/dasch-swiss/dsp-metadata-gui/commit/d02fc7e791403c5a1ca1d9423e2e0ec09e562518))
* minor improvements and typo fixes in documentation (DSP-1531) ([#11](https://github.com/dasch-swiss/dsp-metadata-gui/issues/11)) ([68976b3](https://github.com/dasch-swiss/dsp-metadata-gui/commit/68976b3499eef6b8d8808ee281649e433d7ff145))

### [1.4.2](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.4.1...v1.4.2) (2024-07-31)


### Maintenance

* replace pipenv with poetry ([#34](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/34)) ([17e1dd2](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/17e1dd28f71d0acc850db879b7ec715dfea1dc6c))

### [1.4.1](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.4.0...v1.4.1) (2024-07-31)


### Maintenance

* attempt to fix PyPI release ([#32](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/32)) ([d226321](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/d22632153f5ebe7ea56ef7c41c447f604e39e490))

## [1.4.0](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.3.3...v1.4.0) (2024-07-31)


### Enhancements

* simplify JSON model ([#30](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/30)) ([1a57de8](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/1a57de89b31df0c12f9bee5b7177a169b188a4e4))

### [1.3.3](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.3.2...v1.3.3) (2023-02-20)


### Bug Fixes

* issues with RDF to json conversion ([#28](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/28)) ([4801f95](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/4801f95cf82035fffb815cd9a2e034ad1034c52d))

### [1.3.2](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.3.1...v1.3.2) (2023-02-14)


### Bug Fixes

* installation still fails on later pip versions ([#26](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/26)) ([0eb253a](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/0eb253a7ccd1772e1d8689c0065578ef8b95150d))

### [1.3.1](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.3.0...v1.3.1) (2023-02-14)


### Bug Fixes

* installation not possible with current pip version ([#24](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/24)) ([4090007](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/409000791673367741c285fb5e6e69283e8cfddb))

## [1.3.0](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.2.1...v1.3.0) (2021-10-25)


### Enhancements

* make RDF conversion accessible thorugh CLI entry point ([#22](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/22)) ([aebb6ca](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/aebb6cab232e4ed6c1bce892be2b3db3df7a8aed))

### [1.2.1](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.2.0...v1.2.1) (2021-09-30)


### Bug Fixes

* module not found when installing from PyPI (DSP-1731) ([#20](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/20)) ([097bf24](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/097bf2475ef33541285f7563ae279a534d43daec))

## [1.2.0](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.1.0...v1.2.0) (2021-09-28)


### Enhancements

* **data-model-v2:** add conversion from json to rdf for new data model (DSP-1731) ([#19](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/19)) ([46993e2](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/46993e284487f9821d420ef310579df24e2427d5))
* **datamodel-v2:** change conversion according to new data model (DSP-1731) ([#17](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/17)) ([6741397](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/6741397d3ba8a44587de0d3d5a99ba7b6eea4091))

## [1.1.0](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.0.4...v1.1.0) (2021-06-02)


### Bug Fixes

* strip whitespace from input (DSP-1681) ([#16](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/16)) ([132878d](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/132878dceb6490086c7647cfc0c77692ceb338ed))


### Enhancements

* add conversion to v2 datamodel (DSP-1419) ([#13](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/13)) ([f1f90bf](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/f1f90bff7b4d66f5ba646f71691e1d28fb71ad02))


### Documentation

* add troubleshoot section to documentation (DSP-1683) ([#15](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/15)) ([c310b4e](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/c310b4ed6bee5df6b0aed4f38ad3a6d268f5e893))

### [1.0.4](https://www.github.com/dasch-swiss/dsp-metadata-gui/compare/v1.0.3...v1.0.4) (2021-04-19)


### Documentation

* minor improvements and typo fixes in documentation (DSP-1531) ([#11](https://www.github.com/dasch-swiss/dsp-metadata-gui/issues/11)) ([68976b3](https://www.github.com/dasch-swiss/dsp-metadata-gui/commit/68976b3499eef6b8d8808ee281649e433d7ff145))

### [1.0.3](https://github.com/dasch-swiss/dsp-metadata-gui/releases/tag/1.0.3) (2021-04-16)

### Maintenance

* prepare release 1.0.3

### [1.0.2](https://github.com/dasch-swiss/dsp-metadata-gui/releases/tag/1.0.2) (2021-03-26)

#### Bug Fixes

* **minor bugfix** exported files on windows are not UTF-8


### [1.0.1](https://github.com/dasch-swiss/dsp-metadata-gui/releases/tag/1.0.1) (2021-03-24)

#### Bug Fixes

* **Critical bugfix** Application does not start on windows.


### [1.0.0](https://github.com/dasch-swiss/dsp-metadata-gui/releases/tag/1.0.0) (2021-03-12)

* Initial release of the metadata GUI tool.
