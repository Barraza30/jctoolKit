#*****************************************************************
# content = joint utily
#date     = 2022-07-109#
# class   = Python Advance
# author  = Juan Carlos Barraza Mendoza
#*****************************************************************

import maya.cmds as cmds
import math
import sys

import rigtools.utils.math_utility as mu
reload(mu)

def createJointChain(name,startPosition=(0,0,0),startRotation=(0,0,-90),number=5):
    """
    :param name: Name of object
    :type name: str

    :return: Return name of joint
    :rtype: str
    """
    if not isinstance (name, basestring):
        raise TypeError('Must pass in string')
    # declaring empty joint list
    jointList = []
    #loop through number range and creating joints while adding to jointList
    for i in range (number):
        position = (startPosition[0], startPosition[1] + i, startPosition[2])
        newJnt = cmds.createNode('joint', n='{}_{:02d}_Jnt'.format(name, i+1))
        #adding joint list to the empety list
        jointList.append(str(newJnt))
    
    #reverse the current joint list
    list_reverse=jointList
    #parent in correct hierarchy the fk chain
    for i,x in zip(jointList[:-1], list_reverse[1:]):
        cmds.parent(x,i)
    
    #move up the joint in the chain
    for jnt in  jointList[1:]:
        print jnt
        cmds.xform(jnt, r=True , t=position)
    
    cmds.xform(jointList[0], r=True , ro=startRotation)
    
    return jointList

def createJoint(name='Default_Jnt', p=(0,0,0), r=(0,0,0), rad=0.2, par='', color=0, vis=True, snap_to_parent=False):
    '''
    Creates a joint with the given parameters
    if the parent doesn't exists it will be ignored

        # missing color and visibility attributes

    '''
    if snap_to_parent and par:
        p = cmds.xform(par, ws=True, q=True, t=True)
        r = cmds.xform(par, ws=True, q=True, t=True)
    jnt = cmds.createNode("joint", name=name)
    cmds.xform(jnt, ws=True, t=p, ro=r)
    #parent
    if par: 
        if cmds.objExists(par): 
            cmds.parent(jnt, par)
    #set the radius
    cmds.setAttr("{0}.radius".format(jnt), rad)
    #set visibility
    if not vis: cmds.setAttr("{0}.v".format(jnt), False)
    return jnt


def labelJoint(jnt, displayAxis=True, labelAsJnt=None):
    '''
    the joint must be named as side + bodypart + index + keyword + Jnt
    inpit:
        jnt(string): the name of the joint going to be labeled
        labelAsJnt(string): if not none, label jnt as another given joint
    '''
    if labelAsJnt:
        side = labelAsJnt.partition('_')[0]
        otherType = labelAsJnt.partition('_')[2]
    else:
        side = jnt.partition('_')[0]
        otherType = jnt.partition('_')[2]

    sideDic = {"LF": 1, "RT": 2}
    sideNo = sideDic[side] if side in ["LF", "RT"] else 0
    cmds.setAttr("{0}.side".format(jnt), sideNo)
    cmds.setAttr("{0}.type".format(jnt), 18)
    cmds.setAttr("{0}.otherType".format(jnt), otherType, type="string")

    if displayAxis:
        cmds.toggle(jnt, localAxis=True)

def setJoint(jnt, jntClass="Bind", setAs=None):
    '''
    put joint in the right set, need a good naming
    the joint set is classified as side + bodypart + index
    '''
    masterSet = "Jnts_Set"
    if not cmds.objExists(masterSet):
        cmds.sets(n=masterSet, em=True)

    subJntsSet = "{0}_Jnts_Set".format(jntClass)
    if not cmds.objExists(subJntsSet):
        cmds.sets(n=subJntsSet, em=True)
        cmds.sets(subJntsSet, add=masterSet)

    if not setAs:
        jntSet = jnt.split('_', 3)[0] + "_" + jnt.split('_', 3)[1] + "_" + jnt.split('_', 3)[2] + "_{0}_Jnt_Set".format(jntClass)
    else:
        jntSet = setAs

    if not cmds.objExists(jntSet):
        cmds.sets(n=jntSet, em=True)
        cmds.sets(jntSet, add=subJntsSet)
    cmds.sets(jnt, add=jntSet, nw=True)

def copyJointChain(joints, oldAlias="Proxy_Jnt", newAlias="Jnt", freeze=True):
    '''
    copy joint chain when old chain is not clean in childern node
    '''
    newJoints = []
    cmds.select(cl=True)
    for i, jnt in enumerate(joints):
        pos = cmds.xform(jnt, q=True, t=True, ws=True)
        ori = cmds.xform(jnt, q=True, ro=True, ws=True)
        newJoint = cmds.joint(n=jnt.replace(oldAlias, newAlias), rad=0.5)
        cmds.xform(newJoint, t=pos, ro=ori, ws=True, a=True)
        newJoints.append(newJoint)

    if freeze:    
        cmds.makeIdentity(newJoints[0], r=True, a=True)  

    return newJoints

