from PIL import Image

#region Prints out colour information from image pixel by pixel

im = Image.open('image.png')    #gets the image and puts it into a Image Class object

pix_ar = im.load()       # load image into a PixelAccess Class object

numrows = im.width
numcols = im.height

print (im.format, im.size, im.mode, numrows, numcols)

i = 4
j = i % 0

print(j)

# for x in range (0, numcols):
#         for y in range (0, numrows):
#                         print (pix_ar[x,y])

#endregion