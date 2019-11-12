#!/usr/bin/env python
#

import sys
import logging
import argparse
import attr

from PIL import Image, ImageDraw, ImageFont

log = logging.getLogger('exhibitcreator') 

class DefaultInteger:
    def __call__(self, argument):
        if type(argument) == int:
            return argument
        else:
            return 0
    
defaultInteger = DefaultInteger()
        
@attr.s(slots = True)
class RenderSettings:
    border = attr.ib(type=int, converter=defaultInteger)
    padding = attr.ib(type=int, converter=defaultInteger)
    fontfile = attr.ib(type=str)
    fontsize = attr.ib(type=int, converter=defaultInteger)
    width = attr.ib(type=int, converter=defaultInteger)
    height = attr.ib(type=int, converter=defaultInteger)

    def isAutoScale():
        return ( (not bool(width)) or (not bool(height)) )


def parseArguments():
    parser = argparse.ArgumentParser(description='Exhibit creator - convert text to image')

    parser.add_argument('-i', '--input', action='store', help='Input text file')
    parser.add_argument('-o', '--output', action='store', help='Output image file')
    parser.add_argument('-c', '--check', action='store_true', help='Check font size')
    parser.add_argument('-r', '--render', action='store_true', help='Render text into image')
    parser.add_argument('-f', '--fontfile', action='store', help='Font to use for rendering')
    parser.add_argument('-s', '--fontsize', action='store', type=int, help='Font size to use for rendering')
    # TODO: This is intended to be temporary for test purposes as it's quicker than
    # writing all the code that will handle reading from file/stdin
    parser.add_argument('-t', '--text', action='store', help='Font to use for rendering')
    parser.add_argument('-b', '--border', action='store', type=int, help='Border width')
    parser.add_argument('-p', '--padding', action='store', type=int, help='Padding around text')
    
    parser.add_argument('-x', '--width', action='store', type=int, help='Width to use for image')
    parser.add_argument('-y', '--height', action='store', type=int, help='Height to use for image')
    parser.add_argument('-mw', '--maxwidth', action='store', type=int, help='Max width to use for checking image')
    parser.add_argument('-mh', '--maxheight', action='store', type=int, help='Max height to use for checking image')
    parser.add_argument('-d', '--debug', action='store_true', help='Turn on debugging')
    return parser.parse_args()


def fontForNameAndSize(fontfile, fontSize):
    if fontfile:
        font = ImageFont.truetype(fontfile, fontSize, layout_engine = ImageFont.LAYOUT_RAQM)
    else:
        font = ImageFont.load_default()

    return font

def findIndexOfLongestLine(text):
    longestIndex = 0
    index = 0
    size = 0
    for line in text:
        length = len(line)
        if length > size:
            size = length
            longestIndex = index
        index += 1

    return longestIndex


def calculateTextMetricsForFont(text, font):
    longestLine = findIndexOfLongestLine(text)
    log.debug('Index of longest line: %s', longestLine)
    sizeForOneLine = font.getsize(text[longestLine])
    sizeForAllLines = ( sizeForOneLine[0], sizeForOneLine[1] * len(text))
    return (sizeForOneLine, sizeForAllLines)


def addAllAroundToSize(size, around):
    total = around * 2
    return ( size[0]+total , size[1]+total )


def calculateTotalImageSizeForTextSize(textSize, renderSettings):
    log.debug('Text size: %s', textSize)
    textSize = addAllAroundToSize(textSize, renderSettings.padding)
    log.debug('Text size after padding: %s', textSize)
    textSize = addAllAroundToSize(textSize, renderSettings.border)
    log.debug('Text size after border: %s', textSize)
    return textSize


def isImageSizeGreaterThanMaximum(text, renderSettings, maximum):
    font = fontForNameAndSize(renderSettings.fontfile, renderSettings.fontsize)
    textSize = calculateTotalImageSizeForText(text, font, renderSettings)
    log.debug('Total size: %s, max size: %s', textSize, maximum)
    result = (textSize[0] > maximum[0] or textSize[1] > maximum[1])
    log.debug('Is image size greater than maximum: %d', result)
    return result


