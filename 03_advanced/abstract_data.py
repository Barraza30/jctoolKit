#*****************************************************************
# content = Abstract_Data

# date    = 2022-08-05

# author  = Juan Carlos Barraza Mendoza
#*****************************************************************

import os
import json
from collections import OrderedDict

import maya.cmds as cmds


class AbstractData(object):
    '''
    '''
    def __init__(self):
        '''
        '''

        # set class attributes defaults
        self._data = OrderedDict()
        self._filepath = None

    def gatherData(self,node):
        '''
        '''
        if not cmds.objExists(node):
            cmds.warning('{0} does not exists in the current Maya session.'.format(node))
        #self._data['User'] = getpass.getuser()
        self._data[node] = OrderedDict(dagPath=cmds.ls(node, l=True)[0])

    
    def gatherDataIterate(self,nodes):
        '''
        '''
        for node in nodes:
            self.gatherData(node)


    def getData(self):
        '''
        example to get data: nodeData.getData()['jointName']['dagPath']
        '''
        return self._data 

    def write(self, filepath):
        '''
        This will write a dictionary of information out to disc in .json format.

        :param data: This is the dictionary of info you want to write out.
        :type data: dict | orderedDict

        :param filepath: The path to the file you wish to write. 
        '''

        if not isinstance(self._data, (dict,OrderedDict)):
            raise TrpeError('This data must be passed in as  a dictionary.')
        
        # dump data to json format and write it out to disk.
        data = json.dumps(self._data, indent=4, sort_keys=True)
        f=open(filepath,'w')
        f.write(data)
        f.close()
        
        # set a new filepath on the class.
        self._filepath = filepath

    def read(self,filepath):
        '''
        This will read a .json file from disk and return the data in the file.

        :param filepath: The path to the file you wish to read from.
        :type filepath: str

        :return: Data that was read from filepath given.
        :rtype: dict 
        '''

        if not os.path.isfile(filepath):
            raise RuntimeError('This{0} does not exists.'.format(filepath))

        f=open(filepath,'r')
        self._data = json.loads(f.read())
        f.close()

        # set a new filepath on the class
        self._filepath = filepath

        return self._data

    def applyData( node, attributes=None):
        '''
        '''


        pass