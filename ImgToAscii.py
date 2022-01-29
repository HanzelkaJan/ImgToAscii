import argparse

import numpy as np
from PIL import Image

gscale = "@%#*+=-:. "

def main():
    descStr = "Turns images into ASCII art"
    parser = argparse.ArgumentParser(description=descStr)

    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='fontScale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)

    args = parser.parse_args()

    imgFile = args.imgFile
    image = Image.open(imgFile).convert("L")

    outFile = "output.txt"
    if args.outFile:
        outFile = args.outFile
    output = open(outFile, 'w')

    fontScale = 0.43
    if args.fontScale:
        fontScale = float(args.fontScale)

    cols = 200
    if args.cols:
        cols = int(args.cols)

    ascii = imageToAscii(image, cols, fontScale)

    for row in ascii:
        output.write(row + "\n")


def imageToAscii(image, cols, scale):
    W,H = image.size[0], image.size[1]
    w = W/cols
    h = w/scale
    rows = H/h
    aimg = []

    if cols > W or rows > H:
        print("Image is too small for this many columns")
        exit(0)

    for j in range(int(rows)):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        if j == rows-1:
            y2 = H
        aimg.append("")
        for i in range(int(cols)):
            x1 = int(i * w)
            x2 = int((i + 1) * w)
            if i == cols - 1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))
            avg = getAverageShade(img)
            aimg[j] += gscale[int(avg/255*9)]

    return aimg

def getAverageShade(image):
    img = np.array(image)
    return np.average(img)


if __name__ == '__main__':
    main()