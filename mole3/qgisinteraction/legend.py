# -*- coding: utf-8 -*-

"""
Project:        OpenEQuarter
Subproject:     Mole
Type:           A QGIS plugin
Module:         legend
Package:        mole3.qgisinteraction
Description:    Functions to deal with the QGIS Legend
Authors:        Werner 'Max' Kaul, UdK-Berlin (max)
Creation Date:  2015-09-16
Latest Changes: 2015-09-16 (max)

(C) Open eQuarter Project Team UdK-Berlin
"""

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsProject,QgsLayerTreeGroup,QgsLayerTreeLayer,QgsProject,QgsVectorFileWriter,QgsVectorLayer,QgsField,QgsFeature,QgsCoordinateReferenceSystem,QgsCoordinateTransform
from qgis.utils import iface
from mole3 import oeq_global
from mole3.project import config
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

def nodeExists(nodename):
        node = nodeByName(nodename)
        if not node:
            return False
        return True


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
        return [x for x in nodelist if nodeIsGroup(x)]
    if which == 'layer':
        return [x for x in nodelist if nodeIsLayer(x)]
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



def nodePosition(node,searchgroup=None):
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

    if searchgroup == None:
        searchgroup = QgsProject.instance().layerTreeRoot()

    count=0
    for child in searchgroup.children():
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
        if not node:
            return None
        node = node[0]

    if not target_node:
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
    #oeq_global.OeQ_wait_for_renderer(60000)
    node.parent().removeChildNode(node)
    #oeq_global.OeQ_wait_for_renderer(60000)
    return cloned_node



from qgis.PyQt.QtCore import Qt

def nodeExpand(node):
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
    #if nodeIsGroup(node):
    node.setExpanded(True)
    #oeq_global.OeQ_unlockQgis()
    #oeq_global.OeQ_wait(0.1)
    return node.isExpanded()

def nodeCollapse(node):
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
    #if nodeIsGroup(node):
    node.setExpanded(False)
    #oeq_global.OeQ_unlockQgis()
    #oeq_global.OeQ_wait(0.1)
    return node.isExpanded()

def nodeShow(node):
    """
    nodeShow:       Switch 'node' to visible
    :param node:    Node to show
    :return:        visibility state
    """
    #print node
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node:
            return None
        node = node[0]
    node.setVisible(Qt.Checked)
    #oeq_global.OeQ_unlockQgis()
    #oeq_global.OeQ_wait(0.1)
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
    #oeq_global.OeQ_unlockQgis()
    #oeq_global.OeQ_wait(0.1)
    return node.isVisible()

def nodesHide(nodes):
    """
    nodesHide:      Switch 'nodes' to invisible
    :param nodes:   list of nodes to hide
    :return:        no return
    """
    for node in nodes:
        nodeHide(node)


def nodeStoreVisibility(node,restorevariablename="was_visible_before_Solo"):
    """
    nodeStoreVisibility:    Stores the current visibility state in a custom property
                            (if the property does not already exist)
    :param node:            Node to work on
    :return:                Success True/False  or None if node not found
    """
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node:
            return None
        node = node[0]

    if node.customProperty(restorevariablename) == None:
            node.setCustomProperty(restorevariablename, node.isVisible())
            return True
    return False


def nodeRestoreVisibility(node,restorevariablename="was_visible_before_Solo"):
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

    if node.customProperty(restorevariablename) != None:
        if node.customProperty(restorevariablename) > 0:
            node.setVisible(Qt.Checked)
        else:
            node.setVisible(Qt.Unchecked)
        node.removeCustomProperty(restorevariablename)
    return node


def nodeToggleSoloAction(node,state):
        if oeq_global.isStringOrUnicode(node):
            node = nodeByName(node)
            if len(node) == 0:
                return None
            node = node[0]

        if state == 2:
            nodeInitSolo(node.customProperty("SoloLayers"))
        elif state == 0:
            nodeExitSolo()

        #legend.nodeExitSolo()
        #legend.nodeInitSolo([config.investigation_shape_layer_name])
#node.visibilityChanged.connect(list_view.model().itemChanged.connect(self.check_progress_status)

def nodeInitRadioAction(node,state):
        if state == 2:
            nodeInitRadio(node.customProperty("SoloLayers"))
        elif state == 0:
            nodeExitSolo()


