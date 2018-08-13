# Contributing to mothulity

You are more than welcome to contribute and if you do - great thanks! :+1:
Below you can find the description of mothulity structure and contribution guidelines.

## Table of Contents

[Flow](#flow)

[Branch Names](#branch-names)

[Hard-Coding](#hard-coding)

[Testing](#testing)

[Installation for Development](#installation-for-development)

[Mothulity Structure](#mothulity-structure)
  * [Python Files](#python-files)
  * [Mothur Binaries](#mothur-binaries)
  * [Config File](#config-file)
  * [JavaScript](#javascript)
  * [Templates](#templates)
  * [Tests](#tests)
  * [Data for Teststing](#data-for-testing)

[Deployment](#deployment)

## Flow

The philosophy behind mothulity is quite simple:

1. gather all the info from the user with a short one-liner.

2. run [Mothur](https://mothur.org/wiki/Main_Page)

3. gather the [Mothur's](https://mothur.org/wiki/Main_Page) output and generate an elegant HTML report.

mothulity does quite a lot of text processing. The engine that runs it is mostly [Jinja2](http://jinja.pocoo.org/docs/2.10/).
It is used for generating ```bash``` scripts that run [Mothur](https://mothur.org/wiki/Main_Page) and the final HTML report.

## Branch names

The branch names **must** be named after issues so they **must** contain the corresponding issue number. Every issue has also a label. Thus, the only accepted convention naming branches is label-of-issue#number-of-issue. The labels are 3-letters shortcuts. Upper letters should be used.

For instance: BUG#42 or UPD#66 or ENH#13

## Hard-coding

**No hard-coding is allowed**. The ```config``` file is meant for the persistent storage.
When defining a function, do **NOT** use raw str or int - wrap it in a variable:

For instance:

**BAD**

```python
def f(arg1):
    if arg1 == 'answer to everything':
        return 42
```

**GOOD**

```python
def f(arg1,
      arg2='answer to everything'):
    if arg1 == arg2:
        return 42
```

## Testing

**Code not tested is dysfunctional** and will not be accepted. Not without really good reasoning...
Seriously, tests are vital. Unit tests are meant for the module, Continuous Integration is meant for the scripts. If you have a great piece of code but having trouble with suitable tests, let us know.
Unit tests are preferred to doctests. The existing doctests will be converted to unit test in the future, see [this issue](https://github.com/dizak/mothulity/issues/67).
Data used for the testing purposes should be put in the ```test_data/```. Existing data in the ```tests/``` directory will be moved to ```test_data/``` in the future.

## Installation for developmeant

mothulity is meant to be used after installation with pip. For local developmeant, please add /path/to/mothulity-scripts/ and /path/to/mothulity/embedded/executables to your $PATH.

## Mothulity Structure

### Python Files

Localization in the repository: ```mothulity/```

Localization after installation: ```bin/```

mothulity itself consists of 4 executables:

  - ```mothulity```
  - ```mothulity_fc```
  - ```mothulity_draw```
  - ```mothulity_dbaser```

and 1 module:

  - ```utilities.py```

The scripts cannot contain any function definition besides ```main```. If anything else is needed - it should be defined in the ```utilities.py``` module and imported from there.

### [Mothur](https://mothur.org/wiki/Main_Page) Binaries

Localization in the repository: ```bin/```

Localization after installation: ```bin/```

[Mothur](https://mothur.org/wiki/Main_Page) and its accompanying BLAST binaries are taken from the [Mothur repository](https://github.com/mothur/mothur).

### Config File

Localization in the repository: ```config/```

Localization after installation: ```config/```

Hard-coding should be avoided as much as possible. A human-readable config file should be used as a place for persistent storage.

### JavaScript

Localization in the repository: ```js/```

Localization after installation: ```js/```

Putting JavaScript code inside the [Jinja2](http://jinja.pocoo.org/docs/2.10/) templates is forbidden. ```js/``` directory is the place for it. To make the JavaScript file discoverable by mothulity, put its name in the ```config``` file inside the ```[js]``` section.

### Templates

Localization in the repository: ```templates/```

Localization after installation: ```templates/```

There are 3 functional templates at the momeant (```venn_diagrams_template.html.j2``` is not acually used anywhere yet):

  - ```preproc_template.sh.j2``` - from sequence preprocessing to OTU-clustering
  - ```analysis_template.sh.j2``` - running the actual analysis once the sequences are clustered into OTUs.
  - ```output_template.html.j2``` - final HTML report

To make the templates files discoverable by mothulity, put their name in the ```config``` file inside the ```[templates]``` section.

### Tests

Localization in the repository: ```tests/```

A place for the unit tests. Some test data still live under this directory but should be moved to ```test_data``` in the future.

### Data for Testing

Localization in the repository: ```test_data/```

Any data used for the purpose of testing should be placed there.

## Deployment

The deployment is managed by [Travis-CI](https://travis-ci.org). It is triggered by setting a version tag on branch master.
