# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************
import maya.cmds as cmds

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with a variabale name and the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions print out and store the data in the cube (translate, rotate, scale and color)

2. CREATE 3 cube objects with different names (use __init__(name)).

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats: e.g. [1.2, 2.4 ,3.7]
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your cube class.
   Update the cube class to not repeat the content of Object.

NOTE: Upload only the final result.


"""
#*************************************************************
#PARENT CLASS
class Object():
   def __init__(self):


   # self needs to be the first argument
   def print_infos(self):
      print("{} : {}".format(self.name, self.color))

   def store_data(self):

   def update_transform(ttype, value):
      pass

   def print_Status(self):
      pass

#*************************************************************
# CLASS with __init__
class Cube(Object):
   # initialize class
   def __init__(self):
      super(Cube, self).__init__( name, translate=(0,0,0), rotate=(0,0,0), scale=(0,0,0), color=[0,0,0])

      self._name     = name
      self.translate = translate
      self.rotate    = rotate
      self.scale     = scale
      self.color     = color
      
      #self.print_infos()
   
   
   cube = cmds.polyCube( 'polyCube1', n=self._name, w=True )
   cmds.xform(cube, t=)




#*************************************************************
# EXAMPLE
'''
pillar_stone = Cube(name="pillar", color="grey")
fire_stone = Cube(name="fire_stone", color="red")

# override
pillar_stone.color = "black"
pillar_stone.print_infos()
'''