def nodeInitSolo(visiblenodes=[]):
    """
    nodeInitSolo:       Init Solo Mode (and Hide all existing nodes and show only 'nodes')
    :param nodes:       List of nodes to show solo
    :return:            True/False/None if node does not exist
    """

    if type(visiblenodes) != type([]):
        visiblenodes = [visiblenodes]
    nodes_to_show =[]
    for node in visiblenodes:
        if oeq_global.isStringOrUnicode(node):
            node = nodeByName(node)
            if len(node) == 0:
                continue
            node = node[0]
        nodes_to_show.append( node.layer().name())

    for anode in nodeAllLayers():

         if nodeStoreVisibility(anode):
            if [x for x in nodes_to_show if x == anode.layer().name()]:
            #if anode.layer().name() in nodes_to_show:
                nodeShow(anode)
            else:
                nodeHide(anode)

def nodeRadioAdd(node,radiogroup=None):
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node: return None
        node = node[0]

    if isinstance(node, QgsLayerTreeLayer):
        if isinstance(radiogroup, QgsLayerTreeGroup):
           radiogroup = radiogroup.name()
        if not node.customProperty("radiogroup"):
            node.setCustomProperty("radiogroup" , radiogroup)
            nodeHide(node)
            node.visibilityChanged.connect(nodeRadioSwitch)
    elif isinstance(node, QgsLayerTreeGroup):
        for node_item in nodeAllLayers(node):
            nodeRadioAdd(node_item,node)
    return node

def nodeRadioRemove(node,radiogroup=None):
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node: return None
        node = node[0]

    if isinstance(node, QgsLayerTreeLayer):
        if isinstance(radiogroup, QgsLayerTreeGroup):
            radiogroup = radiogroup.name()
        if node.customProperty("radiogroup"):
            node.removeCustomProperty("radiogroup")
            node.visibilityChanged.disconnect(nodeRadioSwitch)
    elif isinstance(node, QgsLayerTreeGroup):
        for node_item in nodeAllLayers(node):
            nodeRadioRemove(node_item,node)
    return node

def nodeRadioSwitch(node,state=None):
    if state:
        if oeq_global.isStringOrUnicode(node):
            node = nodeByName(node)
            if not node: return None
            node = node[0]
            nodeExpand(node)
        radiogroup = node.customProperty("radiogroup")
        for nodeitem in nodeAllLayers():
            if nodeitem.layer().name() != node.layer().name():
                if nodeitem.customProperty("radiogroup") == radiogroup:
                    nodeCollapse(nodeitem)
                    nodeHide(nodeitem)



def nodeRemove(node,physical=False):
    import os
    from mole3.qgisinteraction import layer_interaction
    from mole3 import oeq_global
    os.environ['PATH'] += ":"+"/usr/local/bin"
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    result = layer_interaction.remove_layer(node.layer(),physical=physical)
    oeq_global.OeQ_wait(0.3)
    return result




def nodeExitSolo():
    """
    nodeExitSolo:       Exit Solo Mode (and Restore visibility states)
    :return:            no return
    """
    for i in nodeAllLayers():
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
    #oeq_global.OeQ_wait_for_renderer(60000)
    new_node = nodeByLayer(new_layer)[0]
    new_node = nodeMove(new_node,position,target_node)
    QgsProject.instance().addMapLayer(new_layer, False)
    #oeq_global.OeQ_wait_for_renderer(60000)
    #oeq_global.OeQ_unlockQgis()
    #oeq_global.OeQ_wait(0.1)
    return new_node


def nodeDuplicate(node,newname=None,position='bottom',target_node=None):
    import time
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
    #
    #print node.layer().name()
    #print newname
    layer = node.layer()
    # source of the layer
    provider = layer.dataProvider()
    #print "---------------------"
    #print provider.crs().authid()
    #print layer.crs().authid()
    #print "---------------------"
    # creation of the shapefiles:
    pathfile = os.path.join(oeq_global.OeQ_project_path(),newname+'.shp')
    ct_pathfile = os.path.join(oeq_global.OeQ_project_path(),newname+'.qml')
    writer = QgsVectorFileWriter(pathfile, "CP1250", provider.fields(), provider.geometryType(), layer.crs(), "ESRI Shapefile")
    #print writer
    outelem = QgsFeature()
    # iterating over the input layer
    for elem in layer.getFeatures():
             outelem.setGeometry(elem.geometry() )
             outelem.setAttributes(elem.attributes())
             writer.addFeature(outelem)
    del writer
    oeq_global.OeQ_wait_for_file(pathfile)
    #time.sleep(1)
    newlayer = QgsVectorLayer(pathfile, newname, "ogr")

    #print layer.isValid()
    QgsProject.instance().addMapLayer(newlayer, True)
    newlayer.setCrs(layer.crs())
    #oeq_global.OeQ_wait_for_renderer(60000)
    #print newlayer.name()


    newnode = nodeByName(newlayer.name())
    if len(newnode) == 0:
        return None
    newnode = newnode[0]
   # oeq_global.OeQ_unlockQgis()
    #time.sleep(1)
    newlayer.loadNamedStyle(ct_pathfile)
    nodeCollapse(newnode)
    #time.sleep(1)
    #position = nodePosition(node,target_node)
    newnode=nodeMove(newnode,position,target_node)
    #time.sleep(1)
    #oeq_global.OeQ_unlockQgis()
    #oeq_global.OeQ_wait(0.5)
    #print "+++++++++++++++"
    return newnode

