#*****************************************************************
# content = control utily
# date    = 2022-07-109#
# class   = Python Advance
# author  = Juan Carlos Barraza Mendoza
#*****************************************************************
import maya.cmds as cmds

'''
def enumMenu(grpTarget):
        outfitGeos = cmds.listRelatives(grpTarget)
        outfits = [i.replace('_Geo_Grp', '') for i in outfitGeos]
        attrs = ':'.join(outfits)
        cu.addVisibilityEnumAttr("Master_Ctrl", grpTarget, en=attrs, obj_list=outfitGeos, driven_attr='v', dv=0)
'''
#*************************************************************************************
#FUNCTIONS
#*************************************************************************************
def addOffset(dst, suffix='OFF'):
    '''
    :return: offset name
    '''

    grp_offset = cmds.createNode('transform', name='{}_{}'.format(dst, suffix))
    dst_mat = cmds.xform(dst, q=True, m=True, ws=True)
    cmds.xform(grp_offset, m=dst_mat, ws=True)

    dst_parent = cmds.listRelatives(dst, parent=True)
    if dst_parent:
            cmds.parent(grp_offset, dst_parent)

    cmds.parent(dst, grp_offset)

    return grp_offset

#*************************************************************************************
def lockAttr(ctrl, lockAttrs=["v"]):
    '''
    lock and hide ctrl's attributes
    input:
        ctrl(string): control name
        lockAttrs(string list): valid list member: tx, ty, tz, rx, ry, rz, sx, sy, sz, v
    '''
    kAttrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
    for at in ["t", "r", "s"]:
        if at in lockAttrs:
            lockAttrs.remove(at)
            [lockAttrs.append(attr) for attr in ["{0}x".format(at), "{0}y".format(at), "{0}z".format(at)]]

    for attr in lockAttrs:
        cmds.setAttr("{0}.{1}".format(ctrl, attr), l=True, cb=False, k=False)
        kAttrs.remove(attr)

    for attr in kAttrs:
        if not cmds.getAttr("{0}.{1}".format(ctrl, attr), k=True):
            cmds.setAttr("{0}.{1}".format(ctrl, attr), l=False, k=True)
    return True

#*************************************************************************************
def unlockAttr(ctrl, lockAttrs=["v"]):
    '''
    unlock and hide ctrl's attributes
    input:
        ctrl(string): control name
        lockAttrs(string list): valid list member: tx, ty, tz, rx, ry, rz, sx, sy, sz, v
    '''
    kAttrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
    for at in ["t", "r", "s"]:
        if at in lockAttrs:
            lockAttrs.remove(at)
            [lockAttrs.append(attr) for attr in ["{0}x".format(at), "{0}y".format(at), "{0}z".format(at)]]

    for attr in lockAttrs:
        cmds.setAttr("{0}.{1}".format(ctrl, attr), l=False, cb=False, k=True)
        kAttrs.remove(attr)

    for attr in kAttrs:
        if not cmds.getAttr("{0}.{1}".format(ctrl, attr), k=True):
            cmds.setAttr("{0}.{1}".format(ctrl, attr), l=False, k=True)
    return True
#*************************************************************************************
# Scake Control Function
def scaleCtrl(value=0.5):
    '''
    :param value: value to scale the control
    :type name: float
    '''
    
    #get the control selection
    selection_control = cmds.ls(selection=True)
    
    for all in selection_control:
    
        spans=cmds.getAttr( all+'.spans' )
        cmds.select (all+'.cv[0:{}]'.format(spans))
        cmds.xform (s=[value,value,value], r=True, os=True, wd=True )
        cmds.select(d=True)
        cmds.select(all)
    return True