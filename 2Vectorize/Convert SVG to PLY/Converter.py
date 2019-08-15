import Vector3
import EarClipMethod
import numpy as npy
import matplotlib.pyplot as plt
import triangle

#region Open and Create the files

SVGfile = open("SVGimage.svg", "r")
PLYfile = open("PLYimage.ply", "w+")

#endregion

#region Global Variables

#EAR CLIP
vertices2DArray = [[]] #Vertex array of the points from each entry of vertices from the the SVG file for a grouped colour
tris = []              #List of tris converted from the SVG vertices for the creating the PLY file

#TRIANGULATE
verticesArray = []     #Vertex array for the Triangulate method
triangles = []         #Triangle array for the Triangulate method

#PROPERTIES
numOfVertex = 0        #Number of Vertices
numOfFaces = 0         #Number of Faces
orderOfFaces = 0       #Order of the Faces
coloursArray = []      #Colour Array for each group of points

sizeMultiplier = 1 #0.001 #Scales the end result to make it viewable on Graphic Programs

#endregion

# region Functions

def ParseSVGtoVector3():  # Converts the SVG into Vectors
    """Converts the SVG into Vectors"""
    stringfile = []
    stringfile = SVGfile.readlines()

    for sf in stringfile:
        if (sf.find('fill=') > 1):
            ColourIndex = sf.find('fill=') + 7
            ColourString = sf[ColourIndex:ColourIndex+6]
            coloursArray.append(ConvertHEXtoRGB(ColourString))
        if (sf.find(' d=') > 1):
            VectorIndex = sf.find(' d=') + 7
            VectorString = (sf[VectorIndex:len(sf)-7])
            # ConvertSVGVertexPointsToVector3(VectorString) #EAR CLIP METHOD
            # CreateTrisAndProperties(len(coloursArray)-1)  #EAR CLIP METHOD
            ConvertSVGVertexPointsToTris(VectorString)
            # WritesPLYFile()

    SVGfile.close()

    return None


def ConvertHEXtoRGB(cstring):
    """Converts HEX colour information into RGB values in a tuple"""
    return tuple(int(cstring[i:i+2], 16) for i in (0, 2, 4))

#region EarClip Method

def ConvertSVGVertexPointsToVector3(vstring): #FOR EAR CLIP METHOD
    """Converts the 2D vertex points of the SVG into a Vector3 format"""
    x = ''
    y = ''
    xy = False #Flips between entering x values and y values

    vstring = str.replace(vstring,' L ',' ')
    vstring = str.replace(vstring,' C ',' ')
    vstring = str.replace(vstring,' M ',' ')

    vstringLength = len(vstring)

    for j in range(vstringLength):
        if (vstring[j] == ' '):
            xy = not xy
            if (xy == False):
                vertices2DArray[len(coloursArray)-1].append(Vector3.Vector3(float(x)*sizeMultiplier,float(y)*sizeMultiplier,0.0))                                
                x = ''
                y = ''
            continue
        if (xy == False):
            x += vstring[j]
        if (xy == True):
            y += vstring[j]

    vertices2DArray.append([])

def CreateTrisAndProperties(verts):
    """Converts the vertices into triangles and creates the properties for the PLY"""
    global numOfVertex
    global numOfFaces
    
    if (len(vertices2DArray[verts]) <= 3):
        tris.append(vertices2DArray[verts])
    else:
        tris.append(EarClipMethod.EarClipping(vertices2DArray[verts]))  #NEED TO ADD 0.0 for Z axis
    numOfVertex += len(tris[verts]*3)
    numOfFaces += len(tris[verts])

def WritesPLYFile():     #Writes the PLY file and exports it as PLYimage.ply
    """Writes the PLY file"""

    #\nproperty float nx\nproperty float ny\nproperty float nz
    #" 0.0 0.0 -1.0 "+

    PLYfile.write("ply\nformat ascii 1.0\n")                      #Preprocessor for PLY file
    PLYfile.write("element vertex "+str(numOfVertex)+"\n")        #Number of Vertices
    PLYfile.write("property float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\n")       #Add the properties
    PLYfile.write("element face "+str(numOfFaces)+"\n")           #Number of Faces                   
    PLYfile.write("property list uchar uint vertex_indices\nend_header\n")    #More Property information
    
    for j in range(len(tris)):
        for k in range(len(tris[j])):
            for l in range(len(tris[j][k])):
                PLYfile.write(str(tris[j][k][l][0])+" "+ \
                str(tris[j][k][l][1])+" "+ \
                str(tris[j][k][l][2])+" "+ \
                str(coloursArray[j][0])+" "+ \
                str(coloursArray[j][1])+" "+ \
                str(coloursArray[j][2])+"\n")

    for i in range(numOfVertex):
        if (i == 0):
                PLYfile.write("3 "+str(i))
                continue
        if ((i % 3) != 0):
                PLYfile.write(" "+str(i))
        else:
                PLYfile.write("\n3 "+str(i))

    PLYfile.close()
    return None       

