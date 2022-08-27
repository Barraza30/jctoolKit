#*****************************************************************
# content = transform utily
#date     = 2022-07-109#
# class   = Python Advance
# author  = Juan Carlos Barraza Mendoza
#*****************************************************************

from maya import cmds


def snap(driven, driver):
    p=cmds.xform(driver, ws=True, q=True, t=True)
    r=cmds.xform(driver, ws=True, q=True, ro=True)
    cmds.xform(driven, ws=True, t=p, ro=r)

def getTransforms(o):
    '''
    Get positions of the given objects
    '''
    p = cmds.xform(o, ws=True, t=True, q=True)
    r = cmds.xform(o, ws=True, ro=True, q=True)
    s = cmds.xform(o, ws=True, s=True, q=True)

    return p,r,s

def snap(driven, driver):
    p,r,s =getTransforms(driver)
    cmds.xform(driven, ws=True, t=p, ro=r)

def createGrp(name, pos_obj='', parent='', child=''):
    p=(0,0,0)
    r=(0,0,0)
    if pos_obj:
        p=cmds.xform(pos_obj, ws=True, q=True, t=True)
        r=cmds.xform(pos_obj, ws=True, q=True, ro=True)
    grp=cmds.createNode('transform', n=name)
    cmds.xform(grp, ws=True, t=p, ro=r)
    if parent:
        cmds.parent(grp, parent)
    if child:
        cmds.parent(child, grp)


def createLocator(name, position=(0,0,0), rotation=(0, 0, 0), size=5.00, pos_obj='', visible=False, parent='', buffer_grp=False):
    #set postion for the locator
    if pos_obj:
        p=cmds.xform(pos_obj, ws=True, q=True, t=True)
        r=cmds.xform(pos_obj, ws=True, q=True, ro=True)
    else:
        p=position
        r=rotation
    #create a locator
    loc = cmds.spaceLocator()
    loc = cmds.rename(loc[-1], name)
    cmds.setAttr(loc + '.localScaleX', size)
    cmds.setAttr(loc + '.localScaleY', size)
    cmds.setAttr(loc + '.localScaleZ', size)
    cmds.xform(loc, ws=True, t=p, ro=r)
    if not visible:
        cmds.setAttr(loc + '.v', 0)
    #add buffer group
    if buffer_grp:
        grp = cmds.createNode('transform', n=loc+'_Grp')
        cmds.xform(grp, ws=True, t=p, ro=r)
        cmds.parent(loc, grp)
        if parent:
            cmds.parent(grp, parent)
    else:
        if parent:
            cmds.parent(loc, parent)
    return loc

def duplicateAsTransform(reference_object, name, parent=''):
    #create transform node
    transform = cmds.createNode('transform', n=name)
    #get transforms
    pos = cmds.xform(reference_object, ws=True, t=True, q=True)
    rot = cmds.xform(reference_object, ws=True, ro=True, q=True)
    # set transforms
    cmds.xform(transform, ws=True, t=pos, ro=rot)
    if parent:
        cmds.parent(transform, parent)
    return transform

def duplicateAsLocator(reference_object, name, parent='', vis=True):
    #create locator node
    locator = cmds.createNode('locator')
    locator = cmds.listRelatives(locator, p=True, type='transform')
    locator = cmds.rename(locator, name)
    #get locator
    pos = cmds.xform(reference_object, ws=True, t=True, q=True)
    rot = cmds.xform(reference_object, ws=True, ro=True, q=True)
    # set locator
    cmds.xform(locator, ws=True, t=pos, ro=rot)
    if parent:
        cmds.parent(locator, parent)
    #set visibility
    cmds.setAttr(locator+'.v', vis)
    return locator

