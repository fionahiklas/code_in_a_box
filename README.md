## Overview

Simple utility to convert UTF-8 text into a PNG image with a black 2 pixel border.


## Quickstart

### Finding the size of text

```
python exhibitcreator.py -f fonts/FiraMono/FiraMono-Regular.ttf -s 12 -c -t "Hello World" -mw 100 -mh 200
```

### Rendering of simple text

```
python exhibitcreator.py -f fonts/FiraMono/FiraMono-Regular.ttf -s 12 -r -t "Hello World" -o helloWorld.png -d
```

### Rendering with border and padding

```
python exhibitcreator.py -f fonts/FiraMono/FiraMono-Regular.ttf -s 12 -r -t "Hello World" -o helloWorld.png -d -p 10 -b 7
```


### Rendering text from a file

```
python exhibitcreator.py -f fonts/FiraMono/FiraMono-Regular.ttf -s 12 -r -o helloWorld.png -d -p 3 -b 2 -i tests/test.txt
```


## Parameters

See the output from `exhibitcreator.py -h` for up-to-date command usage information

```
usage: exhibitcreator.py [-h] [-i INPUT] [-o OUTPUT] [-c] [-r] [-f FONTFILE]
                         [-s FONTSIZE] [-t TEXT] [-b BORDER] [-p PADDING]
                         [-x WIDTH] [-y HEIGHT] [-mw MAXWIDTH] [-mh MAXHEIGHT]
                         [-d]

Exhibit creator - convert text to image

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input text file
  -o OUTPUT, --output OUTPUT
                        Output image file
  -c, --check           Check font size
  -r, --render          Render text into image
  -f FONTFILE, --fontfile FONTFILE
                        Font to use for rendering
  -s FONTSIZE, --fontsize FONTSIZE
                        Font size to use for rendering
  -t TEXT, --text TEXT  Font to use for rendering
  -b BORDER, --border BORDER
                        Border width
  -p PADDING, --padding PADDING
                        Padding around text
  -x WIDTH, --width WIDTH
                        Width to use for image
  -y HEIGHT, --height HEIGHT
                        Height to use for image
  -mw MAXWIDTH, --maxwidth MAXWIDTH
                        Max width to use for checking image
  -mh MAXHEIGHT, --maxheight MAXHEIGHT
                        Max height to use for checking image
  -d, --debug           Turn on debugging
```


## Development 

### Create Virtual Environment

```
python3 -m venv matrix
. ./matrix/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```

### Fonts

Some are included under the `fonts` directory, see the references section to links.  This are all
Open Source TrueType fonts.  Any other TrueType fonts can be used.


## Notes

### ImageFont.getsize()

The `getsize()` method on the returned font object seems to calculate the width without issue but
it doesn't take into account the number of lines in the whole block of text when calculating the 
height.

A defect was apparently [raised for this](https://github.com/python-pillow/Pillow/issues/2966)

The proposed solution is to use `ImageDraw.Draw.textsize()` which does apparently consider the number
of lines.  The only problem with this approach is that you need to have an image from which to create
the Draw object.  This seems hacky and, for checking the size at least, there seems little point in 
creating the image.

The only work around I could find for this is to treat a block of text as an array of lines, find the
longest one, get the metrics for that line and then multiply the height up.  This seems to work and 
gets the job done but it might be nicer if this was available in the font engine.


### Draw.line() using width

I tried several attempts to calculate the correct coordinates for lines to be drawn around the border
so that they had uniform thickness all the way round.  It seems that there may be some magic 
calculation that can be done but I couldn't figure out what it was.  Getting the code working with a
border with of 7 it then failed on 2.

In the end the solution I came up with was to draw single pixel width lines multiple times at offsets
from the outside of the image area.  This seemed to work correctly.  Not an entirely elegant solution
but functional.


## References

### Python

* [Pillow Package](https://pypi.org/project/Pillow/)
* [Pillow docs](https://pillow.readthedocs.io/en/stable/)
* [PIL Tutorial](https://code-maven.com/create-images-with-python-pil-pillow)

### Fonts

* [OpenSource fonts](https://opensource.com/article/17/11/how-select-open-source-programming-font)
* [FirCode font](https://github.com/tonsky/FiraCode)
* [DejaVu fonts](https://dejavu-fonts.github.io/)
* [FiraMono](https://fonts.google.com/specimen/Fira+Mono)