# endregion

#region Triangulate Method

def ConvertSVGVertexPointsToTris(vstring):
    """Converts the 2D vertex points of the SVG into Tris with Triangulate"""
    global numOfVertex
    global numOfFaces

    x = ''
    y = ''
    xy = False #Flips between entering x values and y values

    vstring = str.replace(vstring,' L ',' ')
    vstring = str.replace(vstring,' C ',' ')
    vstring = str.replace(vstring,' M ',' ')

    vstringLength = len(vstring)

    for j in range(vstringLength):
        if (vstring[j] == ' '):
            xy = not xy
            if (xy == False):                
                verticesArray.append((float(x),float(y)))
                x = ''
                y = ''
            continue
        if (xy == False):
            x += vstring[j]
        if (xy == True):
            y += vstring[j]

    triangles.append(triangle.triangulate({'vertices': verticesArray}))

    numOfVertex += len(verticesArray)
    numOfFaces += len(triangles[len(coloursArray)-1]['triangles'])
    
    verticesArray.clear()

def SVGtoPLYFileTriangulate():
    """Writes the PLY file with the Triangulate method"""

    global orderOfFaces

    PLYfile.write("ply\nformat ascii 1.0\n")                      #Preprocessor for PLY file
    PLYfile.write("element vertex "+str(numOfVertex)+"\n")        #Number of Vertices
    PLYfile.write("property float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\n")       #Add the properties
    PLYfile.write("element face "+str(numOfFaces)+"\n")           #Number of Faces                   
    PLYfile.write("property list uchar uint vertex_indices\nend_header\n")    #More Property information
    
    for j in range(len(coloursArray)):        
        for k in range(len(triangles[j]['vertices'])):
            PLYfile.write(str(triangles[j]['vertices'][k][0])+" "+ \
            str(triangles[j]['vertices'][k][1])+" "+ \
            str(0.0)+" "+ \
            str(coloursArray[j][0])+" "+ \
            str(coloursArray[j][1])+" "+ \
            str(coloursArray[j][2])+"\n")

    for i in range(len(triangles)):
        if (i != 0):
            orderOfFaces += len(triangles[i-1]['vertices'])
        for p in range(len(triangles[i]['triangles'])):
            PLYfile.write("3 "+str(triangles[i]['triangles'][p][0]+orderOfFaces)+" "+ \
            str(triangles[i]['triangles'][p][1]+orderOfFaces)+" "+ \
            str(triangles[i]['triangles'][p][2]+orderOfFaces)+"\n")

    PLYfile.close()
    return None

# endregion

# endregion

# region Convert SVG to PLY file

ParseSVGtoVector3()
SVGtoPLYFileTriangulate()

# endregion

# #EXPERIMENT HERE

# C = [(1.0,2.0),(1.2,3.2)]   #DIS ONE
# B = dict(vertices=npy.array(((0, 0), (1, 0), (1, 1), (0, 1))))
# testsererw = npy.array(vertices2DArray[0][0:len(vertices2DArray[0])])
# # A = dict(vertices=npy.array((vertices2DArray[0][0:len(vertices2DArray[0])])))
# A = dict(vertices=npy.array((verticesArray)))   #DIS IS THE ONE


# teerer = [[vertices2DArray[0]]]
# tester = dict([('vertices', teerer)])

# spiral = triangle.get_data('spiral')
# #IN A SENSE THE TRIANGLES ARE CREATING THE FACES FROM THE VERTICES
# t = triangle.triangulate({'vertices': verticesArray})   #BOTH OF THESE TRIANGLES THE ORDER FOR MAKING THE TRIANGLES
# t2 = triangle.triangulate(A)    #BOTH OF THESE TRIANGLES THE ORDER FOR MAKING THE TRIANGLES
# t['vertices'].tolist()

# print (t['vertices'].tolist())
# print (t2['vertices'].tolist())
# print ('WHAT')
# #EXPERIMENT HERE