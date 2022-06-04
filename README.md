# Sploinkd
A collection of scripts that I use.
Python <= 3.7 required.

Whenever I need something to be automated by a script I add it here.

## Installation
### UNIX systems
```bash
pip3 install git+https://github.com/Euab/sploinkd.git#egg=spolinkd
```
### Windows
```bash
pip install git+https://github.com/Euab/sploinkd.git#egg=sploinkd
```
There's also an `install.bat` file which you can run instead.

## Stuff
### Line counter
```
usage: loc.py [-h] [-v] [-nM] project

positional arguments:
  project              The path to the project to scan.

options:
  -h, --help           show this help message and exit
  -v, --verbose        Run loc in Verbose mode.
  -nM, --node-modules  Add this flag to include node_modules in search.
```
####Example:
```bash
python3 -m sploinkd.loc ./myAwesomeProject
```
Output:
```
LOC Copyright (C) 2022, Euan Mills. All Rights Reserved.

Scanning directories...
Computing line count...

Project "/Users/euab/myAwesomeProject" has 2129 lines.
Processed 48 files with 0 errors. (error rate: 0.00%)
```

## Normalise line endings project-wide:
```
usage: le.py [-h] [-v] [-lf] [-crlf] [-c] project

positional arguments:
  project        The path the the project where the requested operation should
                 be performed.

options:
  -h, --help     show this help message and exit
  -v, --verbose  Run le in verbose
  -lf            Convert to LF
  -crlf          Convert to CRLF
  -c, --check    Check line endings only
```
### Example
Normalise all line endings to use CRLF.
In this example all the line endings in the Linux kernel are changed to CRLF.
```bash
python3 -m spolinkd.le ~/linux -crlf
```
Output:
```
SploinkD LineEnder Copyright (C) 2022, Euan Mills. All rights reserved.
Discovering files...
Converting 59811 files...

Processed 59811 files with 0 errors. (error rate: 0.00%)

Process completed. Time elapsed: 105s
```