def nodeCopyAttributes(node,target_node,attributenames=None,indexfield = config.building_id_key):
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node: return None
        node = node[0]
    source_layer = node.layer()
    source_field_names = [field.name() for field in source_layer.dataProvider().fields() ]
    if not source_field_names: return None

    if oeq_global.isStringOrUnicode(target_node):
        target_node = nodeByName(target_node)
        if  not target_node: return None
        target_node = target_node[0]
    target_layer = target_node.layer()
    target_field_names = [field.name() for field in target_layer.dataProvider().fields()]
    #print "X1"
    #print attributenames
    if attributenames:
        fieldnames_to_copy = [x for x in attributenames if x in source_field_names]
    else:
        fieldnames_to_copy = source_field_names
    #print fieldnames_to_copy
    fieldnames_to_copy = [x for x in fieldnames_to_copy if x != indexfield]

    fieldnames_to_add = [x for x in fieldnames_to_copy if x not in target_field_names]

    fields_to_add = [x for x in source_layer.dataProvider().fields() if x.name() in fieldnames_to_add]
    target_layer.dataProvider().addAttributes(fields_to_add)
    #print "X2"
    #target_layer.startEditing()
    target_field_names = [field.name() for field in target_layer.dataProvider().fields()]
    target_field_ids = [[i for i,x in enumerate(target_field_names) if x == fieldname][0] for fieldname in fieldnames_to_copy]
    for feature in target_layer.dataProvider().getFeatures():
        source_feature = [x for x in source_layer.dataProvider().getFeatures() if x[indexfield] == feature[indexfield]]
        if  not source_feature: continue
        source_feature = source_feature[0]
        attr = dict(list(zip(target_field_ids,[source_feature[x] for x in fieldnames_to_copy])))
        #target_layer.dataProvider().changeAttributeValues({feature.id():attr})
        target_layer.updateFields()
       # print "X3"

    #print "X4"
    #target_layer.commitChanges()
    #print "X5"
    return target_layer

def nodeDeleteAllAttributes(node,indexfield = None):
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node: return None
        node = node[0]
    layer = node.layer()
    fields = layer.dataProvider().fields().toList()
    to_remove = []
    count = 0
    if not bool(indexfield):
        layer.dataProvider().deleteAttributes(list(range(0,len(fields)-1)))
    for field in fields:
        if field.name() != indexfield:
            to_remove.append(count)
        count += 1
    layer.dataProvider().deleteAttributes(to_remove)
    layer.updateFields()


def nodeCopyAsMemory(node,newname=None,position=None,target_node=None):
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
    #print source_layer.name()
    #print source_layer.source()
    #print source_layer.providerType() + u'?crs=' + source_layer.crs().authid()
    #print newname
    new_layer = QgsVectorLayer( 'Polygon' + '?crs=' + source_layer.crs().authid(), newname, "memory")
    new_layer.setProviderEncoding('System')
    QgsProject.instance().addMapLayer(new_layer, True)
    #oeq_global.OeQ_wait_for_renderer(60000)
    new_node = nodeByName(newname)[0]
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
    #test
    dataprovider = new_layer.dataProvider()
    dataprovider.addAttributes([QgsField(indexfieldname, QVariant.Int)])
    new_layer.updateFields()
    writer = QgsVectorFileWriter.writeAsVectorFormat(new_layer, os.path.join(path , nodename+'.shp'), "System", new_layer.crs(), providertype)
    if writer != QgsVectorFileWriter.NoError:
        oeq_global.OeQ_push_error(title='Write Error:', message=os.path.join(path , nodename+'.shp'))
        return None
    del writer
    oeq_global.OeQ_wait_for_file(os.path.join(path , nodename+'.shp'))
    iface.addVectorLayer(os.path.join(path , nodename+'.shp'),nodename, 'ogr')
    #oeq_global.OeQ_wait_for_renderer(60000)
    new_node = nodeMove(nodename,position,target_node)
    new_layer = new_node.layer()
    #dataprovider = new_layer.dataProvider()
    #dataprovider.addAttributes([QgsField(indexfieldname,  QVariant.Int)])
    #new_layer.updateFields()

    #oeq_global.OeQ_unlockQgis()

    return new_node


