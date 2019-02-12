# -*- coding: utf-8 -*-

def write_project_definition_report(self,template):
    from mole.qgisinteraction import legend
    from mole.project import config
    from mole import oeq_global
    database=legend.nodeByName(config.data_layer_name)
    if not database:
        return None
    database = database[0]
    tpl_path=os.path.join(oeq_global.OeQ_project_path(),config.report_template_dir,config.building_report_tpl)
    th = open(tpl_path, 'r')
    template = th.read()
    th.close()
    building_list = database.layer().selectedFeatures()
    if not building_list:
        building_list = database.layer().getFeatures()
    output = []
    for building in building_list:
        tpl =template
        for field in [i.name() for i in database.layer().fields()]:
            tpl.replace('!!!'+field+'!!!',str(building[field]))
        output.append()
    return output

def write_building_reports(bld_ids=[],reporttemplate=None):
    from mole.qgisinteraction import legend
    from mole.project import config
    from mole import oeq_global
    import os
    database=legend.nodeByName(config.data_layer_name)
    if not database:
        return None
    database = database[0]
    if not reporttemplate:
        reporttemplate=config.building_report_tpl
    tpl_path=os.path.join(oeq_global.OeQ_project_path(),config.report_template_dir,reporttemplate)
    rep_path=os.path.join(oeq_global.OeQ_project_path(),config.building_report_dir)
    th = open(tpl_path, 'r')
    template = th.read()
    th.close()
    building_list = database.layer().selectedFeatures()
    if not building_list:
        building_list = database.layer().getFeatures()
    output = []
    for building in building_list:
        if (not bld_ids) | (building[config.building_id_key] in bld_ids):
            tpl =template
            for field in [i.name() for i in database.layer().fields()]:
                tpl.replace('!!!'+field+'!!!',str(building[field]))
            rh=open(os.path.join(rep_path,"BLD_"+building[config.building_id_key]+'.html'),'w')
            rh.write(tpl)
            rh.close()
            output.append(tpl)
    return output

def write_project_definitions_report():
    from qgis.core import QgsCoordinateReferenceSystem,QgsCoordinateTransform
    from mole.qgisinteraction import legend
    from mole.project import config
    from mole import oeq_global
    import os
    import webbrowser
    from cgi import escape
    from urllib.request import pathname2url
    tpl_path=os.path.join(oeq_global.OeQ_plugin_path(),config.report_template_dir,config.project_definitions_tpl)
    rep_path=os.path.join(oeq_global.OeQ_project_path(),config.report_dir,config.project_definitions_tpl)
    th = open(tpl_path, 'r')
    template = str(th.read())
    th.close()
    extend_node=legend.nodeByName(config.investigation_shape_layer_name)
    if not extend_node:
        return None
    extent=extend_node[0].layer().extent()
    #crsSrc=QgsCoordinateReferenceSystem(int(config.default_extent_crs.split(':')[-1]), QgsCoordinateReferenceSystem.EpsgCrsId)
        #crsDest=QgsCoordinateReferenceSystem(int(self.source_crs.split(':')[-1]), QgsCoordinateReferenceSystem.EpsgCrsId)
        ##transform extent
        #coord_transformer = QgsCoordinateTransform(crsSrc, crsDest)
        #extent = coord_transformer.transform(extent)
    p_info = oeq_global.OeQ_project_info
    project_info = {'PRJ_NAME':p_info['project_name'],
             'PRJ_DESCR':p_info['description'],
             'IAC_CTY':p_info['location_city'],
             'IAC_COD':p_info['location_postal'],
             'IAC_LON1':p_info['location_lon'],
             'IAC_LAT1':p_info['location_lat'],
             'IA_LONMIN':str(extent.xMinimum()),
             'IA_LONMAX':str(extent.xMaximum()),
             'IA_LATMIN':str(extent.yMinimum()),
             'IA_LATMAX':str(extent.xMaximum()),
             'IA_CRS':p_info['location_crs'],
             'PRJ_YOC':p_info['average_construction_year'],
             'PRJ_PDENS':p_info['population_density'],
             'PRJ_HDD':p_info['heating_degree_days']}
    for field in list(project_info.keys()):
            print(field)
            print(escape(project_info[field]))
            template=template.replace('!!!'+field+'!!!',escape(project_info[field]))
    if not os.path.exists(os.path.join(oeq_global.OeQ_project_path(),config.report_dir)):
        os.makedirs(os.path.join(oeq_global.OeQ_project_path(),config.report_dir))
    print(rep_path)
    rh=open(rep_path,'w')
    print(rep_path)
    template=template.encode('utf8', 'replace')
    rh.write('"""'+template+'"""')
    rh.close()
    #print escape(rep_path)
    print(rep_path)
    webbrowser.open('file://' + os.path.realpath(rep_path),new=2)
    return template


