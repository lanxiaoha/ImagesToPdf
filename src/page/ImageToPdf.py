import functools
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter


def supportFile(filename):
    return filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg")

def sortFileName(filename1:str,filename2:str):
    first = filename1.split(".")[0]
    second = filename2.split(".")[0]
    first = first.replace("_",".",1)
    first = first.replace("_","")
    second = second.replace("_",".",1)
    second = second.replace("_","")
    try:
        first = float(first)
        second = float(second)
        if first > second:
            return 1
        elif first < second:
            return -1
        else:
            return 0
    except:
        return 1


def exportPdfFile(folder_path:str,scale:float= 1.5,directNewPage = True,autoScale:float = 1.7):
    resultPath = os.path.join(folder_path, "result.pdf")

    maker = canvas.Canvas(resultPath)
    pageWidth = A4[0]
    pageHeight = A4[1]
    print("pageWidth", pageWidth)
    print("pageHeight", pageHeight)

    namelist = os.listdir(folder_path)
    filterNameList = []
    for filename in namelist:
        if supportFile(filename):
            filterNameList.append(filename)

    filterNameList.sort(key= functools.cmp_to_key(sortFileName))
    print(filterNameList)

    maxWidth = 0
    maxHeight = 0
    for filename in filterNameList:
        if supportFile(filename):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            width = img.width
            height = img.height
            if width > maxWidth:
                maxWidth = width
            if height > maxHeight:
                maxHeight = width

    widthScale = maxWidth / pageWidth
    if widthScale < 1:
        widthScale = 1
    heightScale = maxHeight / pageHeight
    if heightScale < 1:
        heightScale = 1

    needScale = max(widthScale, heightScale)
    needScale = needScale * scale

    print("needScale", needScale, "widthScale", widthScale, "heightScale", heightScale)
    heightOffset = 0

    for filename in filterNameList:
        if supportFile(filename):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            width = img.width
            height = img.height
            print("image",filename, width, "height", height)
            y = heightOffset + height / needScale
            yPos = pageHeight - y
            if yPos <= 0:

                if directNewPage:
                    print("下一页")
                    maker.showPage()
                    heightOffset = 0
                    y = heightOffset + height / needScale
                    yPos = pageHeight - y
                    maker.drawImage(img_path, x=10, y=yPos, width=width / needScale, height=height / needScale,
                                    preserveAspectRatio=True)
                    heightOffset += height / needScale
                else:
                    bakNeedScale = needScale
                    needScale = needScale * autoScale

                    y = heightOffset + height / needScale
                    yPos = pageHeight - y
                    if yPos <=0:
                        print("下一页")
                        maker.showPage()
                        heightOffset = 0
                        needScale = bakNeedScale
                        y = heightOffset + height / needScale
                        yPos = pageHeight - y
                        maker.drawImage(img_path, x=10, y=yPos, width=width / needScale, height=height / needScale,
                                        preserveAspectRatio=True)
                        heightOffset += height / needScale
                    else:
                        maker.drawImage(img_path, x=10, y=yPos, width=width / needScale, height=height / needScale,
                                        preserveAspectRatio=True)
                        maker.showPage()
                        heightOffset = 0

                    needScale = bakNeedScale

            else:
                maker.drawImage(img_path, x=10, y=yPos, width=width / needScale, height=height / needScale,
                            preserveAspectRatio=True)
                heightOffset += height / needScale

    maker.save()