def nodeCreateMemoryLayer(nodename, position='bottom',target_node=None,source="Point",crs=None,indexfieldname='id'):
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
    QgsProject.instance().addMapLayer(new_layer, True)
    #oeq_global.OeQ_wait_for_renderer(60000)
    new_node = nodeMove(nodename,position,target_node)
    new_layer = new_node.layer()
    dataprovider = new_layer.dataProvider()
    dataprovider.addAttributes([QgsField(indexfieldname,  QVariant.Int)])
    new_layer.updateFields()
    #oeq_global.OeQ_unlockQgis()

    return new_node


def nodeSaveMemoryLayer(node , path=None , providertype="ESRI Shapefile"):
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None

    new_layer = node[0].layer()
    new_layer_name = new_layer.name()
    writer = QgsVectorFileWriter.writeAsVectorFormat(new_layer, os.path.join(path , new_layer_name+'.shp'), "System", new_layer.crs(), providertype)
    if writer != QgsVectorFileWriter.NoError:
        oeq_global.OeQ_push_error(title='Write Error:', message=os.path.join(path , new_layer_name+'.shp'))
        return None
    del writer
    oeq_global.OeQ_wait_for_file(os.path.join(path , new_layer_name+'.shp'))
    iface.addVectorLayer(os.path.join(path , new_layer_name+'.shp'),new_layer_name, 'ogr')
    #oeq_global.OeQ_wait_for_renderer(60000)
    target_node = node.parent()
    position = nodePosition(node,target_node)
    new_node = nodeMove(new_layer_name,position,target_node)
    #oeq_global.OeQ_unlockQgis()

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





def nodeConvertCRSold(node,crs=None):
    import os, subprocess
    os.environ['PATH'] += ":"+"/usr/local/bin"
    from mole3 import oeq_global
    from mole3.qgisinteraction import layer_interaction
    if crs == None:
        crs='epsg:4326' #default is WGS84
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    src_crs = node.layer().crs().authid()
    name=node.layer().name()
    src_path = node.layer().source()
    src_dir =os.path.dirname(src_path)
    src_name = os.path.basename(src_path).split('.')[0]
    src_ext = src_path.split('.')[1]
    tgt_name = src_name+'_tmp'
    tgt_path = os.path.join(src_dir,tgt_name+'.'+src_ext)
    tgt_crs=QgsCoordinateReferenceSystem(int(crs.split(':')[1]), QgsCoordinateReferenceSystem.EpsgCrsId)
    bu_name= src_name+'_'+src_crs.split(':')[1]
    bu_path = os.path.join(src_dir,bu_name+'.'+src_ext)
    #print src_path
    #print tgt_path
    #print src_crs
    #print crs
    cmd = ' '.join(["ogr2ogr", "-f","'ESRI Shapefile'","-s_srs",src_crs,"-t_srs",crs,"'"+tgt_path+"'","'"+src_path+"'"])
    #print cmd
    #try:
    #it is necessary
    try:
        process = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print((process.stdout.read()))
    except:
        oeq_global.OeQ_push_error('nodeClipByShapefile :',"ogr2ogr failed to run -clipsrc !")
    #subprocess.call(cmd,shell=True)
    #except:
    #oeq_global.OeQ_wait(3)

    try:
        layer_interaction.remove_filegroup(src_dir,bu_name,ignore=['qml'])
    except:
        pass
    #print bu_path
    try:
        layer_interaction.rename_filegroup(src_dir,src_name,bu_name,ignore=['qml'])
    except:
        pass
    try:
        layer_interaction.rename_filegroup(src_dir,tgt_name,src_name,ignore=['qml'])
    except:
        pass
    #node.parent().removeChildNode(node)
    #print bu_path
    iface.addVectorLayer(src_path,name, 'ogr')
    oeq_global.OeQ_wait_for_renderer()
    newnode=nodeByName(name)
    if newnode:
            return newnode[0]
    return None

