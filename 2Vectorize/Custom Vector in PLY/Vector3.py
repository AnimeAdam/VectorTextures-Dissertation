import math

class Vector3:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    
  def __str__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
    
  def get_length(self):
    return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
  def __add__(self, v):
    return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)
    
  def __sub__(self, v):
    return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)

  def __mul__(self, n):
    return Vector3(self.x * n, self.y * n, self.z * n)
        
  @staticmethod
  def dot_product(v1, v2):
    return (v1.x * v2.x + v1.y * v2.y + v1.z * v2.z)