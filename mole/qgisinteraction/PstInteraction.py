from qgis.core import QgsMapLayerRegistry, QgsVectorLayer, QgsVectorFileWriter, QgsCoordinateReferenceSystem
import os
import sys


class PstInteraction(object):

    def __init__(self, plugin, iface, plugin_name='pointsamplingtool'):

        self.point_sampling_tool = plugin
        self.plugin_folder = os.path.dirname(sys.modules[plugin_name].__file__)

        # if the pst is not part of the path, add it to the path, so the modules can be imported
        if self.plugin_folder not in sys.path:
            sys.path.insert(0, self.plugin_folder)

        from doPointSamplingTool import Dialog

        self.pst_dialog = Dialog(iface)
        self.path_to_output_layer = ''

    def set_input_layer(self, layer_name):

        if layer_name is not None and not layer_name.isspace():

            layer_available = False
            layer_dict = QgsMapLayerRegistry.instance().mapLayers()
            for layer_key in layer_dict:
                layer = layer_dict[layer_key]

                if layer.name() == layer_name:
                    layer_available = True

            if layer_available:
                index = 0
                # drop down menu, listing all available layers
                in_layer = self.pst_dialog.inSample
                in_layer.setCurrentIndex(index)

                # while the given layer is not active, iterate over the menu
                while in_layer.currentText() != layer_name:
                    index += 1
                    in_layer.setCurrentIndex(index)

                print in_layer.currentText()

    # def set_output_layer(self, path_to_layer, encoding, crs_name):
    #
    #     if path_to_layer is not None and not path_to_layer.isspace() and not os.path.exists(path_to_layer):
    #
    #         if (encoding is not None and not encoding.isspace()) and \
    #                 (crs_name is not None and QgsCoordinateReferenceSystem().createFromUserInput(crs_name)):
    #
    #             out_path, out_name = os.path.split(path_to_layer)
    #             if out_name.upper().endswith('.SHP'):
    #                 out_name = out_name[:-4]
    #
    #             full_path = os.path.join(out_path, out_name + '.shp')
    #
    #             vlayer = QgsVectorLayer('Point?crs=EPSG:4326', 'pas_out2', 'memory', False)
    #             return_code = QgsVectorFileWriter.writeAsVectorFormat(vlayer, full_path, encoding, QgsCoordinateReferenceSystem(crs_name), 'ogr')
    #
    #             if return_code == QgsVectorFileWriter.NoError:
    #                 QgsMapLayerRegistry.instance().addMapLayer(vlayer)
    #                 self.path_to_output_layer = full_path

    def select_files_for_sampling(self):

        sample_list = self.pst_dialog.inData
        number_of_samples = len(sample_list)

        # ToDo change the range to full select and eliminate duplicates
        #for i in range(0, number_of_samples):
        for i in range(0, number_of_samples):
            print sample_list.item(i).text()
            sample_list.setItemSelected(sample_list.item(i), True)



    def start_sampling(self, path_to_layer, layer_name):

        if path_to_layer and not path_to_layer.isspace() and \
            layer_name and not layer_name.isspace():

            if os.path.exists(path_to_layer):

                if layer_name.upper().endswith('.SHP'):
                    layer_name = layer_name[:-4]

                if os.path.exists(os.path.join(path_to_layer, layer_name + '.shp')):
                    new_name = layer_name
                    suffix = 0

                    while os.path.exists(os.path.join(path_to_layer, new_name + '.shp')):
                        suffix += 1
                        new_name = layer_name + str(suffix)

                    layer_name = new_name

                full_path = os.path.join(path_to_layer,layer_name + '.shp')
                self.pst_dialog.sampling(full_path)

                return full_path

        else:
            return ''
