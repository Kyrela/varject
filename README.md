# Varject

![PyPI - Implementation](https://img.shields.io/pypi/implementation/varject)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/varject)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/varject)

![GitHub Repo stars](https://img.shields.io/github/stars/kyrela/varject?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/kyrela/varject?style=social)
![GitHub followers](https://img.shields.io/github/followers/kyrela?style=social)

A simple and powerful configuration file system


## Features

- Easily create and import variables of any type
- Easily manipulate them : just use varject.variablename
- Insert commentaries, formatted text, text on multiple lines
- Specify variables type or even inject your own code on-fly without editing your python code
- Simple syntax

## Installing

**Python 3.6 or above is required**

### From Pipy

Just run the following command in your terminal :

```bash
pip install varject
```

### From manual installation

Download the .whl file from the last [release](https://github.com/Kyrela/varject/releases/) and run :
```bash
pip install filename.whl
```

where filename is the name of the .whl you downloaded, assuming you're in the directory where the .whl was downloaded.

You can also clone the repo and run this at the root of the project (only working for 3.7 or above):
```bash
pip install .
```

## Usage exemple

Code

```python
import varject

vj = varject.Varject("path_to_file.varj")

print(vj.test)
print(vj.mode * vj.instance_number)
```

Varject file (.varj, .vject, vj)

```
#----------- Main config -----------#
token            : 5J.4IjazAyMDM3.X0Ypxg.gajOhhNJSgedl0v5lHg0oY
prefix           : !
name             : test
filelogs         : logs/logs.txt
version          : 1.1.x
colour           : 0xD15620  : int
instance_number  : 56        : int


#----------- Core -----------#
id            : 751004191845203141   : int      # target id
check_time    : 2 * 60               : eval     # time between two checks
settings_file : config/server.config            # settings file
mode          : 1                    : int
debug         : True                 : bool

# mode 0 : disabled
# mode 1 : classic
# mode 2 : predictive

#----------- detailed params -----------#
description :

"A simple program for testing. It does :\n
\t- Nothing\n
\t- And that's all."

"list
elements" : 0 1 2 3 4 : var.split(" ") 
```