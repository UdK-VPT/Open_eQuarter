#!/bin/bash

#Name of the temp git
OEQGIT=~/.oeqgit
#Name of the temp work dir
OEQTMP=~/.oeqtmp

#Cleanup temp & git
rm -rf $OEQGIT
rm -rf $OEQTMP

#Create new temp
mkdir $OEQTMP

echo "Open eQuarter Mole: Updatings the QGIS repository"
echo "---------------------------------------------------"
echo
echo "Step 1: Cloning the Open eQuarter git"
git clone https://github.com/UdK-VPT/Open_eQuarter.git $OEQGIT
cd $OEQGIT
echo
echo Current Git Status:
echo `git status`
echo
echo "Step 2: Reading the QGIS plugin metadata"
echo "----------------------------------------"
NAME=`cat mole/metadata.txt | grep name= | sed 's/name=//'`
DESCRIPTION=`cat mole/metadata.txt | grep description= | sed 's/description=//'`
QGISVERSION=`cat mole/metadata.txt | grep qgisMinimumVersion= | sed 's/qgisMinimumVersion=//'`
VERSION=`cat mole/metadata.txt | grep version= | sed 's/version=//'`
AUTHOR=`cat mole/metadata.txt | grep author= | sed 's/author=//'`
EMAIL=`cat mole/metadata.txt | grep email= | sed 's/email=//'`
TAGS=`cat mole/metadata.txt | grep tags= | sed 's/tags=//'`
HOMEPAGE=`cat mole/metadata.txt | grep homepage= | sed 's/homepage=//'`
TRACKER=`cat mole/metadata.txt | grep tracker= | sed 's/tracker=//'`
QGISREPO=`cat mole/metadata.txt | grep repository= | sed 's/repository=//'`
ICON=`cat mole/metadata.txt | grep icon= | sed 's/icon=//'`
EXPERIMENTALFLAG=`cat mole/metadata.txt | grep experimental= | sed 's/experimental=//'`

echo "Name:             $NAME"
echo "Description:      $DESCRIPTION"
echo "Min QGIS Version: $QGISVERSION"
echo "Version:          $VERSION"
echo "Author:           $AUTHOR"
echo "Email:            $EMAIL"
echo "Tags:             $TAGS"
echo "Tracker:          $TRACKER"
echo "QGIS Repository:  $QGISREPO"
echo "Icon:             $ICON"
echo "Experimental:     $EXPERIMENTALFLAG"
echo
echo "Step 3: Creating the QGIS repo xml"
echo "----------------------------------------"
echo
echo "<?xml version = '1.0' encoding = 'UTF-8'?>
<?xml-stylesheet type='text/xsl' href='/plugins.xsl' ?>
<plugins>
  <pyqgis_plugin name='$NAME' version='$VERSION'>
    <description>$DESCRIPTION</description>
    <version>$VERSION</version>
    <qgis_minimum_version>2.4</qgis_minimum_version>
    <homepage>http://udk-vpt.github.io/Open_eQuarter</homepage>
    <file_name>mole.zip</file_name>
    <author_name>$AUTHOR</author_name>
    <download_url>$QGISREPO/mole.zip</download_url>
    <uploaded_by>OeQ Team</uploaded_by>
    <create_date>2015-03-10</create_date>
    <update_date>`date +"%Y-%m-%d"`</update_date>
  </pyqgis_plugin>
</plugins" | tee $OEQTMP/plugins.xml
echo
echo "Step 4: Archiving the latest version"
echo "----------------------------------------"
echo
cd $OEQGIT
zip -r $OEQTMP/mole mole
echo
echo "Step 5: Moving xml and archive to the gh-pages branch"
echo "----------------------------------------"
echo
git checkout gh-pages
 

mkdir qgis_repo
mv "$OEQTMP/mole.zip" $OEQGIT/qgis_repo
mv "$OEQTMP/plugins.xml" $OEQGIT/qgis_repo

git add qgis_repo/mole.zip
git add qgis_repo/plugins.xml
echo
echo "Step 6: Comitting and pushing the changes"
echo "----------------------------------------"
echo

git commit -m "Updated QGIS repo to $VERSION @ `date +"%Y-%m-%d"`"
git push

rm -rf $OEQGIT
rm -rf $OEQTMP

echo "Open eQuarter Mole: QGIS repository update complete"
echo "---------------------------------------------------"

