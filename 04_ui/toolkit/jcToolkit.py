#*****************************************************************
# content = jc-Toolkit, this is focused in rig, and it is helping to improve the process in some tasks that are repetitly day by day.
# date     = 2022-06-14
#
# class   = Python Advance
# author  = Juan Carlos Barraza Mendoza
#*****************************************************************

import os
import sys
import types
import webbrowser

from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMayaUI as omui

import rigtools.libs.control as ctl
import rigtools.utils.fx_utility as fu
import rigtools.libs.common as common
import rigtools.utils.joint_utility as ju
import rigtools.utils.control_utily as cu
import rigtools.utils.transform_utility as tu

reload(common)
reload(ctl)
reload(fu)
reload(cu)
reload(tu)

#*****************************************************************
# VARIABLES SECTION

TITLE = os.path.splitext(os.path.basename(__file__))[0]
CURRENT_PATH = os.path.dirname(__file__)
IMG_PATH = CURRENT_PATH + "/img/{}.png"
path_ui = IMG_PATH + "/" + TITLE + ".ui"


def maya_main_window():
    """
    Return the Maya window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()

    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

#*****************************************************************
# CLASSES SECTION

'''EXTEND THE QLINE EDIT'''
class MyLineEdit(QtWidgets.QLineEdit):
    #create signal
    enter_pressed = QtCore.Signal()

    #emit the current text in the qline edit with every key enter
    def keyPressEvent(self, e):
        super(MyLineEdit, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit()

#*****************************************************************
#JcToolkit CLASS
class JcToolkit(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(JcToolkit, self).__init__(parent)
        
        #Show ui
        self.init_ui()

        """
        Run Connections
        """
        #Color Section
        self.create_control_connections()
        #General section
        self.create_general_connections()
        #Joint section
        self.create_joint_connections()

    #*****************************************************************
    def init_ui(self):
        
        #path_ui = CURRENT_PATH + "/" +TITLE + ".ui"
        path_ui = ("/").join([os.path.dirname(__file__), TITLE + ".ui"])
        #Read and open the .ui file
        self.ui = QtUiTools.QUiLoader().load(path_ui,parentWidget=self)

        #setWindowIcon 
        self.ui.setWindowIcon(QtGui.QPixmap(IMG_PATH.format("toolkit")))
        #Remove the ? from the dialog on Window
        self.ui.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        #Show the - from the dialog on Window
        self.ui.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowFlags(QtCore.Qt.WindowMinimizeButtonHint, True))

        self.ui.show()

    '''SIGNALS SECTION'''
    #*****************************************************************
    #SIGNAL CONNECTIONS CONTROL'S TAP
    def create_control_connections(self):
        self.ui.btnRED.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.RED)) 
        self.ui.btnBLUE.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.BLUE)) 
        self.ui.btnYELLOW.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.YELLOW)) 
        self.ui.btnGREEN.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.GREEN02)) 
        self.ui.btnDARK.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.BLACK)) 
        self.ui.btnPINK.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.PINK)) 
        self.ui.btnRED02.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.RED02)) 
        self.ui.btnCYAN.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.BLUE04)) 
        self.ui.btnORANGE.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.ORANGE)) 
        self.ui.btnVIOLET_RED.clicked.connect(lambda:self.setcolor_curve(btnCOLOR=common.VIOLET_RED))

        self.ui.btnCreatCtrl.clicked.connect(self.create_control) 
   
        self.ui.btnScaleUp.clicked.connect(lambda:self.scale_ctl(Range=1.2)) 

        self.ui.btnScaleDn.clicked.connect(lambda:self.scale_ctl(Range=-0.9)) 
  
        self.ui.btnCurveUtil.clicked.connect(self.CurveUtil)

    
    #*****************************************************************
    #SIGNAL CONNECTIONS GENERAL'S TAP
    def create_general_connections(self):
            self.ui.btnOffsetGrp.clicked.connect(self.create_offset) 

            self.ui.btnLockHide.clicked.connect(self.lockAll) 
            self.ui.btnUnlockAll.clicked.connect(self.unlockAll) 

            self.ui.btnSnap.clicked.connect(self.snap) 

            self.ui.btnScale.clicked.connect(self.scale_connection) 
            self.ui.btnRotate.clicked.connect(self.rotate_connection) 
            self.ui.btnTranslate.clicked.connect(self.translate_connection) 

    #*****************************************************************
    #SIGNAL CONNECTIONS JOINT'S TAP
    def create_joint_connections(self):

        self.ui.btnAverageJnt.clicked.connect(self.average_Joint) 

        self.ui.btnSelJoint.clicked.connect(self.selectionTojoint) 

        #Add widgets into the horizontalLayout_12
        self.create_fkChain_Layout()
 
        self.create_bttn.clicked.connect(self.fkJointChain)

        self.ui.btnShow.clicked.connect(self.showOrient)
        self.ui.btnHide.clicked.connect(self.hideOrient)
  
        self.ui.btnShowAxis.clicked.connect(self.showAxis)
        self.ui.btnHideAxis.clicked.connect(self.hideAxis)

    #*****************************************************************
    #SIGNAL CONNECTIONS FX'S TAP

        self.ui.btn_show_selection.clicked.connect(lambda:self.follcile_Visibility(1, selection=True, All=False))
        self.ui.btn_hide_selection.clicked.connect(lambda:self.follcile_Visibility(0, selection=True, All=False)) 
        
        self.ui.btn_show_all.clicked.connect(lambda:self.follcile_Visibility(1, selection=False, All=True))
        self.ui.btn_hide_all.clicked.connect(lambda:self.follcile_Visibility(0, selection=False, All=True)) 

        self.ui.btn_fx_create.clicked.connect(self.create_Follicles)

    #*****************************************************************
    #SIGNAL CONNECTIONS GEOMETRY'S TAP

        self.ui.btnAbSymMesh.clicked.connect(self.abSymmetryMesh)

        self.ui.btnDoraSkin.clicked.connect(self.DoraSkinWeightImpExp)

        self.ui.btnZeroTransforms.clicked.connect(self.ZeroTransform)



    #*****************************************************************
    #CONTROL FUNCTIONS 
    
    def color_dialog(self):
        color = QtWidgets.QColorDialog.getColor( self, options=QtWidgets.QColorDialog.DontUseNativeDialog)
        return color

    def setcolor_curve(self, btnCOLOR=common.RED02):

        control = cmds.ls(sl=True)

        for i in control:

            color = btnCOLOR
            cmds.setAttr('{0}.overrideEnabled'.format(i),1)
            cmds.setAttr('{0}.overrideColor'.format(i), color)

    def create_control(self):
        #get the control selection
        getNameObj = cmds.ls(sl=True, an=True)

        for i in getNameObj:  
            #get joint position
            JointPosition = cmds.xform(i, q=True, ws=True, matrix=True) 
            #cretae control
            control = ctl.createControl(name='{0}_Ctrl'.format(i),controlType='sphere', hierarchy=['Grp','nul'], position=[0,0,0],
                    rotation=[0,0,0], parent=None, color=common.BLUE, ctrlScale=[1,1,1])
            
            #Match the control position to the joint position
            cmds.xform(control[-1], ws=True, matrix=JointPosition)
            #parent joint to control
            cmds.parent(i, control[-1])

        return control

    def scale_ctl(self, Range=0.1):
        
        cu.scaleCtrl(value=Range)
        

    def CurveUtil(self):
            '''
            Run the CurveUtil tool
            '''
            mel.eval("source cr_curveUtil;")
            mel.eval("cr_curveUtil;")

            return True

    
    #*****************************************************************
    #GENERAL FUNCTIONS
    
    def create_offset(self):

        getObj = cmds.ls(sl=True)
        
        for i in getObj:
            cu.addOffset(i, suffix='Off')

    def lockAll(self):
        
        getObj = cmds.ls(sl=True)
        
        for i in getObj:
            
            cu.lockAttr(i, lockAttrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
            

    def unlockAll(self):
        
        getObj = cmds.ls(sl=True)
        
        for i in getObj:
            
            cu.unlockAttr(i, lockAttrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])

    def snap(self):

        getObj = cmds.ls(sl=True)

        tu.snap(getObj[0], getObj[-1])

    def translate_connection(self):

        getObj = cmds.ls(sl=True)

        tAttrs = ["tx", "ty", "tz"]
        for t in tAttrs:
            cmds.connectAttr ('{0}.{1}'.format(getObj[0],t), '{0}.{1}'.format(getObj[-1],t))
    
    def rotate_connection(self):

        getObj = cmds.ls(sl=True)

        rAttrs = ["rx", "ry", "rz"]
        for t in rAttrs:
            cmds.connectAttr ('{0}.{1}'.format(getObj[0],t), '{0}.{1}'.format(getObj[-1],t))

    def scale_connection(self):

        getObj = cmds.ls(sl=True)

        sAttrs = ["sx", "sy", "sz"]
        for t in sAttrs:
            cmds.connectAttr ('{0}.{1}'.format(getObj[0],t), '{0}.{1}'.format(getObj[-1],t))

    #*****************************************************************
    #JOINT FUNCTIONS

    def average_Joint(self):

        Cluster=cmds.cluster( rel=True )
        Jnt=cmds.createNode('joint', n='Temp_01_Jnt')
        Pcon=cmds.parentConstraint(Cluster[-1],Jnt, mo=False)
        cmds.delete(Pcon)
        cmds.delete(Cluster)

        return True

    def selectionTojoint(self):
        #get selectyion obj
        getObj = cmds.ls(sl=True)
        #get leng of the list
        numList = len(getObj)
        #joint empty list
        jnt_lidt = []
        #create joint
        for x in range(numList):
            jnt = cmds.createNode('joint', n='Temp_{:02d}_Jnt'.format(x+1))
            jnt_lidt.append(jnt)
        #snap joints to each obj in the list
        for obj, jnt in zip(getObj,jnt_lidt):
            tu.snap(jnt,obj)

        return True

    def fkJointChain(self):
        Number = self.spin_box.value()
        Suffix = self.lineEdit.text()

        ju.createJointChain('{}'.format(Suffix), startPosition=(0,0,0), startRotation=(0,0,-90), number=Number)
    
    def create_fkChain_Layout(self):
        #append the new QLine edit, QSpinBox, QPushBotton into the horizontalLayout_12
        
        self.lineEdit = MyLineEdit()
        self.lineEdit.setStyleSheet("QLineEdit"
                        "{"
                        "background-color: rgb(64, 73, 81);"
                        "}")
        self.spin_box = QtWidgets.QSpinBox()
        self.spin_box.setStyleSheet("QSpinBox"
                "{"
                "background-color: rgb(64, 73, 81);"
                "}")
        self.spin_box.setMinimum(1)
        self.name_text_lb = QtWidgets.QLabel('Prefix:')
        self.create_bttn = QtWidgets.QPushButton('Create')
        self.ui.horizontalLayout_12.addWidget(self.name_text_lb)
        self.ui.horizontalLayout_12.addWidget(self.lineEdit)
        self.ui.horizontalLayout_12.addWidget(self.spin_box)
        self.ui.horizontalLayout_12.addWidget(self.create_bttn)
        


    def showOrient(self):
        ju.orientAttr(On_Off=True)
    
    def hideOrient(self):
        ju.orientAttr(On_Off=False)

    def showAxis(self):
        ju.setAxisDisplay(display=True, allObj=False)

    def hideAxis(self):
        ju.setAxisDisplay(display=False, allObj=False)

    #*****************************************************************
    #FX FUNCTIONS

    def follcile_Visibility(self, value, selection=True, All=False):
        fu.follicle_vis(show_off=value, selection=selection, All=All)

        return True

    def create_Follicles(self):
        lineEdit  = self.get_line_edit_text(self.ui.lineEdit_fx)
        spinBox   = self.get_spin_value(self.ui.spinBox_fx)
        UcheckBox = self.get_checkBox_state(self.ui.UcheckBox)
        VcheckBox = self.get_checkBox_state(self.ui.VcheckBox)

        print (lineEdit, spinBox, UcheckBox, VcheckBox)

        fu.createFollicles( name_Surface='{0}'.format(lineEdit), u_dir=UcheckBox, v_dir=VcheckBox, resolution=spinBox, vParam=0.5, uParam=0.5)

        return True

    #*****************************************************************
    #GEOMETRY FUNCTIONS
    def abSymmetryMesh(self):
        #Run the abSymMesh tool
        mel.eval("source abSymMesh;")
        mel.eval("abSymMesh;")

        return True

    def DoraSkinWeightImpExp(self):
        #Run the DoraSkinWeightImpExp tool
        mel.eval("source DoraSkinWeightImpExp;")
        mel.eval("DoraSkinWeightImpExp;")

        return True

    def ZeroTransform(self):
        getNameCtrl = cmds.ls(sl=True, an=True)
        for i in getNameCtrl:
            cmds.makeIdentity(i, apply=True, t=1, r=1, s=1, n=0)

        return True

    #*****************************************************************
    #GET UI DATA
    def get_line_edit_text(self, target):
        prefix = target.text()
        print("prefix: {0}".format(prefix))

        return prefix

    def get_spin_value(self, target):
        value = target.value()
        print("Value: {0}".format(value))

        return value

    def get_checkBox_state(self, target):
        state = target.isChecked()
        print("State: {0}".format(state))

        return state

#*****************************************************************
#START UI
if __name__ == "__main__":
    #app = QtWidgets.QApplication(sys.argv)
    try:
        Create_UI_ui.close() # pylint: disable=E0601
        Create_UI_ui.deleteLater()
    except:
        pass

    Create_UI_ui = JcToolkit()
    Create_UI_ui.show()

def load():

    global Create_UI_ui   
    Create_UI_ui = JcToolkit()

        




