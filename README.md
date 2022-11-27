# LinuxManDumper
An experimental side project which uses a python file to dump (nearly) every single C library function defined in the linux api inside a structured JSON file.

## Usage
To use the parser you must first concatenate all the man pages using `zget` in the `/usr/share/man/manX`, where X is the manual section.

> Notice: this was only tested with the 3rd section of the linux manuals, use at your own risk on other manuals

- Then you simply run `python3 parse.py` on the concatenated manual text file, i.e `python3 parse.py man.txt`

## Bugs / Notices
- For now, the program skips functions that have a badly formatted name
- This program might skip some functions with custom return types

- The program was written over the course of a day, so it is not really optimized, but it works. Feel free to optimize it at your needs.

## Purpose
- This project to generate a JSON file for **Sublime Text autocompletion** (Using `sublime-intellitip`)

![image](https://user-images.githubusercontent.com/57685496/204114306-1df9fb29-5461-4e9b-b830-ad7dee4d95d4.png)







