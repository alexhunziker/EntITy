# EntITy - Entlich Programmieren
Entity enables programming with ducks. It is a -some would say silly- python based programing language.

## Why should I use EntITy?
Because it allows you to write code with colorful ducks!

## How can it be used?
EntITy requires python and tk to be installed.

In order to write your EntITy Program, click on the duck icons to add new ducks to your program. The following ducks are available:

* Control Duck (green): Enables to check for a condition and specify which duck(s) to execute if the condition is true or false
* Loop Duck (pink): Enables to create loops (currently while loops only, for loop not implemented yet), by checking for a condition and specifying duck(s) to execute as long as condition evaluates to true
* Block Duck (blue): Enables to execute (python) code, and specify which duck to execute after (default: next duck, linear)
* End Duck (yello): Signals the end of a linear code execution sequence (i.e. end of program/"function")

If no duck is specified with which to continue, the program is executed in a linear fashion.

The code can be executed by clicking on the "Run" icon. Code blocks can be edited by moving the cursor over them. Furthermore code blocks can be exchanged by clicking the "move left" or "move right" icons. The delete icon deletes the current duck

Please note: Currently only the regular console output is written to the console area. The error messages can be found in the regular python terminal.


## How does it work?
EntITy is a Graphical Programming tool written in python with tk for the interface. 
The program code is stored as a sequence of different ducks and there properties. On execution the ducks are converted into python code and executed.

## Licence
The project is licenced under GPLv3
