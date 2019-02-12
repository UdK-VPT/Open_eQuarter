#!/bin/bash
cd "$( dirname "$0" )"
#path to mole module here (relative)
MOLE="../mole"
#path to mole module in qgis python plugins (relative)
MOLEQGISPATH=~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/
MOLEQGIS=~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/mole
echo "Open eQuarter Mole: Copy the MOLE plugin from this gitclone into QGIS"
echo "---------------------------------------------------------------------"
echo
echo "Step 1: Removing the old plugin $MOLEQGIS"
#Cleanup temp & git
rm -rf "$MOLEQGIS"
echo "Step 2: Creating the plugin directory $MOLEQGIS"
mkdir "$MOLEQGIS"
echo "Step 3: Copying the plugin from $MOLE to $MOLEQGIS"
cp -R "$MOLE" "$MOLEQGISPATH"
echo "Done!"
