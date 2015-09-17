# -*- coding: utf-8 -*-

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

from qgis.core import QgsProject,QgsLayerTreeGroup,QgsLayerTreeLayer,QgsMapLayerRegistry
from qgis.utils import iface

def nodeIsLayer(node):
    """nodeIsLayer: Checks, weather node represents a Layer
    :param node: Node to check or name of node
    :return: True/False/None if node does not exist
    """
    if (type(node) == type('')) | (type(node) == type(u'')):
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
    if (type(node) == type('')) | (type(node) == type(u'')):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    if isinstance(node, QgsLayerTreeGroup):
        return True
    return False


def nodeAll(which='all',root=None):
    """nodeAll: Delivers all nodes of kind 'which' from node 'root'
    :param which: kind of node 'all'/'layer'/'group
    :param root: Parent node to search, default is the legend#s root
    :return: list of found nodes
    """
    if root == None:
        root = QgsProject.instance().layerTreeRoot()
    if (type(root) == type('')) | (type(root) == type(u'')):
        root = nodeByName(root)
        if len(root) == 0:
            root = None
        else:
            root = root[0]
    nodelist=[]
    for child in root.children():
        nodelist.append(child)
        if isinstance(child, QgsLayerTreeGroup):
            nodelist=nodelist + nodeAll(which,child)
    if which == 'group':
        return filter(lambda x: nodeIsGroup(x), nodelist)
    if which == 'layer':
        return filter(lambda x: nodeIsLayer(x), nodelist)
    return nodelist


def nodeCount(which='all',root=None):
    """nodeCount: Number of nodes of kind 'which' in 'root'
    :param which: kind of node 'all'/'layer'/'group
    :param root: Parent node to search, default is the legend#s root
    :return: Number of nodes
    """
    return len(nodeAll(which,root))


def nodeAllGroups(root=None):
    """
    nodeAllGroups:  Delivers all group nodes from node 'root'
    :param root:    Parent node to search, default is the legend#s root
    :return:        list of found nodes
    """
    return nodeAll('group',root)


def nodeAllLayers(root=None):
    """
    nodeAllLayers:  Delivers all layer nodes from node 'root'
    :param root:    Parent node to search, default is the legend#s root
    :return:        list of found nodes
    """
    return nodeAll('layer',root)


def nodeNames(which='all',root=None):
    """
    nodeNames:      Delivers all nodenames from node 'root'
    :param which:   kind of node 'all'/'layer'/'group'
    :param root:    Parent node to search, default is the legend#s root
    :return:        List of names of all found nodes
    """
    nodelist=nodeAll(which,root)
    namelist=[]
    for i in nodelist:
        if nodeIsGroup(i):
            namelist.append(i.name())
        if nodeIsLayer(i):
            namelist.append(i.layerName())
    return namelist


def nodeByName(nodename,which='all',root=None):
    """
    nodeByName:     Delivers all nodes of kind 'which' named 'nodename'  in 'root'
    :param which:   kind of node 'all'/'layer'/'group
    :param root:    Parent node to search, default is the legend#s root
    :return:        List of found nodes
    """
    allnodes=nodeAll(which,root)
    nodelist=[]
    for i in allnodes:
        if nodeIsGroup(i):
            if i.name() == nodename:
                nodelist.append(i)
        if nodeIsLayer(i):
            if i.layerName() == nodename:
                nodelist.append(i)
    return nodelist

def nodesByName(nodenames,which='all',root=None):
    """
    nodesByName:    Delivers all nodes of kind 'which' named 'nodenames'  in 'root' for multiple nodenames
    :param which:   kind of node 'all'/'layer'/'group
    :param root:    Parent node to search, default is the legend#s root
    :return:        List of found nodes for each name in 'nodenames' (as list of lists)
    """
    nodelist=[]
    for nodename in nodenames:
        nodelist.append(nodeByName(nodename,which,root))
    return nodelist


def nodeByLayer(layer,root=None):
    """
    nodeByName:     Delivers all nodes of kind 'which' containing 'layer'  in 'root'
    :param root:    Parent node to search, default is the legend#s root
    :return:        List of found nodes
    """
    allnodes=nodeAll('layer',root)
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
    if (type(node) == type('')) | (type(node) == type(u'')):
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


def nodeMove(node,direction='down',target_node=None):
    """
    nodeMove:               Moves 'node' in direction or position 'direction' in group 'target_node'
    :param node:            Node to move or name of node to move
    :param target_node:     Target group to move 'node' to or name of the target group
    :return:                moved node or None if source or target node do not exist
    """
    if (type(node) == type('')) | (type(node) == type(u'')):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]

    if target_node == None:
        target_node = node.parent()
        if direction == 'down':
                direction = min(nodePosition(node)+2,nodeCount(node))
        elif direction == 'up':
                direction = max(nodePosition(node)-1,0)
    else:
         if (type(target_node) == type('')) | (type(target_node) == type(u'')):
            target_node = nodeByName(target_node)
            if len(target_node) == 0:
                return None
            target_node = target_node[0]

    if direction == 'top':
        direction = 0
    if direction == 'bottom':
        direction=nodeCount(target_node)
    else:
        if type(direction) != type(int()):
                 direction = nodeCount(target_node)
    cloned_node = node.clone()
    target_node.insertChildNode(direction, cloned_node)
    node.parent().removeChildNode(node)
    return cloned_node


from PyQt4.QtCore import Qt


def nodeShow(node):
    """
    nodeShow:       Switch 'node' to visible
    :param node:    Node to show
    :return:        no return
    """
    if (type(node) == type('')) | (type(node) == type(u'')):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    print node
    node.setVisible(Qt.Checked)

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
    if (type(node) == type('')) | (type(node) == type(u'')):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    node.setVisible(Qt.Unchecked)

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
    if (type(node) == type('')) | (type(node) == type(u'')):
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
    if (type(node) == type('')) | (type(node) == type(u'')):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]

    if node.customProperty("was_visible") > 0:
        node.setVisible(Qt.Checked)
    else:
        node.setVisible(Qt.Unchecked)
    node.removeCustomProperty("was_visible")
    return node


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
    nodeMove:               Moves 'node' in direction or position 'direction' in group 'target_node'
    :param node:            Node to move or name of node to move
    :param target_node:     Target group to move 'node' to or name of the target group
    :return:                moved node or None if source or target node do not exist
    """
    if (type(node) == type('')) | (type(node) == type(u'')):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]

    if target_node == None:
        target_node = node.parent()
    else:
         if (type(target_node) == type('')) | (type(target_node) == type(u'')):
            target_node = nodeByName(target_node)
            if len(target_node) == 0:
                return None
            target_node = target_node[0]

    if position == 'top':
        position = 0
    elif position == 'bottom':
        position = nodeCount(target_node)
    else:
        if type(position) != type(int()):
            position = max(nodePosition(node)-1,0)
    source_layer = node.layer()
    new_layer = iface.addVectorLayer(source_layer.source(), newname,source_layer.providerType())
    QgsMapLayerRegistry.instance().addMapLayer(new_layer, False)
    new_node = nodeByLayer(new_layer)[0]
    new_node = nodeMove(new_node,position,target_node)
    return new_node