def nodeConvertCRS(node,crs=None):
    import os, subprocess
    os.environ['PATH'] += ":"+"/usr/local/bin"
    from mole3 import oeq_global
    from mole3.qgisinteraction import layer_interaction
    if crs == None:
        crs='epsg:4326' #default is WGS84
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    src_crs = node.layer().crs().authid()
    name=node.layer().name()
    src_path = node.layer().source()
    src_dir =os.path.dirname(src_path)
    src_name = os.path.basename(src_path).split('.')[0]
    src_ext = src_path.split('.')[1]
    tgt_name = src_name+'_tmp'
    tgt_path = os.path.join(src_dir,tgt_name+'.'+src_ext)
    bu_name= src_name+'_'+src_crs.split(':')[1]
    bu_path = os.path.join(src_dir,bu_name+'.'+src_ext)
    nodeVectorSave(node,tgt_path,crs)
    oeq_global.OeQ_wait_for_file(tgt_path)
    nodeRemove(node)
    #    return None
    layer_interaction.remove_filegroup(src_dir,bu_name,ignore=['qml'])
    layer_interaction.rename_filegroup(src_dir,src_name,bu_name,ignore=['qml'])
    oeq_global.OeQ_wait_for_file(bu_name)
    layer_interaction.rename_filegroup(src_dir,tgt_name,src_name,ignore=['qml'])
    oeq_global.OeQ_wait_for_file(src_path)

    iface.addVectorLayer(src_path,name, 'ogr')
    oeq_global.OeQ_wait_for_renderer()

    newnode=nodeByName(name)
    if newnode:
            newnode[0].layer().triggerRepaint()
            #oeq_global.OeQ_wait_for_renderer(60000)
            return newnode[0]
    return None



def nodeClipByShapefile(node,clip_filepath=None,target_filepath=None):
    import os, subprocess
    from qgis.core import QgsMessageLog
    from mole3 import oeq_global
    from mole3.qgisinteraction import layer_interaction
    #add path in case ogr2ogr can not be found

    #check if a clippath is given
    if clip_filepath == None:
        return None

    #if node is a string get the according node
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]

    #source CRS
    src_crs = node.layer().crs().authid()

    src_layer_name = node.layer().name()
    src_layer_filepath = node.layer().source()
    #remove sourcenode from the qgislegend
    nodeRemove(node)


    src_dir =os.path.dirname(src_layer_filepath)
    src_name = os.path.basename(src_layer_filepath).split('.')[0]
    src_ext = src_layer_filepath.split('.')[1]


    bu_name= src_name+'_before_clip'
    bu_path = os.path.join(src_dir,bu_name+'.'+src_ext)

    #convert original to backup

    if not target_filepath:
        #remove older backups
        layer_interaction.remove_filegroup(src_dir,bu_name,ignore=['qml'])
        #rename original to backup
        layer_interaction.rename_filegroup(src_dir,src_name,bu_name,ignore=['qml'])
        oeq_global.OeQ_wait_for_file(bu_name)
        ret=subprocess.call(["ogr2ogr", "-f", "ESRI Shapefile","-clipsrc", clip_filepath, src_layer_filepath, bu_path])
        if ret!=0:
            QgsMessageLog.logMessage("nodeClipByShapefile : ogr2ogr failed to run -clipsrc(1) !",'Error in nodeClipByShapefile', QgsMessageLog.CRITICAL)
            oeq_global.OeQ_push_error('nodeClipByShapefile :',"ogr2ogr failed to run -clipsrc(1) !")
            return None
        oeq_global.OeQ_wait_for_file(src_layer_filepath)
        newlayer = iface.addVectorLayer(src_layer_filepath,src_layer_name, 'ogr')
        oeq_global.OeQ_wait_for_renderer()
    else:
        target_name = os.path.basename(target_filepath).split('.')[0]
        #check if it is filename or filepath
        if os.path.basename(target_filepath) == target_filepath:
            target_filepath=os.path.join(src_dir,target_filepath)
        target_dir = os.path.dirname(target_filepath)
        #remove old clip files
        layer_interaction.remove_filegroup(target_dir,target_name,ignore=['qml'])
        ret = subprocess.call(["ogr2ogr", "-f", "ESRI Shapefile","-clipsrc", clip_filepath, target_filepath, src_layer_filepath])
        if ret!=0:
            QgsMessageLog.logMessage("nodeClipByShapefile : ogr2ogr failed to run -clipsrc(2) !",'Error in nodeClipByShapefile', QgsMessageLog.CRITICAL)
            oeq_global.OeQ_push_error('nodeClipByShapefile :',"ogr2ogr failed to run -clipsrc(2) !")
            return None
        oeq_global.OeQ_wait_for_file(target_filepath)
        newlayer = iface.addVectorLayer(target_filepath,src_layer_name, 'ogr')
        oeq_global.OeQ_wait_for_renderer()
    if not newlayer:
        QgsMessageLog.logMessage("nodeClipByShapefile : Could not open layer '"+str(target_filepath)+"' !",'Error in nodeClipByShapefile', QgsMessageLog.CRITICAL)
        oeq_global.OeQ_push_error('nodeClipByShapefile :',"Could not open layer '"+str(target_filepath)+"' !")
        return None
    newlayer.setCrs(QgsCoordinateReferenceSystem(int(src_crs.split(':')[1])), QgsCoordinateReferenceSystem.EpsgCrsId)
    newnode = nodeByLayer(newlayer)
    if not newnode:
        QgsMessageLog.logMessage("nodeClipByShapefile : Could not find node for new layer!",'Error in nodeClipByShapefile', QgsMessageLog.CRITICAL)
        oeq_global.OeQ_push_error('nodeClipByShapefile :',"Could not find node for new layer!")
        return None
    return newnode[0]


