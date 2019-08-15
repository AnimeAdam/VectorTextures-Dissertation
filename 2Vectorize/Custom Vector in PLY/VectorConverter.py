from PIL import Image
import Vector3
import numpy as np

#This for converting the image into a sequence of quads

#region Global variables

im = Image.open('image.png')    #gets the image and puts it into a Image Class object
pix_ar = im.load()       # load image into a PixelAccess Class object
numcols = im.width          #the column of pixels
numrows = im.height         #the row of pixels
vertex3DArray = [[[]]]          #[y][x][vertex] first 2 contain each position contains the vertex information for the image
        #vertex3DArray.append (1)            # [[[]], 1]
        #vertex3DArray[0].append (1)         # [[[], 1]]
        #vertex3DArray[0][0].append (1)      # [[[1]]]
        #vertex3DArray[0].append ([[]])      # [[[], [[]]]]
facesOrder = []                 #Order of faces should be seperate into 4 for each vertex
#len(facesOrder)/4 finds the number of faces | len(facesOrder) number of vertices
sizeMultiplier = 0.001           #Multiplier for the size of the vector texture, from a base unit of 1

print (im.format, im.size, im.mode, numrows, numcols, pix_ar[0,0])   #prints image information
#endregion

#region Functions

def CreateVertexArray(x, y): #Creates Vertexes for the vector image
    """Adds the vertex for each pixel"""
    if (x == 0 and y == 0):        
        for j in range (0,4):
                vertex3DArray[y][x].append (CreateVertexPoint(j,x,y))
                CreateFaces()
        return None
    if (y+1 > len(vertex3DArray)):
        vertex3DArray.append([[]])
        for j in range (0,4):
                vertex3DArray[y][x].append (CreateVertexPoint(j,x,y))
                CreateFaces()
        return None
    if (x+1 > len(vertex3DArray[y])):
        vertex3DArray[y].append([])
        for j in range (0,4):
                vertex3DArray[y][x].append (CreateVertexPoint(j,x,y))
                CreateFaces()
        return None
    return None

def CreateVertexPoint(pos, x, y): #pos = The vextex order for each pixel for quads
        """Creates the vertex points"""
        if (pos == 0):
                return Vector3.Vector3((0.0+x)*sizeMultiplier,(0.0-y)*sizeMultiplier,0.0)
        if (pos == 1):
                return Vector3.Vector3((1.0+x)*sizeMultiplier,(0.0-y)*sizeMultiplier,0.0)
        if (pos == 2):
                return Vector3.Vector3((1.0+x)*sizeMultiplier,(-1.0-y)*sizeMultiplier,0.0)
        if (pos == 3):
                return Vector3.Vector3((0.0+x)*sizeMultiplier,(-1.0-y)*sizeMultiplier,0.0)
        
def CreateFaces(): #Creates the face order
        """Creates the face order"""
        facesOrder.append(len(facesOrder))

def WritesPLYFile():     #Writes the PLY file and exports it as Image.ply
        """Writes the PLY file"""
        numOfVertex = len(facesOrder)           #Number of Vertices
        numOfFaces = int(len(facesOrder)/4)          #Number of Faces

        #\nproperty float nx\nproperty float ny\nproperty float nz
        #" 0.0 0.0 -1.0 "+

        f = open("image.ply","w+")

        f.write("ply\nformat ascii 1.0\n")                      #Preprocessor for PLY file
        f.write("element vertex "+str(numOfVertex)+"\n")        #Number of Vertices
        f.write("property float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\n")       #Add the properties
        f.write("element face "+str(numOfFaces)+"\n")           #Number of Faces                   
        f.write("property list uchar uint vertex_indices\nend_header\n")    #More Property information
        for y in range (0, numrows):
                for x in range (0, numcols):
                        for j in range (0,4):
                                #Vertex information
                                f.write(str(vertex3DArray[y][x][j].x)+" "+ \
                                str(vertex3DArray[y][x][j].y)+" "+ \
                                str(vertex3DArray[y][x][j].z)+" "+ \
                                str(pix_ar[x,y][0])+" "+ \
                                str(pix_ar[x,y][1])+" "+ \
                                str(pix_ar[x,y][2])+"\n")
        for i in facesOrder:
                if (i == 0):
                        f.write("4 "+str(i))
                        continue
                if ((i % 4) != 0):
                        f.write(" "+str(i))
                else:
                        f.write("\n4 "+str(i))

        f.close()
        return None

#endregion

#region Converting to a Vector image

for y in range (0, numrows):
    for x in range (0, numcols):
        CreateVertexArray(x,y) #vertex3DArray[x][y].insert(x, Vector3.Vector3)

#endregion

#region Create PLY file

WritesPLYFile()

#endregion