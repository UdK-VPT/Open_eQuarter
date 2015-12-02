# -*- coding: utf-8 -*-

"""
Project:        OpenEQuarter
Subproject:     Mole
Type:           A QGIS plugin
Module:         workflow
Package:        mole.qgisinteraction
Description:    Functions to handle workflows
Authors:        Werner 'Max' Kaul, UdK-Berlin (max)
Creation Date:  2015-11-26
Latest Changes: 2015-11-26 (max)

(C) Open eQuarter Project Team UdK-Berlin
"""


class OeQ_WorkStep:
    '''
    Single step of a workflow
    name:                   Name of the workstep
    description:            Short description of the workstep
    workstepfunction:       Function or method to achieve the workstep
    successcheckfunction:   Function or method to check if the workstep was successful
    waitfunction:           Function or method to wait for completion of the workstep
    errorfunction:          Function or method to run if the execution of the workstep failed
    '''

    def __init__(self,name,
                 description,
                 workstepfunction,
                 successcheckfunction=None,
                 waitfunction=None,
                 errorfunction=None):
        self.name=name
        self.description=description
        self.workstepfunction=workstepfunction
        if successcheckfunction:
            self.successcheckfunction=successcheckfunction
        else:
            self.successcheckfunction=self.succes_default
        if waitfunction:
            self.waitfunction=waitfunction
        else:
            self.waitfunction=self.wait_default
        if errorfunction:
            self.errorfunction=errorfunction
        else:
            self.errorfunction=self.error_default

    def error_default(self):
        '''
        Default errorfunction
        :return: None
        '''
        from mole import oeq_global
        oeq_global.OeQ_init_error(u"Workstep '"+self.name+ "': ", u'Execution failed!')

    def wait_default(self):
        '''
        Default waitfunction
        :return: True
        '''
        return True

    def succes_default(self):
        '''
        Default successfunction
        :return: True
        '''
        return True

    def do(self):
        '''
        Run the Function defined in workstepfunction, wait for completion and check success
        :return: True if success, otherwise False
        '''
        if self.workstepfunction():
            if self.waitfunction():
                return self.successcheckfunction()
        return False

    def wait_until_done(self):
        '''
        Wait until workstepfunction is done
        :return:  True if success, otherwise False
        '''
        if self.waitfunction():
            return self.successcheckfunction()
        return False

    def is_done(self):
        '''
        check success of workstepfunction
        :return: True if success, otherwise False
        '''
        return self.successcheckfunction()

    def error(self):
        '''
        Run errorfunction
        :return: True if success, otherwise False
        '''
        return self.errorfunction()

    def info(self):
        '''
        Print name and description of the workstep
        :return:
        '''
        print "Workstep   : '"+self.name+"'"
        print "Description: "+self.description


class OeQ_Workflow:
    def __init__(self, name='', description='', registry=[], worksteps=[], state=0):
        self.name=name
        self.description=description
        self.registry=registry
        self.worksteps=worksteps
        self.state=state

    def reset(self):
        self.state=0

    def register_workstep(self,workstep):
        '''
        Add workstep to OeQ_WorkStep_Registry
        :param workstep:  Workstep of type OeQ_WorkStep
        :return: None
        '''
        self.registry.append(workstep)


    def get_workstep(self,name):
        '''
        Get workstep by name
        :param name: Name of the workstep
        :return:
        '''
        ws = filter(lambda x: x.name == name, self.registry)
        if not ws:
            return None
        return ws[0]

    def workstep_exists(self,name):
        '''
        Check if workstep exists in OeQ_Registry
        :param name: Name of the workstep
        :return: True if exists
        '''
        if self.get_workstep(name):
            return True
        return False

    def do_workstep(self,name):
        '''
        Check if workstep exists in OeQ_Registry
        :name: Name of the workstep
        :return: True if exists
        '''
        ws = self.get_workstep(name)
        if ws:
            return ws.do()
        return False

    def workstep_is_done(self,name):
        '''
        Check if workstep exists in OeQ_Registry
        :name: Name of the workstep
        :return: True if exists
        '''
        ws = self.get_workstep(name)
        if ws:
            return ws.is_done()
        return False

    def next_workstep(self,check_current=True):
        '''
        Check if workstep exists in OeQ_Registry
        :return: True if exists
        '''

        if check_current:
            self.state=self.find_current_workstep()
        if self.state == len(self.worksteps):
            return None
        print self.worksteps[self.state]
        if self.do_workstep(self.worksteps[self.state]):
            self.state+=1
            return True
        return False

    def next_worksteps_name(self,check_current=True):
        '''
        Check if workstep exists in OeQ_Registry
        :return: True if exists
        '''

        if check_current:
            self.state=self.find_current_workstep()
        if self.state == len(self.worksteps):
            return None
        print self.worksteps[self.state]
        return self.worksteps[self.state]


    def find_current_workstep(self):
        '''
        Check if workstep exists in OeQ_Registry
        :name: Name of the workstep
        :return: True if exists
        '''
        self.state=0
        for i in self.worksteps:
            ws = self.get_workstep(i)
            if ws.is_done():
                self.state +=1
            else:
                break
        return self.state

    def all_mandatory_worksteps_done(self,name,check_current=True):
        if check_current:
            self.state=self.find_current_workstep()
        if self.state == len(self.worksteps):
            return True
        if self.worksteps.index(name)<=self.state:
            return True
        return False



    def unregister_workstep(self,name):
        '''
        Remove workstep from OeQ_WorkStep_Registry
        :param name: Name of the workstep
        :return: True if successfull
        '''
        if self.workstep_exists(name):
            self.registry = filter(lambda x: x.name != name, self.registry)
            return True
        return False

    def is_done(self):
        if self.state == len(self.worksteps):
            return True
        return False

    def append_workstep(self,name):
        if self.workstep_exists(name):
            self.worksteps.append(name)

    def prepend_workstep(self,name):
        if self.workstep_exists(name):
            self.worksteps=[name]+self.worksteps

    def insert_workstep(self,name,position):
        if self.workstep_exists(name):
            self.worksteps=self.worksteps[:position]+[name]+self.worksteps[position:]


    def remove_workstep(self,name=None,position=None):
        if name in self.worksteps:
            if name == None:
                self.worksteps=self.worksteps[:position-1]+self.worksteps[position:]
            else:
                self.worksteps = filter(lambda x: x != name, self.worksteps)
            return True
        return False

    def clear_worksteps(self):
        self.worksteps=[]

    def info(self):
        '''
        Print Info for Worklow
        :return: None
        '''
        print "Workflow   : '"+self.name+"'"
        print "Description: "+self.description
        print "State      : "+str(self.state)
        print "Worksteps  : "+str(self.worksteps)

