#!/usr/bin/env python
#AUTHOR: Jan Winter, Sandy Buschmann, Robert Franke TU Berlin, FG Lichttechnik,
#	j.winter@tu-berlin.de, www.li.tu-berlin.de
#LICENSE: free to use at your own risk. Kudos appreciated.
#This Python file uses the following encoding: utf-8

# This is the entry point to the script. Command line arguments are parsed here.
# Here the classes 'simulator' and 'configgenerator' are instantiated.

#expected format of the scene description file:
#<RoadScene>
#    <SceneDescription>
#        <Road  NumLanes="a number" LaneWidth="width in meters" SidewalkWidth="width in meters" Surface="plastic, R1-R4, C1, C2, C2W3, C2W4" LightLossFactor="0 clean - 9 dirty"/>
#        <Background Context="City or Grass"/>
#        <Calculation Method="standard" VeilingLuminance="off" TresholdLuminanceFactor="7"/><!--Method can be standard, rp800 or reflectancy, VeilingLuminance can be on and off-->
#    </SceneDescription>
#    <TargetParameters>
#        <!--<ViewPoint Distance="273" Height="1.2" TargetDistanceMode="fixedTargetDistance"/>-->
#        <ViewPoint Distance="distance in meters" Height="height in meters" TargetDistanceMode="fixedViewPoint or fixedTargetDistance" XOffset="observer vertical offset in meters" ViewDirection="auto, first, last"/>
#        <Target Size="edge length in meters" Reflectancy="RBG value" Specularity="0-1" Roughness="0-1" Position="right, left, or centre" OnLane="0-numlanes"/>
#    </TargetParameters>
#    <LDCs>
#        <!-- all LDC's come here, name of files and the light source type-->
#        <LDC Name="TX033306" LightSource="HPS"/>
#        <LDC Name="TX033307" LightSource="HPS"/>
#    </LDCs>    
#    <Poles>
#        <PoleArray PoleHeight="height in meters" PoleSpacing="spacing in meters" IsStaggered="True or false" LDC="name of ldc" Side="Right or left"/>
#        <PoleArray PoleHeight="height in meters" PoleSpacing="spacing in meters" IsStaggered="True or false" LDC="name of ldc" Side="Left or right"/>
#        <!--<PoleSingle PoleHeight="height in meters" LDC="name of ldc" PositionX="position along the road in meters" Side="Left or right"/>-->
#    </Poles>
#    <FocalLength FL="50"></FocalLength>
#</RoadScene>

#The description files itself must be placed in its own directory, and the name of the directory is to be
#passed to the script as a command line argument, with the option '--dir'. Inside this directory, must
#also be a direcotry called LDC, where all the ies files used int he scene must be kept

import os
from optparse import OptionParser
import sys
import shutil
import datetime

import ConfigGenerator as modulConfigGenerator
import Simulator as modulSimulator
import Evaluator as modulEvaluator
import VideoSimulator as modulVideoSimulator
import EnvVarSetter


# Determine the current directory of executaion
# Important step because configfiles and output directories are relative to this path
def extractWorkingDir( ):
    currentDir = os.getcwd( )
    slashindex = currentDir.rfind("/" )
    currentDir = currentDir[ :slashindex ]
    return currentDir
        
def cleanSceneDir( path ):
    print "Will delete all created files in scene directory"
    cwd = extractWorkingDir()
    LMKSetMatDir = cwd + '/scenes/' + path + "/" + path #path + "/LMKSetMat"
    OctsDir = cwd + '/scenes/' + path + "/Octs"
    PicsDir = cwd + '/scenes/' + path + "/Pics"
    RadsDir = cwd + '/scenes/' + path + "/Rads"
    RefOctsDir = cwd + '/scenes/' + path + "/RefOcts"
    RefPicsDir = cwd + '/scenes/' + path + "/RefPics"
    LIDCsDir = cwd + '/scenes/' + path + "/LIDCs"
    EvaluationDir = cwd + '/scenes/' + path + "/Evaluation"
    TempOctsDir = cwd + '/scenes/' + path + "/TempOcts"
    TempRadsDir = cwd + '/scenes/' + path + "/TempRads"
    if( os.path.exists( LMKSetMatDir ) ):
        shutil.rmtree( LMKSetMatDir )
    if( os.path.exists( OctsDir ) ):
        shutil.rmtree( OctsDir )
    if( os.path.exists( PicsDir ) ):
        shutil.rmtree( PicsDir )
    if( os.path.exists( RadsDir ) ):
        shutil.rmtree( RadsDir )
    if( os.path.exists( RefOctsDir ) ):
        shutil.rmtree( RefOctsDir )
    if( os.path.exists( RefPicsDir ) ):
        shutil.rmtree( RefPicsDir )
    if( os.path.exists( EvaluationDir ) ):
        shutil.rmtree( EvaluationDir )
    if( os.path.exists( TempOctsDir ) ):
        shutil.rmtree( TempOctsDir )
    if( os.path.exists( TempRadsDir ) ):
        shutil.rmtree( TempRadsDir )
    if( os.path.exists( LIDCsDir ) ):
        dirList = os.listdir( LIDCsDir )
        for file in dirList:
            if( file.endswith( ".dat" ) or file.endswith( ".rad" ) or file.endswith( ".txt" ) ):
                os.remove( LIDCsDir + "/" + file )
                
usage = "usage: %prog [options]"
version = "%prog 0.1"

oparser = OptionParser( )
oparser.add_option( "--setEnv", action = "store", type = "string", dest = "setEnv", help = "this option tests the radiance installation" )
oparser.add_option( "--dir", action = "store", type = "string", dest = "dir", help = "you have to give a relative path from scenes to your sceneDescription.xml dir" )
oparser.add_option( "--skipRefPics", action = "store_true", dest = "skipRefPics", help = "option to skip refPics" )
oparser.add_option( "--cleanDir", action = "store", type = "string", dest = "cleanDir", help = "option to clean the given dir")
oparser.add_option( "--video", action = "store", type = "string", dest = "video", nargs = 2 , help = "option to make a road video, first parameter is speed in kmh, second is fps eg. --video 30 25" )

( options, args ) = oparser.parse_args()

if( options.setEnv ):
    envtest = EnvVarSetter.EnvVarSetter( options.setEnv )
    if( not envtest.testRadianceInstall( ) ):
            print "Radiance not installed properly. Adding path"
            envtest.addRadianceEnv()
            sys.exit()

starttime = datetime.datetime.now()

if( options.cleanDir ):
    cleanSceneDir( options.cleanDir )    
    
elif( options.dir ):
    cleanSceneDir( options.dir )
    configGen = modulConfigGenerator.ConfigGenerator( extractWorkingDir( ) + '/scenes/' + options.dir )
    print 'All Rads are successful made. Starting with Simulator ...'
    print '---------------------------------------------------------'
    sim = modulSimulator.Simulator( extractWorkingDir( ) + '/scenes/' + options.dir, options.skipRefPics )
    print 'All Simualtions are successful made. Starting with Evaluator ...'
    print '----------------------------------------------------------------'
    ev = modulEvaluator.Evaluator( extractWorkingDir( ) + '/scenes/' + options.dir )
    print 'All Evaluations are successful made ...'
    print '----------------------------------------------------------------'
    if ( options.video ):
        vid = modulVideoSimulator.VideoSimulator( extractWorkingDir( ) + '/scenes/' + options.dir,  options.video )
        print 'Video pics are successful made ...'
        print '----------------------------------------------------------------'

else:
    oparser.print_usage( )

endtime = datetime.datetime.now()
print "Total time elapsed: " + str( endtime - starttime )
