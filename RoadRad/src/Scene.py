# This Python file uses the following encoding: utf-8

class Scene:
    #Scene Description Variables
    Length = 0
    NumLanes = 0
    LaneWidth = 0
    SidewalkWidth = 0
    Surfacetype = ""
    
    Background = ""
        
    #Target Parameters Variables
    #Viewpoint variables
    ViewpointDistance = 0
    ViewpointHeight = 0
    ViewpointDistanceMode = 0
    #Target Variables
    TargetSize = 0
    TargetReflectency = 0
    TargetPosition = 0
    TargetOrientation = 0
        
    #LDC Variables
    LDCName = ""
    LDCLightSource = ""
    LCDTag = ""
        
    #An Array of pole objects to contain all types of poles that might exsist in a scene
    Poles = [ ]
        
        