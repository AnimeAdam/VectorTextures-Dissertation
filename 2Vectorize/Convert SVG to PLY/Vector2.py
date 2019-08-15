import math

class Vector2:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def __str__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ")"
    
  def get_length(self):
    return math.sqrt(self.x ** 2 + self.y ** 2)
    
  def __add__(self, v):
    return Vector2(self.x + v.x, self.y + v.y)
    
  def __sub__(self, v):
    return Vector2(self.x - v.x, self.y - v.y)

  def __mul__(self, n):
    return Vector2(self.x * n, self.y * n)
	
  @staticmethod
  def dot_product(v1, v2):
    return (v1.x * v2.x + v1.y * v2.y)