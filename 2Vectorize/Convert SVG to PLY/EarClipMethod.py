import math
import sys
from collections import namedtuple

#region Globals

VERTEXTUP = namedtuple('vertex', ['x', 'y'])
EPSILON = math.sqrt(sys.float_info.epsilon)

#endregion

#region Main Method

def EarClipping(vertices):
        """Creates tris from the set of vertices"""
#     if (len(vertices) == 100):
#             print(vertices)
        earVertex = []
        tris = []

        verticesCopy = list.copy(vertices)
        #[Vertex(*vertex) for vertex in vertices]

        if IsItClockwise(verticesCopy):
                verticesCopy.reverse()

        verticesLength = len(verticesCopy)
        for i in range(verticesLength):
                preIndex = i - 1
                preVertex = verticesCopy[preIndex]
                vertex = verticesCopy[i]
                nextIndex = (i + 1) % verticesLength
                nextVertex = verticesCopy[nextIndex]

                if IsItAEar(preVertex,vertex,nextVertex,verticesCopy):
                        earVertex.append(vertex)

        while earVertex and verticesLength >= 3:        #MAKE ANOTHER METHOD FOR NON-EAR POLYGONS
                ear = earVertex.pop(0)
                i = verticesCopy.index(ear)
                preIndex = i - 1
                preVertex = verticesCopy[preIndex]
                nextIndex = (i + 1) % verticesLength
                nextVertex = verticesCopy[nextIndex]

                verticesCopy.remove(ear)
                verticesLength -= 1
                tris.append(((preVertex.x, preVertex.y,0.0), (ear.x, ear.y,0.0), (nextVertex.x, nextVertex.y,0.0)))
                if verticesLength > 3:
                        prepreVertex = verticesCopy[preIndex - 1]
                        nextnextIndex = (i + 1) % verticesLength
                        nextnextvertex = verticesCopy[nextnextIndex]

                        groups = [
                                (prepreVertex, preVertex, nextVertex, verticesCopy),
                                (preVertex, nextVertex, nextnextvertex, verticesCopy),
                        ]
                        for group in groups:
                                V = group[1]
                                if IsItAEar(*group):
                                        if V not in earVertex:
                                                earVertex.append(V)
                                        elif V in earVertex:
                                                earVertex.remove(V)

        #Error checking for usually results
        if (tris == []):
                print (tris)
                print (verticesCopy)
                print (vertices)

        return tris

#endregion

#region Queries

def IsItClockwise(vertices):
    """Checks if the polygon is ordered clockwise"""
    i = 0
    verticesLength = len(vertices)
    for j in range(verticesLength):
        vertex = vertices[j]
        vertex1 = vertices[(j + 1) % verticesLength]
        i += (vertex1.x - vertex.x) * (vertex1.y + vertex.y) 
    return i > 0

def IsItAEar(v1,v2,v3,vertices):
    """Checks if the vertices are creating an ear"""
    ear = DoesItHaveNoVertices(v1,v2,v3,vertices) and \
    IsItConvex(v1,v2,v3) and \
    TriArea(v1.x,v1.y,v2.x,v2.y,v3.x,v3.y) > 0
    return ear

def DoesItHaveNoVertices(v1,v2,v3,vertices):
    """Checks if the vertices from the EarClipping contain a vertex"""
    for vNum in vertices:
        if vNum in (v1,v2,v3):
            continue
        elif IsItInside(vNum,v1,v2,v3):
            return False
    return True

def IsItInside(vNum,v1,v2,v3):
    """Checks if the vertices are inside"""
    area1 = TriArea(v1.x, v1.y, v2.x, v2.y, v3.x, v3.y)
    area2 = TriArea(vNum.x, vNum.y, v2.x, v2.y, v3.x, v3.y)
    area3 = TriArea(vNum.x, vNum.y, v1.x, v1.y, v3.x, v3.y)
    area4 = TriArea(vNum.x, vNum.y, v1.x, v1.y, v2.x, v2.y)
    areaDifference = abs(area1 - sum([area2, area3, area4])) < math.sqrt(sys.float_info.epsilon)
    return areaDifference

def IsItConvex(pre,vertex,next):
    """Checks if the vertices are convex"""
    return TriSum(pre.x, pre.y, vertex.x, vertex.y, next.x, next.y) < 0

#endregion

#region Algorithms

def TriArea(x1,y1,x2,y2,x3,y3):
    """Finds the area of the triangle"""
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def TriSum(x1, y1, x2, y2, x3, y3):
    """Finds the sum of the triangle"""
    return x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)

#endregion


