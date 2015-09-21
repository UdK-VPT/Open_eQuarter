# -*- coding: utf-8 -*-

"""
Project:        OpenEQuarter
Subproject:     Mole
Type:           A QGIS plugin
Module:         legend
Package:        mole.qgisinteraction
Description:    Functions to deal with the QGIS Legend
Authors:        Werner 'Max' Kaul, UdK-Berlin (max)
Creation Date:  2015-09-16
Latest Changes: 2015-09-16 (max)

(C) Open eQuarter Project Team UdK-Berlin
"""

from PyQt4.QtCore import QVariant
from qgis.core import QgsProject,QgsLayerTreeGroup,QgsLayerTreeLayer,QgsMapLayerRegistry,QgsVectorFileWriter,QgsVectorLayer,QgsField
from qgis.utils import iface
from mole import oeq_global
from mole.project import config
import os

def nodeIsLayer(node):
    """nodeIsLayer: Checks, weather node represents a Layer
    :param node: Node to check or name of node
    :return: True/False/None if node does not exist
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    if isinstance(node, QgsLayerTreeLayer):
        return True
    return False

def nodeIsGroup(node):
    """nodeIsGroup: Checks, weather node represents a Group
    :param node: Node to check or name of node
    :return: True/False/None if node does not exist
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    if isinstance(node, QgsLayerTreeGroup):
        return True
    return False


def nodeAll(which='all',searchgroup=None):
    """nodeAll: Delivers all nodes of kind 'which' from node 'searchgroup'
    :param which: kind of node 'all'/'layer'/'group
    :param searchgroup: Parent node to search, default is the legend's root
    :return: list of found nodes
    """
    if searchgroup == None: 
        searchgroup = QgsProject.instance().layerTreeRoot()
    if oeq_global.isStringOrUnicode(searchgroup):
        searchgroup = nodeByName(searchgroup,'group')
        if len(searchgroup) == 0:
            return []
        else:
            searchgroup = searchgroup[0]
    nodelist=[]
    for child in searchgroup.children():
        nodelist.append(child)
        if isinstance(child, QgsLayerTreeGroup):
            nodelist=nodelist + nodeAll(which,child)
    if which == 'group':
        return filter(lambda x: nodeIsGroup(x), nodelist)
    if which == 'layer':
        return filter(lambda x: nodeIsLayer(x), nodelist)
    return nodelist


def nodeCount(which='all',searchgroup=None):
    """nodeCount: Number of nodes of kind 'which' in 'searchgroup'
    :param which: kind of node 'all'/'layer'/'group
    :param searchgroup: Parent node to search, default is the legend#s root
    :return: Number of nodes
    """
    return len(nodeAll(which,searchgroup))


def nodeAllGroups(searchgroup=None):
    """
    nodeAllGroups:  Delivers all group nodes from node 'searchgroup'
    :param searchgroup:    Parent node to search, default is the legend#s root
    :return:        list of found nodes
    """
    return nodeAll('group',searchgroup)


def nodeAllLayers(searchgroup=None):
    """
    nodeAllLayers:  Delivers all layer nodes from node 'searchgroup'
    :param searchgroup:    Parent node to search, default is the legend#s root
    :return:        list of found nodes
    """
    return nodeAll('layer',searchgroup)


def nodeNames(which='all',searchgroup=None):
    """
    nodeNames:      Delivers all nodenames from node 'searchgroup'
    :param which:   kind of node 'all'/'layer'/'group'
    :param searchgroup:    Parent node to search, default is the legend#s root
    :return:        List of names of all found nodes
    """
    nodelist=nodeAll(which,searchgroup)
    namelist=[]
    for i in nodelist:
        if nodeIsGroup(i):
            namelist.append(i.name())
        if nodeIsLayer(i):
            namelist.append(i.layerName())
    return namelist


def nodeByName(nodename,which='all',searchgroup=None):
    """
    nodeByName:     Delivers all nodes of kind 'which' named 'nodename'  in 'searchgroup'
    :param which:   kind of node 'all'/'layer'/'group
    :param searchgroup:    Parent node to search, default is the legend#s root
    :return:        List of found nodes
    """
    if oeq_global.isEmpty(nodename):
        return [QgsProject.instance().layerTreeRoot()] 
        
    allnodes=nodeAll(which,searchgroup)
    nodelist=[]
    for i in allnodes:
        if nodeIsGroup(i):
            if i.name() == nodename:
                nodelist.append(i)
        if nodeIsLayer(i):
            if i.layerName() == nodename:
                nodelist.append(i)
    return nodelist