def nodeClipByShapenode(node,clip_node=None,target_path=None):
    import os, subprocess
    from mole3 import oeq_global
    #os.environ['PATH'] += ":"+"/usr/local/bin"
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if len(node) == 0:
            return None
        node = node[0]
    if oeq_global.isStringOrUnicode(clip_node):
        clip_node = nodeByName(clip_node)
        if len(clip_node) == 0:
            return None
        clip_node = clip_node[0]
    return nodeClipByShapefile(node,clip_node.layer().source(),target_path)

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
    import time

    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node: return None
        node = node[0]

        canvas = iface.mapCanvas()
        canvas.freeze(True)
        extent=node.layer().extent()
        canvas.setExtent(extent)
        center =canvas.center()
        #canvas.zoomByFactor(1.1)
        #limit scale to openstreetmap min
        #print canvas.scale()
        if canvas.scale() < 1700/1.1:
            canvas.zoomScale(1700)
        else:
            canvas.zoomByFactor(1.1)
        canvas.setCenter(center)
        canvas.freeze(False)
        canvas.refresh()
        #oeq_global.OeQ_wait_for_renderer(60000)



def nodeGetExtent(node):
    canvas = iface.mapCanvas()
    #canvas.freeze(True)
    backup_extent = canvas.extent()
    nodeZoomTo(node)
    node_extent = canvas.extent()
    canvas.setExtent(backup_extent)
    canvas.refresh()
    return node_extent


def nodeVectorSave(node,filepath=None,crs=None,load=False):
    from qgis.core import QgsCoordinateReferenceSystem,QgsVectorFileWriter
    from qgis.utils import iface
    from mole3 import oeq_global
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node: return None
        node = node[0]
    if not filepath:
        filepath=node.layer().source()
    if not crs:
        crs=node.layer().crs()
    else:
        crs = QgsCoordinateReferenceSystem(int(crs.split(':')[1]), QgsCoordinateReferenceSystem.EpsgCrsId)
    QgsVectorFileWriter.writeAsVectorFormat( node.layer(),filepath,'System',crs,'ESRI Shapefile')
    if load:
        iface.addVectorLayer(filepath,None, 'ogr')
        #oeq_global.OeQ_wait_for_renderer(60000)

def nodeCreateDatabase(node,database_layer_name,reference_crs=None,overwrite=True, category = None,subcategory=None,position='bottom'):
    from mole3 import oeq_global
    from mole3.project import config
    from mole3.qgisinteraction import layer_interaction
    from qgis.PyQt.QtCore import QVariant
    #get node for building_outline if only layer name is given
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node:
            oeq_global.OeQ_push_warning('nodeCreateDatabase :','No building outlines !')
            return None
    node = node[0]
    #remove database if necessary
    if overwrite:
        nodeRemove(database_layer_name,physical=True)
    #use project reference crs if not given
    if not bool(reference_crs):
        reference_crs = config.project_crs
    #generate db from building outline layer
    db_layer_node = nodeDuplicate(node,database_layer_name)
    #convert db layer to reference crs
    db_layer_node = nodeConvertCRS(db_layer_node,reference_crs)
    if not db_layer_node:
        oeq_global.OeQ_push_warning('nodeCreateDatabase :','Could not build database !')
        return None
    #create category group in legend
    if category:
        if not nodeExists(category):
            cat=nodeCreateGroup(category,position)
        else:
            cat=nodeByName(category)[0]
        nodeHide(cat)
        #create subcategory group in legend
        if subcategory:
            if not nodeExists(subcategory):
                subcat=nodeCreateGroup(subcategory,'bottom',cat)
            else:
                subcat=nodeByName(subcategory)[0]
            nodeHide(subcat)
            db_layer_node=nodeMove(db_layer_node,'bottom',subcat)
            nodeCollapse(subcat)
        else:
            db_layer_node=nodeMove(db_layer_node,'bottom',cat)
            nodeCollapse(cat)
    return db_layer_node