def orientJointChain(joints, aimAxis="x", upAxis=None, sideAxis=None, frontAxis=None, flipX=False, flipY=False, flipZ=False):
    '''
    orient the joint chain to be good for IK creation
    input:
        joints(string list): the name list of joint, must in orider, from parent to child
        aimAxis(string): valid value: x, y, z, -x, -y, -z, the joints chain's primary axis
        upAxis(string): valid value: x, y, z, -x, -y, -z, which of the joint axis is going to match the world y axis
        sideAxis(string): valid value: x, y, z, -x, -y, -z, which of the joint axis is going to match the world x axis, can't use at the same time with upAxis 
        frontAxis(string): valid value: x, y, z, -x, -y, -z, which of the joint axis is going to match the world z axis, can't use at the same time with upAxis, frontAxis

    note: when assignning y as aimAxis and then z as upAxis or sideAxis, z Axis give the opposite result
    '''
    if upAxis:
        sideAxis = None
        frontAxis = None
    else:
        if sideAxis:
            frontAxis = None
        else:
            if not frontAxis:
                print("Error: please input one supporting axis: upAxis, sideAxis, frontAxis")
                return False

    axisDic = {"x": (-1, 0, 0),  "y": (0, -1, 0), "z": (0, 0, -1), "-x": (1, 0, 0),  "-y": (0, 1, 0), "-z": (0, 0, 1)}
    p = [cmds.xform(jnt, q=True, t=True, ws=True) for jnt in joints]
    if aimAxis[0] == '-':
        aimAxis = aimAxis[1]
        v1s = [mu.vPlus(p[i], p[i+1], '-') for i in range(len(p)-1)]
    else:
        v1s = [mu.vPlus(p[i+1], p[i], '-') for i in range(len(p)-1)]

    v2s = []
    v2s.append(mu.vPlus(p[0], p[2], '-'))
    v2s.extend([mu.vPlus(p[i+1], p[i], '-') for i in range(len(p)-2)])
    #get the third vector
    v3s = [mu.vCross(v1s[i], v2s[i]) for i in range(len(p)-1)]

    neg = 1
    if upAxis:
        if upAxis[0] == "-":
            neg = -1
            axis = upAxis[1]
        else:
            axis = upAxis

        for i in range(len(p)-1):
            if v3s[i][1] * neg > 0:
                v3s[i] = mu.vMultiply(v3s[i], -1)
            if v3s[i] == [0, 0, 0]:
                v3s[i] = axisDic[upAxis]
        angles = [mu.vectorToAngle(v1s[i], upVec=v3s[i], aimAxis=aimAxis, upAxis=axis) for i in range(len(p)-1)]

    if sideAxis:
        if sideAxis[0] == "-":
            neg = -1
            axis = sideAxis[1]
        else:
            axis = sideAxis

        for i in range(len(p)-1):
            if v3s[i][0] * neg > 0:
                v3s[i] = mu.vMultiply(v3s[i], -1)
            if v3s[i] == [0, 0, 0]:
                v3s[i] = axisDic[sideAxis]
        angles = [mu.vectorToAngle(v1s[i], sideVec=v3s[i], aimAxis=aimAxis, sideAxis=axis) for i in range(len(p)-1)]

    if frontAxis:
        if frontAxis[0] == "-":
            neg = -1
            axis = frontAxis[1]
        else:
            axis = frontAxis

        for i in range(len(p)-1):
            if v3s[i][2] * neg > 0:
                v3s[i] = mu.vMultiply(v3s[i], -1)
            if v3s[i] == [0, 0, 0]:
                v3s[i] = axisDic[frontAxis]
        angles = [mu.vectorToAngle(v1s[i], sideVec=v3s[i], aimAxis=aimAxis, sideAxis=axis) for i in range(len(p)-1)]

    angles.append(angles[-1])

    #unparent the joint chain
    [cmds.parent(jnt, w=True) for jnt in joints[1:]]
    #rotate joint
    [cmds.xform(jnt, ro=angles[i], a=True, ws=True) for i, jnt in enumerate(joints)]
    if flipX:
        [cmds.xform(jnt, ro=(180, 0, 0), r=True, os=True) for i, jnt in enumerate(joints)]
    if flipY:
        [cmds.xform(jnt, ro=(0, 180, 0), r=True, os=True) for i, jnt in enumerate(joints)]
    if flipZ:
        [cmds.xform(jnt, ro=(0, 0, 180), r=True, os=True) for i, jnt in enumerate(joints)]
    #parent back
    [cmds.parent(jnt, joints[i]) for i, jnt in enumerate(joints[1:])]
    #freeze rotation
    cmds.makeIdentity(joints[0], r=True, a=True)

    return joints

def orientAttr(On_Off=True):
    '''
    If On_Off is True show the jointOrient attributes if not hide them
    input:
        On_Off(Boolean): True or False
        jointOrientAttrs: jointOrientX, jointOrientY, jointOrientZ 
    '''
    
    getJnt=cmds.ls(sl=True)
    
    for i in getJnt:
        
        if On_Off ==True:
            cmds.setAttr ('{0}.jointOrientX'.format(i),k=True)
            cmds.setAttr ('{0}.jointOrientY'.format(i),k=True)
            cmds.setAttr ('{0}.jointOrientZ'.format(i),k=True)
        else:
            cmds.setAttr ('{0}.jointOrientX'.format(i),k=False)
            cmds.setAttr ('{0}.jointOrientY'.format(i),k=False)
            cmds.setAttr ('{0}.jointOrientZ'.format(i),k=False)
            
    return True

#show axis
def setAxisDisplay(display=False, allObj=False):
    # if no joints are selected, do it for all the joints in the scene
    # if allObj flag is True then this will toggle the axis display for all objects in the scene, not just joints.
    if not allObj:
        if len(cmds.ls(sl=1, type="joint")) == 0:
            jointList = cmds.ls(type="joint")
        else:
            jointList = cmds.ls(sl=1, type="joint")
        # set the displayLocalAxis attribute to what the user specifies.
        for jnt in jointList:
            cmds.setAttr(jnt + ".displayLocalAxis", display)
    else:
        if len(cmds.ls(sl=1)) == 0:
            objList = cmds.ls(transforms=1)
        else:
            objList = cmds.ls(sl=1)
        # set the displayLocalAxis attribute to what the user specifies.
        for obj in objList:
            cmds.setAttr(obj + ".displayLocalAxis", display)


#setAxisDisplay(display=True, allObj=False)