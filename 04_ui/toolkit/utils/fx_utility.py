#*****************************************************************
# content = fx utility
# date     = 2022-07-21
# class   = Python Advance
# author  = Juan Carlos Barraza Mendoza
#*****************************************************************

import maya.cmds as cmds
import math
import sys


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#FUNCTIONS

#*****************************************************************
#Follicle visibility
#*****************************************************************
def follicle_vis(show_off = 0, selection=True, All=False):
    '''
    :param show_off: this value drive the show or hiden follicle 0 = off, 1 = on
    :type name: float
    
    :param selection: if selection == True hide/show follicle selected
    :type name: Enum
    
    :param All: if ALL == True hide/show follicle
    :type name: Enum
    '''
        
    if selection == True:
        
        #get the follicle selection
        follicle_sl = cmds.listRelatives( typ='follicle', s=True)
        #loop, set visibility off in the follicle selection.
        for fol in follicle_sl:
            cmds.setAttr ("{0}.visibility".format(fol), show_off)
    
    elif All == True:
        
        #get the follicle selection
        follicle_sl = cmds.ls( typ='follicle')
        #loop, set visibility off in the follicle selection.
        for fol in follicle_sl:
            cmds.setAttr ("{0}.visibility".format(fol), show_off)
            
    return True

#*****************************************************************
#Create Follicles
#*****************************************************************
def createFollicles( name_Surface='replace', u_dir=False, v_dir=True, resolution=5, vParam=0.5, uParam=0.5):
    '''
    :param name_Surface: name of the ribbon surface
    :type name_Surface: string

    :param u_dir: if True create the follicle in u direction
    :type  u_dir: 

    :param v_dir: if True create the follicle in v direction
    :type  v_dir: 

    :param resolution: the amount of follicles
    :type resolution:  float
    
    :param vParam: follicle's paramter V 
    :type vParam:  float

    :param uParam: follicle's paramter u
    :type  uParam: float
    '''
    
    #Tag name of follicle group
    prefix= name_Surface

    positionFollicle=list()

    #Create follicle group
    ribbonFolliclesGrp = cmds.group( n = prefix + '_Follicle_grp', em = True)
    
    #Range of number with the loop is gonna iterate
    x = range(resolution)
    for i in x:

        folic = cmds.createNode('follicle', n = '{0}_{1}_folShape'.format(prefix, i + 1))
        folicTrans = cmds.listRelatives(folic, p = 1)[0]
        folicParent = folicTrans
        cmds.parent(folicParent, ribbonFolliclesGrp)
        cmds.connectAttr(prefix + '.worldMatrix', folic + '.inputWorldMatrix')
        cmds.connectAttr(prefix + '.local', folic + '.inputSurface')
        
        cmds.connectAttr (folic + '.outTranslate', folicParent + '.t')
        cmds.connectAttr (folic + '.outRotate', folicParent + '.r')
        #for foll in folicTrans:
        cmds.setAttr (folic + '.parameterU', uParam)
    #parent follicle group to history group    
    #cmds.parent(ribbonFolliclesGrp, ribbonHistory)
    #------------------------------------------------------
    #if the u_dir is false the direction is 'U' if not it is 'V'
    u_direction = u_dir
    #amount of follicles it gonna be create
    Resolution = resolution
    #get all the follicles in the ribbonFolliclesGrp
    folLis = cmds.listRelatives(ribbonFolliclesGrp, c = True)
    #follicleLis.append(folLis)
    #operation(divide) between the range of follicles to the value 1
    step = 1.0/float(Resolution-1)  
    #get range for each follicle in a range 0 to 1
    for i in range(0, Resolution): 
        follicle_position = [0.5, 0.5]
        if  v_dir == True: 
            follicle_position[1] = step*float(i)

            #append all the position to the emptyList
            positionFollicle.append( step*float(i))

            #Match the positio to the follicles 
            for fol, pos in zip(folLis, positionFollicle):
                cmds.setAttr (fol + '.parameterV', pos)
                cmds.setAttr (fol + '.parameterU', uParam)
        
        elif u_dir == True:

            follicle_position[0] = step*float(i)

            print follicle_position[0]

            #append all the position to the emptyList
            positionFollicle.append( step*float(i))

            #Match the positio to the follicles 
            for fol, pos in zip(folLis, positionFollicle):
                cmds.setAttr (fol + '.parameterU', pos)
                cmds.setAttr (fol + '.parameterV', vParam)
        

    return True
    
#Run the module CreateFollicles
#createFollicles( name='replace', u_dir=False, resolution=5,uParam=0.5)