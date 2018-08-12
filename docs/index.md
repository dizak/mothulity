---
layout: default
---


[![Build Status](https://travis-ci.org/dizak/mothulity.svg?branch=master)](https://travis-ci.org/dizak/mothulity)


# mothulity


Run your 16S/ITS **analysis** with a **single command**

Install your **dependencies** running a single script and **no root**

**Easily** queue your job on a **computing cluster**

Now it is **possible** and **easy** with ```mothulity```!


## Install


```bash
pip install mothulity
```


## Run!


### Locally...


```bash
mothulity /where/your/project/lives -r bash
```


### ...or with Slurm


```bash
mothulity /where/your/project/lives -r sbatch
```