def nodeCreateSampleLayer(node, sample_layer_name, reference_crs=None, overwrite=True, category=None,
                       subcategory=None, position='bottom'):
    from mole3 import oeq_global
    from mole3.project import config
    from mole3.qgisinteraction import layer_interaction
    from qgis.PyQt.QtCore import QVariant
    # get node for building_outline if only layer name is given
    if oeq_global.isStringOrUnicode(node):
        node = nodeByName(node)
        if not node:
            oeq_global.OeQ_push_warning('nodeCreateSampleLayer :', 'No building coordinates !')
            return None
    node = node[0]
    # remove database if necessary
    if overwrite:
        nodeRemove(sample_layer_name, physical=True)
    # use project reference crs if not given
    if not reference_crs:
        reference_crs = config.project_crs
    # generate samplelayer from building coordinates layer
    sample_layer_node = nodeDuplicate(node, sample_layer_name)
    # convert db layer to reference crs
    sample_layer_node = nodeConvertCRS(sample_layer_node, reference_crs)
    if not sample_layer_node:
        oeq_global.OeQ_push_warning('nodeCreateSampleLayer :', 'Could not build samplelayer !')
        return None

    #create category group in legend
    if category:
        if not nodeExists(category):
            cat=nodeCreateGroup(category,position)
        else:
            cat=nodeByName(category)[0]
        nodeHide(cat)
        #create subcategory group in legend
        if subcategory:
            if not nodeExists(subcategory):
                subcat=nodeCreateGroup(subcategory,'bottom',cat)
            else:
                subcat=nodeByName(subcategory)[0]
            nodeHide(subcat)
            sample_layer_node=nodeMove(sample_layer_node,'bottom',subcat)
            nodeCollapse(subcat)
        else:
            sample_layer_node=nodeMove(sample_layer_node,'bottom',cat)
            nodeCollapse(cat)
    return sample_layer_node

#legend.nodeCreateSampleLayer('BLD Centroids', 'Sample Results', reference_crs=None, overwrite=True, category='Data',subcategory=None, position='bottom')


def nodeCreateBuildingIDs(building_outline_node):
    """
    Add a PERIMETER, AREA, BLD_ID and GKN field to the layer's attribute table and populate them with appropiate values.
    Delete duplicate features and finally remove the FID-field
    :param housing_layer: The layer whose attribute-table shall be edited
    :type housing_layer: QgsVectorLayer
    :return: If the changes were commited
    :rtype: bool
    """
    from mole3 import oeq_global
    from mole3.project import config
    from mole3.qgisinteraction import layer_interaction
    from qgis.PyQt.QtCore import QVariant
    #get node for building_outline if only layer name is given
    if oeq_global.isStringOrUnicode(building_outline_node):
        building_outline_node = nodeByName(building_outline_node)
        if not building_outline_node:
            oeq_global.OeQ_push_warning('nodeCreateDatabase :','No building outlines !')
            return None
        building_outline_node = building_outline_node[0]

    #try:
    building_outline_layer=building_outline_node.layer()
    building_outline_layer.startEditing()
    # NEW
    attributes = [QgsField(config.building_id_key, QVariant.String),
                  QgsField('AREA', QVariant.Double),
                  QgsField('PERIMETER', QVariant.Double),
                  QgsField('GKN', QVariant.String)]
    layer_interaction.add_attributes_if_not_exists(building_outline_layer, attributes)
    provider= building_outline_layer.dataProvider()
    #set attributes for all features
    building_id = 0
    for feat in provider.getFeatures():
            #get geometry
            geometry = feat.geometry()
            attributevalues = {building_outline_layer.fieldNameIndex(config.building_id_key): '{}'.format(building_id),
                               building_outline_layer.fieldNameIndex('AREA'): geometry.area(),
                               building_outline_layer.fieldNameIndex('PERIMETER'): geometry.length(),
                               building_outline_layer.fieldNameIndex('GKN'): feat['GKN_ALK']}
            provider.changeAttributeValues({feat.id(): attributevalues})
            building_id += 1



    # END NEW


    '''
    provider.addAttributes([QgsField(config.building_id_key, QVariant.String)])
    name_to_index = provider.fieldNameMap()
    building_index = name_to_index[config.building_id_key]
    try:
        fid_index = name_to_index['FID']
    except:
        pass

    building_id = 0

    for feature in provider.getFeatures():
        # if oeq_global.isnull(feature.attribute('FID')):
        # if feature.attribute(config.building_id_key) == 0:
        geometry = feature.geometry()
        provider.changeAttributeValues({feature.id(): {building_index: '{}'.format(building_id)}})
        building_id += 1
        # else:
        # These features are most likely to be duplicates of those that have an FID-entry
        #    provider.deleteFeatures([feature.id()])
    '''
    #provider.deleteAttributes([fid_index])
    return building_outline_layer.commitChanges()
    #except AttributeError, Error:
    #    print(__name__, Error)
    #    return False