def nodesByName(nodenames,which='all',searchgroup=None):
    """
    nodesByName:    Delivers all nodes of kind 'which' named 'nodenames'  in 'searchgroup' for multiple nodenames
    :param which:   kind of node 'all'/'layer'/'group
    :param searchgroup:    Parent node to search, default is the legend#s root
    :return:        List of found nodes for each name in 'nodenames' (as list of lists)
    """
    nodelist=[]
    for nodename in nodenames:
        nodelist.append(nodeByName(nodename,which,searchgroup))
    return nodelist


def nodeByLayer(layer,searchgroup=None):
    """
    nodeByName:     Delivers all nodes of kind 'which' containing 'layer'  in 'searchgroup'
    :param searchgroup:    Parent node to search, default is the legend#s root
    :return:        List of found nodes
    """
    allnodes=nodeAll('layer',searchgroup)
    nodelist=[]
    for i in allnodes:
        if nodeIsLayer(i):
            if i.layer() == layer:
                nodelist.append(i)
    return nodelist



def nodePosition(node):
    """
    nodePosition:   Delivers the node position of 'node' in it's parent group
    :param node:    Node to check or name of node
    :return:        Position of node or None if node does not exist
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    count=0
    for child in node.parent().children():
        if child == node:
                return count
        count += 1
    return None


def nodeMove(node,position='down',target_node=None):
    """
    nodeMove:               Moves 'node' in position or position 'position' in group 'target_node'
    :param node:            Node to move or name of node to move
    :param target_node:     Target group to move 'node' to or name of the target group
    :return:                moved node or None if source or target node do not exist
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]

    if target_node == None:
        target_node = node.parent()
    else:
         if oeq_global.isStringOrUnicode(target_node):
            target_node = nodeByName(target_node)
            if len(target_node) == 0:
                return None
            target_node = target_node[0]
    if oeq_global.isStringOrUnicode(position):
        if position.upper() == 'DOWN':
            position = min(nodePosition(node)+2,nodeCount(node))
        elif position.upper() == 'UP':
            position = max(nodePosition(node)-1,0)
        elif position.upper() == 'TOP':
            position = 0
        elif position.upper() == 'BOTTOM':
            position=nodeCount(target_node)+1
    if type(position) != type(int()):
            position = nodeCount(target_node)

    cloned_node = node.clone()
    target_node.insertChildNode(position, cloned_node)
    node.parent().removeChildNode(node)
    oeq_global.OeQ_unlockQgis()
    return cloned_node


from PyQt4.QtCore import Qt


def nodeShow(node):
    """
    nodeShow:       Switch 'node' to visible
    :param node:    Node to show
    :return:        visibility state
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    node.setVisible(Qt.Checked)
    oeq_global.OeQ_unlockQgis()
    return node.isVisible()

def nodesShow(nodes):
    """
    nodesShow:      Switch 'nodes' to visible
    :param nodes:   list of nodes to show
    :return:        no return
    """
    for node in nodes:
        nodeShow(node)

def nodeHide(node):
    """
    nodeHide:       Switch 'nodes' to invisible
    :param nodes:   list of nodes to hide
    :return:        no return
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    node.setVisible(Qt.Unchecked)
    oeq_global.OeQ_unlockQgis()
    return node.isVisible()

def nodesHide(nodes):
    """
    nodesHide:      Switch 'nodes' to invisible
    :param nodes:   list of nodes to hide
    :return:        no return
    """
    for node in nodes:
        nodeHide(node)


def nodeStoreVisibility(node):
    """
    nodeStoreVisibility:    Stores the current visibility state in a custom property
                            (if the property does not already exist)
    :param node:            Node to work on
    :return:                Success True/False  or None if node not found
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]

    if node.customProperty("was_visible") == None:
            node.setCustomProperty("was_visible", node.isVisible())
            return True
    return False


def nodeRestoreVisibility(node):
    """
    nodeStoreVisibility:    Sets the visibility state to the state stored earlier
                            (and delete the custom property)
    :param node:            Node to work on
    :return:                node or None if node not found
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]

    if node.customProperty("was_visible") != None:
        if node.customProperty("was_visible") > 0:
            node.setVisible(Qt.Checked)
        else:
            node.setVisible(Qt.Unchecked)
        node.removeCustomProperty("was_visible")
    return node


def nodeToggleSoloAction(node):
        from mole.project import config
        from mole.qgisinteraction import legend
        print node.layer().name()
        #legend.nodeExitSolo()
        #legend.nodeInitSolo([config.investigation_shape_layer_name])



