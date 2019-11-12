#!/usr/bin/env python
#

import sys
import logging
import argparse

from PIL import Image, ImageDraw, ImageFont

log = logging.getLogger('exhibitcreator') 


def parseArguments():
    parser = argparse.ArgumentParser(description='Exhibit creator - convert text to image')

    parser.add_argument('-i', '--input', action='store', help='Input text file')
    parser.add_argument('-o', '--output', action='store', help='Output image file')
    parser.add_argument('-c', '--check', action='store_true', help='Check font size')
    parser.add_argument('-r', '--render', action='store_true', help='Render text into image')
    parser.add_argument('-f', '--font', action='store', help='Font to use for rendering')
    parser.add_argument('-s', '--fontsize', action='store', type=int, help='Font size to use for rendering')
    # TODO: This is intended to be temporary for test purposes as it's quicker than
    # writing all the code that will handle reading from file/stdin
    parser.add_argument('-t', '--text', action='store', help='Font to use for rendering')
    parser.add_argument('-d', '--debug', action='store_true', help='Turn on debugging')
    return parser.parse_args()


def fontForNameAndSize(fontName, fontSize):
    if fontName:
        font = ImageFont.truetype(fontName, fontSize)
    else:
        font = ImageFont.load_default()

    return font
    

def calculateTextSizeForFont(text, font):
    return font.getsize(text)

def addBorderToSize(size, border):
    return ( size[0]+border, size[1]+border ) 

def createImageWithText(text, font, fontSize):
    font = fontForNameAndSize(font, fontSize)
    textSize = calculateTextSizeForFont(text, font)

    log.debug('Text size: %s', textSize)
    imageSize = addBorderToSize(textSize, 10) # TODO: Remove hard-coded border
    log.debug('Image size: %s', imageSize)

    image = Image.new('RGB', imageSize, color = 'white')

    log.debug('Creating drawing object')
    draw = ImageDraw.Draw(image)

    log.debug('Drawing text')
    draw.text((5,5), text, font=font, fill='black') # TODO: Remove hard-coded location
    
    return image


    

# ########### #
# MAIN SCRIPT #
# ########### #

if __name__ == '__main__':
    arguments = parseArguments()

    if arguments.debug:
        log.setLevel(logging.DEBUG)
        log.debug("Enabled debugging")
        log.addHandler(logging.StreamHandler(sys.stderr))
    
    log.debug("Arguments: %s", arguments)


if arguments.check:
    font = fontForNameAndSize(arguments.font, arguments.fontsize)
    result = calculateTextSizeForFont(arguments.text, font)
    print("Size is: ", result)


if arguments.render:
    image = createImageWithText(arguments.text, arguments.font, arguments.fontsize)
    image.save(arguments.output)


    

