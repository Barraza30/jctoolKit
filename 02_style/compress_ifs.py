# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#**********************************************************************************

import maya.cmds as cmds

# Set up colors --------------------------------------------------

"""
1:Black;    4:Dark red;      6:Blue;
13:Red;     25:Dark Yellow;  17:Yellow;
15:NavyBlue;                 16:White;
"""

#Color Dictionary


color = {"Black"    : 1,  "DarkRed" : 4,     "Blue" : 6,
         "Red"      : 13, "DarkYellow" : 25, "Yellow" : 17,
         "NavyBlue" : 15, "White" : 16,}

    
def set_color(ctrlList=None, color=None):

    for ctrlName in ctrlList:
        try:
            #set the control override enable
            cmds.setAttr(ctrlName + 'Shape.overrideEnabled', 1)
        except:
            pass
        try:
            #set control color
            cmds.setAttr(ctrlName + 'Shape.overrideColor', color)

        except:
            pass
            
        return True
 
#EXMAPLE           
#set_color(['LF_Arm_01_Elbow_FK_Ctrl'], color["Black"])