def nodeInitSolo(nodes):
    """
    nodeInitSolo:       Init Solo Mode (and Hide all existing nodes and show only 'nodes')
    :param nodes:       List of nodes to show solo
    :return:            True/False/None if node does not exist
    """
    if type(nodes) != type([]):
        nodes = [nodes]
    for node in nodeAll():
        if nodeStoreVisibility(node):
            nodeHide(node)
    nodesShow(nodes)


def nodeExitSolo():
    """
    nodeExitSolo:       Exit Solo Mode (and Restore visibility states)
    :return:            no return
    """
    for i in nodeAll():
        nodeRestoreVisibility(i)

def nodeCopy(node,newname=None,position=None,target_node=None):
    """
    nodeMove:               Moves 'node' in position or position 'position' in group 'target_node'
    :param node:            Node to move or name of node to move
    :param target_node:     Target group to move 'node' to or name of the target group
    :return:                moved node or None if source or target node do not exist
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]

    if target_node == None:
        target_node = node.parent()
    else:
         if oeq_global.isStringOrUnicode(target_node):
            target_node = nodeByName(target_node)
            if len(target_node) == 0:
                return None
            target_node = target_node[0]

    source_layer = node.layer()
    new_layer = iface.addVectorLayer(source_layer.source(), newname,source_layer.providerType())
    QgsMapLayerRegistry.instance().addMapLayer(new_layer, False)
    new_node = nodeByLayer(new_layer)[0]
    new_node = nodeMove(new_node,position,target_node)
    return new_node

def nodeCreateVectorLayer(nodename, position='bottom',target_node=None,path=None,source="Point",crs=None,providertype="ESRI Shapefile",indexfieldname='id'):
    if target_node == None:
        target_node = QgsProject.instance().layerTreeRoot()
    else:
         if oeq_global.isStringOrUnicode(target_node):
            target_node = nodeByName(target_node)
            if len(target_node) == 0:
                return None
            target_node = target_node[0]

    if path == None:
        path= oeq_global.OeQ_project_path()
    if crs == None:
        crs = config.project_crs
    new_layer = QgsVectorLayer(source + '?crs=' + crs, nodename, "memory")
    new_layer.setProviderEncoding('System')
    writer = QgsVectorFileWriter.writeAsVectorFormat(new_layer, os.path.join(path , nodename+'.shp'), "System", new_layer.crs(), providertype)
    if writer != QgsVectorFileWriter.NoError:
        oeq_global.OeQ_init_error(title='Write Error:', message=os.path.join(path , nodename+'.shp'))
        return None
    del writer
    iface.addVectorLayer(os.path.join(path , nodename+'.shp'),nodename, 'ogr')
    new_node = nodeMove(nodename,position,target_node)
    new_layer = new_node.layer()
    dataprovider = new_layer.dataProvider()
    dataprovider.addAttributes([QgsField(indexfieldname,  QVariant.Int)])
    new_layer.updateFields()

    oeq_global.OeQ_unlockQgis()

    return new_node



def nodeCreateGroup(nodename,position='bottom',target_node=None):
    if target_node == None:
        target_node = QgsProject.instance().layerTreeRoot()
    else:
         if oeq_global.isStringOrUnicode(target_node):
            target_node = nodeByName(target_node)
            if len(target_node) == 0:
                return None
            target_node = target_node[0]

    if oeq_global.isStringOrUnicode(position):
        if position.upper() == 'TOP':
            position = 0
        elif position.upper() == 'BOTTOM':
            position=nodeCount(target_node)+1
    if type(position) != type(int()):
            position = nodeCount(target_node)

    new_node = target_node.insertGroup(position, nodename)
    return new_node


def nodeSetActive(node):
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    iface.setActiveLayer(node.layer())



def testlayer():
    nodeCreateGroup('Testgroup1')
    nodeCreateGroup('Testgroup2',0)
    nodeCreateGroup('Testgroup3',0,'Testgroup1')
    nodeCreateVectorLayer('Testlayer1')
    nodeCreateVectorLayer('Testlayer2',None,'Testgroup2',source='Polygon')
    nodeCreateVectorLayer('Testlayer3',None,'Testgroup2',source='MultiPoint')
    nodeCreateVectorLayer('Testlayer2',None,'Testgroup1')
    nodeCreateVectorLayer('Testlayer4','Top','Testgroup2',source='LineString')


def nodeZoomTo(node):
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
        canvas = iface.mapCanvas()
        canvas.setExtent(node.layer().extent())
        canvas.zoomByFactor(1.1)