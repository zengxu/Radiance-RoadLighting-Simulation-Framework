#AUTHOR: Jan Winter, Sandy Buschmann, Robert Franke TU Berlin, FG Lichttechnik,
#	j.winter@tu-berlin.de, www.li.tu-berlin.de
#LICENSE: free to use at your own risk. Kudos appreciated.
from lxml import etree

class Calculation:

    def __init__( self, root ):
        self.din13201= "" 
        self.veilingLuminance = "" 
        self.veilingLuminanceMethod = "" 
        self.tresholdLuminanceFactor = 0
        self.age = 20
        
        self.loadCalculation( root )
        
    def loadCalculation( self, root ): 
        calcDesc = root.find( 'Scene/Calculation' )
        self.din13201 = calcDesc.get( 'DIN13201' )
        self.veilingLuminance = calcDesc.get( 'VeilingLuminance' )
        self.veilingLuminanceMethod = calcDesc.get( 'VeilingLuminanceMethod' )
        self.headlightOption = calcDesc.get( 'HeadlightOption' )
        self.tresholdLuminanceFactor = calcDesc.get( 'TresholdLuminanceFactor' )
        self.age = calcDesc.get( 'Age' )
        
        print '    calculation parameters loaded ...'