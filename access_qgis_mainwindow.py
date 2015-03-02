c=iface.mainWindow().children()
for i,w in enumerate(c):
	if type(w) is not QAction and w.objectName():
		print i, w.objectName()
0 _layout
1 qt_rubberband
156 centralwidget
157 menubar
158 statusbar
159 mFileToolBar
160 mLayerToolBar
161 mDigitizeToolBar
162 mAdvancedDigitizeToolBar
163 mMapNavToolBar
164 mAttributesToolBar
165 mPluginToolBar
166 mHelpToolBar
167 mRasterToolBar
168 mLabelToolBar
169 mVectorToolBar
170 mDatabaseToolBar
171 mWebToolBar
180 mPanelMenu
181 mToolbarMenu
186 QgsMeasureBase
187 QgsMeasureBase
188 SimplifyLineDialog
189 Layers
192 LayerOrder
193 Overview
198 QgsPluginManagerBase
199 Undo
200 SnappingOption
201 Browser
202 Browser2
203 GPSInformation
204 MessageLog
206 QgsCredentialDialog
227 tmp
229 PluginBuilder
231 Unandreinstallagivenplugin
233 Analyses
235 DBManager
277 projectionsMenu
281 conversionMenu
287 extractionMenu
290 analysisMenu
297 miscellaneousMenu
304 ProcessingToolbox
311 qt_qmainwindow_extended_splitter
312 qt_qmainwindow_extended_splitter
313 qt_qmainwindow_extended_splitter
314 theTileScaleDock
316 OpenEQuarter
319 qt_qmainwindow_extended_splitter
320 PythonConsole
321 qt_qmainwindow_extended_splitter
323 OpenEQuarter
327 OpenEQuarter
331 OpenEQuarter
335 OpenEQuarter
339 OpenEQuarter
343 OpenEQuarter
347 OpenEQuarter
350 qt_qmainwindow_extended_splitter
352 OpenEQuarter
356 OpenEQuarter
360 OpenEQuarter
364 OpenEQuarter
367 MainProcess_dock
369 OpenEQuarter
373 OpenEQuarter
377 OpenEQuarter
381 OpenEQuarter
385 OpenEQuarter
389 OpenEQuarter
393 OpenEQuarter
397 OpenEQuarter
401 OpenEQuarter
405 OpenEQuarter
408 MainProcess_dock
c[0].children()
[]
c[189].children()
[<PyQt4.QtGui.QLayout object at 0x125e3b510>, <PyQt4.QtGui.QAbstractButton object at 0x125e0ecc8>, <PyQt4.QtGui.QAbstractButton object at 0x125e0ed60>, <PyQt4.QtCore.QObject object at 0x125e0edf8>, <PyQt4.QtGui.QAction object at 0x125e0ee90>, <PyQt4.QtGui.QWidget object at 0x125e0ef28>]
len(c[189].children())
6
c[189].children()[5]
<PyQt4.QtGui.QWidget object at 0x125e0ef28>
c[189].children()[5].objectName()
u''
c[189].children()[5].children()
[<PyQt4.QtGui.QVBoxLayout object at 0x125e3b510>, <PyQt4.QtGui.QToolButton object at 0x125e0ef28>, <PyQt4.QtGui.QToolButton object at 0x125e0ecc8>, <PyQt4.QtGui.QToolButton object at 0x125e0ed60>, <PyQt4.QtGui.QToolButton object at 0x125e0edf8>, <PyQt4.QtGui.QToolButton object at 0x125e20050>, <PyQt4.QtGui.QToolButton object at 0x125e200e8>, <qgis._gui.QgsLayerTreeView object at 0x125e20180>]
c[189].children()[5].children()[5]
<PyQt4.QtGui.QToolButton object at 0x125e20050>
c[189].children()[5].children()[6]
<PyQt4.QtGui.QToolButton object at 0x125e200e8>
c[189].children()[5].children()[7]
<qgis._gui.QgsLayerTreeView object at 0x125e20180>
c[189].children()[5].children()[7].objectName()
u'theLayerTreeView'
c[189].children()[5].children()[7].children()
[<PyQt4.QtGui.QWidget object at 0x125e3b510>, <PyQt4.QtGui.QWidget object at 0x125e0ef28>, <PyQt4.QtGui.QStyledItemDelegate object at 0x125e0ecc8>, <PyQt4.QtGui.QHeaderView object at 0x125e0ed60>, <PyQt4.QtGui.QItemSelectionModel object at 0x125e0edf8>, <PyQt4.QtCore.QObject object at 0x125e0ee90>, <PyQt4.QtGui.QWidget object at 0x125e20180>]
l = c[189].children()[5].children()[7].children()
for li in l:
	print li.objectName()
qt_scrollarea_viewport
qt_scrollarea_vcontainer




qt_scrollarea_hcontainer
for li in l:
	print li.children()
[]
[<PyQt4.QtGui.QScrollBar object at 0x125e3ba68>, <PyQt4.QtGui.QBoxLayout object at 0x125e205a8>]
[]
[<PyQt4.QtGui.QWidget object at 0x125e3ba68>, <PyQt4.QtGui.QWidget object at 0x125e205a8>, <PyQt4.QtGui.QWidget object at 0x125e20050>, <PyQt4.QtGui.QItemSelectionModel object at 0x125e200e8>]
[]
[]
[<PyQt4.QtGui.QScrollBar object at 0x125e3ba68>, <PyQt4.QtGui.QBoxLayout object at 0x125e205a8>]