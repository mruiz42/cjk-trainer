# CJK-Trainer
A program geared towards native English speakers to facilitate language vocabulary building. However, I want this to be as modular as possible, so that any language can be studied using this software.

![alt text](https://i.imgur.com/7hdBY8a.png)

![alt text](https://i.imgur.com/tzed8c5.png)

![alt text](https://i.imgur.com/NckF65m.png)
Previously based on PyQt5, transitioned to PySide2 as it is now the officially supported python binding for the  qt framework.


# Install notes
$ pip install pyside2

$ python3 callMainWindow.py

It may be necessary to modify defined file paths in the code, since it may use a different path directory.
(currently working on this)


# Dependencies
Python3
SQLite3
Pyside2



# Developer Notes
The following keywords are in place and will have a general meaning throughout this program:
Vocab - The vocabulary word being learned, is a foreign word to user
Pronun - Pronunciation of the word (foreign), if applicable (ie. pinyin, romanji, etc.)
Definition - Native definition of vocabulary word in user's native language.


# Licensing
MIT License

Copyright (c) 2019 Michael Ruiz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
