# LinuxManDumper
An experimental side project which uses a python file to dump functions defined in (a) man page(s) inside a structured JSON file.

## Usage
1. To dump multiple man files, you must concatenate all the man pages using `zget` in the `/usr/share/man/manX` directory, where X is the manual section. In other cases, you can simply pass one file inside the manual section to the program.

> Notice: this was only tested on section 3 of the linux manuals, use at your own risk on other manuals

2. Then you can simply run `python3 parse.py` on the manual text file, i.e `python3 parse.py man.txt`

## Notice
- The program was written over the course of a day, so it is not really optimized, but it works. Feel free to optimize it further.

## Bugs
- For now, the program skips some functions due to some formatting bugs.
- The program also skips some functions with custom return types.

## Purpose
- This project utilized to dump (nearly) every single C standard library function defined on linux in a JSON.
- This JSON was then used for **Sublime Text autocompletion** (Using `sublime-intellitip`)

![image](https://user-images.githubusercontent.com/57685496/204114306-1df9fb29-5461-4e9b-b830-ad7dee4d95d4.png)







