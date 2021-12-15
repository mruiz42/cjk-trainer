# CJK-Trainer
A cross-platform flashcard study program to help learn foreign languages. Works on Windows/Mac/Linux using the qt-framework and python3. 
### NOTE: This project is not being actively maintained.
I wish I had time to finish this project and it was fun to make but I don't have the time to actively develop
or maintain it. Pull Requests are welcome, feel free to contact me.
# Screenshots
Linux Word List (Dark Theme)
![alt text](https://i.imgur.com/4kPtZYK.png)
Windows 10 Word List (Dark Theme)
![alt text](https://i.imgur.com/fseA91t.png)
Windows 10 Word List (Light Theme)
![alt text](https://i.imgur.com/ZV3hZyG.png)
Windows 10 Typing (Dark Theme)
![alt text](https://i.imgur.com/TGdY0jB.png)

# Runtime Dependencies
* Python3
* SQLite3
* Pyside2

# Development Requirements
* pipenv

# Install notes
* `$ pip install pyside2 OR pip -r install pip_requirements.txt`
* `$ python3 callMainWindow.py`
<br/>
OR
* `pipenv install`
* `pipenv shell`

There are currently no binaries being built, only source code files for now.

# Release Plan
* 1.0 Fully functioning
* 0.9 UI enhancements/bug squashing
* 0.8 Implement image handling to cards
* 0.7b Statistics module working + binaries available
* 0.6a Game modules fully functional 
CURRENT RELEASE -> 0.5a Data IO functioning between user interaction (cards table) and database

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
