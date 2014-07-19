# Rhino.Python-MakeBox

Rhino.Python script to generate a press-fit box for a quick fabrication and assembly

#### Built and Tested with:
[Rhino 5 for mac](http://www.rhino3d.com/mac)
[CodeRunner](http://krillapps.com/coderunner/)
 
## Run
#### on mac:
* Follow the instruction [here](http://wiki.mcneel.com/rhino/mac/python) to run python scripts in Rhino.
* Place MakeBox.py in ~/Library/Application\ Support/McNeel/Rhinoceros/Scripts/
* Open Rhino and make a new model. Type 'RunPythonScript' into command box and select MakeBox.py
* Follow the command to set parameters for the box generation

## Tolerance reference
#### Laser cutting:
* Masonite 3mm thick - 0.01 inch
	
## TODO
* Set maximum number of segments the box can have based on the size of a box and tolerance
* Test on Rhino 5 for Windows
* Put example box images for README.md to show what this script generates

## License 

MIT License applies to this code repository

    Copyright (C) 2014 Akito van Troyer
        
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
    the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
    IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.