def drawLinesAroundBorder(draw, topLeftX, topLeftY, bottomRightX, bottomRightY):
        
    # Horizontal line at the top
    draw.line((topLeftX, topLeftY, bottomRightX, topLeftY), width=1, fill='black')

    # Horizontal line at the bottom
    draw.line((topLeftX, bottomRightY, bottomRightX, bottomRightY), width=1, fill='black')

    # Vertical line at the left
    draw.line((topLeftX, topLeftY, topLeftX, bottomRightY), width=1, fill='black')

    # Vertical line at the right
    draw.line((bottomRightX, topLeftY, bottomRightX, bottomRightY), width=1, fill='black')


def createImageWithText(text, renderSettings):
    font = fontForNameAndSize(renderSettings.fontfile, renderSettings.fontsize)
    lineSize, textSize = calculateTextMetricsForFont(text, font)
    imageSize = calculateTotalImageSizeForTextSize(textSize, renderSettings)

    log.debug('Metrics: textSize: %s, lineSize: %s', textSize, lineSize)
    log.debug('Creating image with size: %s', imageSize)
    image = Image.new('RGB', imageSize, color = 'white')

    log.debug('Creating drawing object')
    draw = ImageDraw.Draw(image)

    textOffset = renderSettings.padding + renderSettings.border
    textRange = range(0, len(text))
    
    for offset in textRange:
        textLocation = ( textOffset, textOffset + (offset * lineSize[1]) )
        draw.text(textLocation, text[offset], font=font, fill='black')

    maxx = imageSize[0] - 1
    maxy = imageSize[1] - 1

    borderRange = range(0,renderSettings.border)
    for offset in borderRange:
        topLeftX = offset
        topLeftY = offset
        bottomRightX = maxx - offset
        bottomRightY = maxy - offset
        drawLinesAroundBorder(draw, topLeftX, topLeftY, bottomRightX, bottomRightY)
        
    return image



##
#
# Check the size of the rendered image against a maximum width and height.
#
# Takes into account the border and padding settings as well as font,
# size, and the actual text that needs to be created.
#
def checkImageSizeAgainstMaximum(text, renderSettings, maximum):
    imageTooBig = isImageSizeGreaterThanMaximum(text, renderSettings, maximum)
    log.debug('Image size is too big, exiting with value of 1')
    sys.exit(1)


##
#
# Render the text into an image using the given settings
#
# Adds the border and padding values to the size of the
# text block before rendering the full image.
#
def renderImageFromTextAndSettings(text, renderSettings):
    return createImageWithText(text, renderSettings)



# ########### #
# MAIN SCRIPT #
# ########### #

if __name__ == '__main__':
    arguments = parseArguments()

    if arguments.debug:
        log.setLevel(logging.DEBUG)
        log.debug("Enabled debugging")
        log.addHandler(logging.StreamHandler(sys.stderr))
    
    log.debug('Arguments: %s', arguments)

renderSettings = RenderSettings(
    border = arguments.border,
    padding = arguments.padding,
    fontfile = arguments.fontfile,
    fontsize = arguments.fontsize,
    width = arguments.width,
    height = arguments.height)

log.debug('Render settings: %s', renderSettings)

if arguments.check:
    log.debug('Checking image size')
    maximum = (arguments.maxwidth, arguments.maxheight)
    log.debug('Checking against maximum: %s', maximum)
    checkImageSizeAgainstMaximum(arguments.text, renderSettings, maximum)


if arguments.render:
    if (not arguments.text) and (not arguments.input):
        print('No input text provided, exiting')
        exit(-1)
        
    textToRender = []   

    if arguments.text:
        textToRender += arguments.text
    else:
        with open(arguments.input, 'r') as file:
            textToRender = file.readlines()
            
    image = renderImageFromTextAndSettings(textToRender, renderSettings)
    image.save(arguments.output)


    

