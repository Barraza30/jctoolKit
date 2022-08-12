# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************
from datetime import datetime

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
#FUNCTIONS
def update_transform(object,translate=[0,0,0], rotate=[0,0,0], scale=[1,1,1]):
      cmds.xform(object, ws= True, t=  translate)
      cmds.xform(object, ws= True, ro= rotate)
      cmds.xform(object, ws= True, s=  scale)

      return True


#*************************************************************
#PARENT CLASS
class Object(object):
   def __init__(self, name, color,translate=[0,0,0], rotate=[0,0,0], scale=[1,1,1]):
      self._name     = name
      self.translate = translate
      self.rotate    = rotate
      self.scale     = scale
      self.color     = color

   def print_infos(self, object):
      obj_translate = cmds.xform(object, q= True,  r= True, t= True )
      obj_rotate    = cmds.xform(object, q= True,  r= True, ro= True )
      obj_scale     = cmds.xform(object, q= True,  r= True, s= True )
      
      print(object + ": translate:{} : rotatate:{} : scale:{}".format(obj_translate, obj_rotate, obj_scale))


   def build(self):

      return True

      
#*************************************************************
class Cube(Object):
   # initialize class
   def __init__(self, name, color, width=1, height=1, depth=1, subDiv_width=1, subDiv_height=1, subDiv_Depth=1):
      super(Cube, self).__init__(name, color, translate=[0,0,0], rotate=[0,0,0], scale=[1,1,1])

      self._name = name
      self.color = color
      self._width = width
      self._height = height
      self._depth = depth
      self._subDiv_width = subDiv_width
      self._subDiv_height = subDiv_height
      self._subDiv_Depth = subDiv_Depth
   
   def build(self):

      super(Cube, self).build()

      def funcCube():

         self.cube = cmds.polyCube( n= self._name, w= True )
         self.objCube = self.cube[0]
         cmds.xform(self.objCube, t= self.translate, ro= self.rotate, s= self.scale)

         # set color
         cmds.setAttr(self.objCube + 'Shape.overrideEnabled', 1)
         cmds.setAttr(self.objCube + 'Shape.overrideColor', self.color)

         #return the polyObject
         self.polyCube = self.cube[-1]
         
         cmds.setAttr ("{}.width".format(self.polyCube ), self._width)
         cmds.setAttr ("{}.height".format(self.polyCube ), self._height)
         cmds.setAttr ("{}.depth".format(self.polyCube ), self._depth)
         cmds.setAttr ("{}.subdivisionsWidth".format(self.polyCube ), self._subDiv_width)
         cmds.setAttr ("{}.subdivisionsHeight".format(self.polyCube ), self._subDiv_height)
         cmds.setAttr ("{}.subdivisionsDepth".format(self.polyCube ), self._subDiv_Depth)

         return  self.objCube
      #----------------------------------------------------------------------------
      def print_status(func):
         def wrapper():
           start_time = datetime.now()
           print("*************************************************")
           print("START")
           
           funcCube() # main_function
           
           print("DONE")
           result_time = (datetime.now() - start_time).total_seconds()
           
           print 'the cube was created in, Time: {}'.format(result_time)
           print("*************************************************")
            
         return wrapper

      @print_status
      def process():

         print("create cube -------------- True")

         return True

      process()

      #----------------------------------------------------------------------------

      #prtin object Data
      self.print_infos(funcCube())

      return True






#*************************************************************
# EXAMPLE
'''
import jctoolKit.cube as cb
reload(cb)

color = {"Black"    : 1,  "DarkRed" : 4,     "Blue" : 6,
         "Red"      : 13, "DarkYellow" : 25, "Yellow" : 17,
         "NavyBlue" : 15, "White" : 16,}
         

cube01 = cb.Cube('g_cube', color['Blue'], height=1, depth=1, subDiv_width=4, subDiv_height=4, subDiv_Depth=1)
cube01.build()

cube02 = cb.Cube('m_cube', color['DarkRed'], height=1, depth=1, subDiv_width=1, subDiv_height=1, subDiv_Depth=1)
cube02.build()
'''