def nodeGetBuildingData(building_coordinates_node):
    """
    Add a PERIMETER, AREA, and BLD_ID field to the layer's attribute table and populate them with appropiate values.
    Delete duplicate features and finally remove the FID-field
    :param housing_layer: The layer whose attribute-table shall be edited
    :type housing_layer: QgsVectorLayer
    :return: If the changes were commited
    :rtype: bool
    """
    from mole3 import oeq_global
    from mole3.webinteraction import googlemaps,nominatim
    from qgis.PyQt.QtCore import QVariant
    #get node for building_outline if only layer name is given
    if oeq_global.isStringOrUnicode(building_coordinates_node):
        building_coordinates_node = nodeByName(building_coordinates_node)
        if not building_coordinates_node:
            oeq_global.OeQ_push_warning('nodeGetBuildingData :','No building coordinates !')
            return None
        building_coordinates_node = building_coordinates_node[0]

    building_coordinates_layer=building_coordinates_node.layer()
    crs=int(building_coordinates_layer.crs().authid().split(':')[1])
    provider = building_coordinates_layer.dataProvider()
    building_coordinates_layer.startEditing()

    provider.addAttributes([QgsField('BLD_LAT1', QVariant.Double),
                QgsField('BLD_LON1', QVariant.Double),
                QgsField('BLD_LAT2', QVariant.Double),
                QgsField('BLD_LON2', QVariant.Double),
                QgsField('BLD_CRS', QVariant.Double),
                QgsField('BLD_NUM', QVariant.String),
                QgsField('BLD_STR', QVariant.String),
                QgsField('BLD_CTY', QVariant.String),
                QgsField('BLD_COD', QVariant.String),
                QgsField('BLD_CTR', QVariant.String)])

    name_to_index = provider.fieldNameMap()
    lat1_index = name_to_index['BLD_LAT1']
    lon1_index = name_to_index['BLD_LON1']
    lat2_index = name_to_index['BLD_LAT2']
    lon2_index = name_to_index['BLD_LON2']
    crs_index = name_to_index['BLD_CRS']
    num_index = name_to_index['BLD_NUM']
    str_index = name_to_index['BLD_STR']
    cty_index = name_to_index['BLD_CTY']
    cod_index = name_to_index['BLD_COD']
    ctr_index = name_to_index['BLD_CTR']

    for feature in provider.getFeatures():
        geometry = feature.geometry()
        #print geometry.asPoint().x()
        #print geometry.asPoint().y()
        #print crs
        bdata=nominatim.getBuildingLocationDataByCoordinates(geometry.asPoint().x(),geometry.asPoint().y(),crs)
        #print bdata
        if bdata:
            bdata=bdata[0]
            values = {lat1_index: geometry.asPoint().x(),
                      lon1_index: geometry.asPoint().y(),
                      lat2_index: bdata['latitude'],
                      lon2_index: bdata['longitude'],
                      crs_index:crs,
                      num_index:bdata['street_number'],
                      str_index:bdata['route'],
                      cod_index:bdata['postal_code'],
                      cty_index:bdata['administrative_area_level_1'],
                      ctr_index:bdata['country'],
                      }
        else:
            values = {lat1_index: geometry.asPoint().x(),
                      lon1_index: geometry.asPoint().y()}
        provider.changeAttributeValues({feature.id(): values})
    return building_coordinates_layer.commitChanges()
