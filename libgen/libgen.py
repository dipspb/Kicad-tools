#!/usr/bin/python
############################################################################
############################################################################
##
"""
##  libgen - Library Generator Program for Kicad Schematics V0.0
## 
##  Designed by
##         A.D.H.A.R Labs Research,Bharat(India)
##            Abhijit Bose( info@adharlabs.in )
##                http://adharlabs.in
##
## License:
## Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported
## CC BY-NC-SA 3.0 http://creativecommons.org/licenses/by-nc-sa/3.0/
## http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode
"""
## Credits:
## Thanks to bifferos (bifferos@yahoo.co.uk) For his DIP Generator
## Link = http://tech.groups.yahoo.com/group/kicad-users/
## files/DIP%20generation%20helper/
##
## Version History:
## version 0.0 - Initial Release (2012-02-08)
##                 > Support for DIP Package type Symbol
##                 > Support for SIP Package type Symbol
##                 > Support for CONN Package type Symbol
##                 > Support for QUAD Package type Symbol
##
############################################################################
############################################################################
#IMPORTS>
import xml.dom.minidom,sys, os
from datetime import datetime
############################################################################
#EXPORT>
__all__=['Help_xml2lib','xml2lib']
__author__ = "Abhijit Bose(info@adharlabs.in)"
__author_email__="info@adharlabs.in"
__version__ = "0.0"
############################################################################
#DEBUG> Print Additional Debug Messages
#  if needed make _debug_message = 1
_debug_message = 0
############################################################################
#FORMAT>Lib
template = """EESchema-LIBRARY Version 2.3  Date: 6/1/2012-05:30AM IST
#encoding utf-8
#
# %(compname)s
#
DEF %(compname)s %(refname)s 0 40 Y Y 1 F N
F0 "%(refname)s" 0 %(refname_y)s 50 H V C C N N
F1 "%(compname)s" 0 %(compname_y)s 50 H V C C N N
DRAW
%(box)s
%(pins)s
ENDDRAW
ENDDEF
#
# End Library
"""
############################################################################
#FORMAT FUNCTIONS>
def PinDescriptions(comp):
  "Read in the pin descriptions as a list"
  el = xmlcomp.getElementsByTagName("component")[0]
  xbits=[i.data for i in el.childNodes if i.nodeType==el.TEXT_NODE]
  
  # Split into lines
  bits = "".join(xbits).split("\n")
  #Remove white space
  bits = [ i.strip() for i in bits ]
  #Remove empty strings
  bits = [ i for i in bits if i!="" ]
  #Get the Pin names & Modes
  bits = [ i.split(',') for i in bits]
  return bits

def PinGen(numb):
  "Generate Pin Numbers if No pin Description is available using PIN"
  bits = []
  for i in range(1,numb+1):
    bits.append([str(i),'P'])#All are passive
  #print bits
  return bits

def MetaData(comp):
  "Extract the component description parameters (common to all pins)"
  el = comp.getElementsByTagName("component")[0]
  d = {}
  for name, value in el.attributes.items() :
    d[name] = value
  return d
############################################################################
#Component Forming FUNCTIONS>
def GetTemplate_DIP(pins, d) :
  #{ Begin of DIP
    """ Generator Function for the DIP Package"""
    print ">Working for DIP or PDIP Package"
    # Count the Number of pins
    pl = len(pins)
    if (pl%2)!=0:
      print "Package has odd number of pins"
      sys.exit(-1)
    # Split the Pin array in Two parts
    left_p = pins[:pl/2]
    right_p = pins[pl/2:]
    # Height dependant on Number of Pins Spaced at 100mil
    height = (len(left_p)+1)*100
    # Width for the body according to Pin String
    width = ((max([len(i[0]) for i in pins] )*50)*2/100)*100+100
    # Calculate the Co-ordinates
    left = -width/2
    top = height/2
    right = width/2
    bottom = -height/2
    # Locate the Reference Designators accordinly
    d["refname_y"] = str(0)
    d["compname_y"] = str(-100)    
    # Make the Box Parameter
    d["box"] = "S %d %d %d %d 0 1 0 N"%(left,top,right,bottom)
    # Pin Length
    plen = 200
    # Pin Counter
    count = 1
    # Result Array
    txt = []
    # Construct the Pins Array For Left Side
    for pin in left_p :
      ypos = top - (count*100)
      xpos = left - plen
      txt.append(\
        "X %s %d %d %d %d R 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
        )
      count += 1
    # Construct the Pins Array for Right Side
    for pin in right_p :
      ypos = bottom + ((count-len(left_p))*100)
      xpos = right + plen
      txt.append(\
        "X %s %d %d %d %d L 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
        )
      count += 1
    # Consolidate the Pins Array 
    d["pins"] = "\n".join(txt)    
    return d
  #} End of DIP
  
def GetTemplate_SIP(pins, d) :
  #{ Begin SIP
    """ Generator Function for the SIP Package"""
    print ">Working for SIP Package"
    # Count the Number of pins
    pl = len(pins)
    # Height dependant on Number of Pins Spaced at 100mil
    height = (pl+1)*100
    # Width for the body according to Pin String
    width = max([len(i[0]) for i in pins] )*50+100    
    # Calculate the Co-ordinates
    left = -width/2
    top = height/2
    right = width/2
    bottom = -height/2
    # Locate the Reference Designators accordinly
    d["refname_y"] = str(top+50)
    d["compname_y"] = str(bottom-50)
    # Make the Box Parameter
    d["box"] = "S %d %d %d %d 0 1 0 N"%(left,top,right,bottom)
    # Pin Length for SIP
    plen = 200
    # Pin Counter
    count = 1
    # Result Array
    txt = []
    # Construct the Pins Array
    for pin in pins:
      ypos = top - (count*100)
      xpos = right + plen
      txt.append(\
        "X %s %d %d %d %d L 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
        )
      count += 1
    # Consolidate the Pins Array  
    d["pins"] = "\n".join(txt)
    return d
  #} End of SIP
  
def GetTemplate_CONN(pins, d) :
  #{ Begin CONN
    """ Generator Function for the CONN Package"""
    print ">Working for CONN Package"
    # Count the Number of pins
    pl = len(pins)
    if (pl%2)!=0:
      print "Package has odd number of pins"
      sys.exit(-1)
    # Height dependant on Number of Pins Spaced at 100mil
    height = (pl/2+1)*100
    # Width for the body according to Pin String
    width = ((max([len(i[0]) for i in pins] )*50)*2/100)*100+100
    # Calculate the Co-ordinates
    left = -width/2
    top = height/2
    right = width/2
    bottom = -height/2
    # Locate the Reference Designators accordinly
    d["refname_y"] = str(top+50)
    d["compname_y"] = str(bottom-50)
    # Make the Box Parameter
    d["box"] = "S %d %d %d %d 0 1 0 N"%(left,top,right,bottom)
    # Pin Length for SIP
    plen = 200
    # Pin Counter
    count = 1
    # Pin Location Counter
    align = 1
    # Result Array
    txt = []
    # Construct the Pins Array
    for pin in pins:
      if(count%2)!=0:#ODD Pin Left
        ypos = top - (align*100)
        xpos = left - plen
        txt.append(\
          "X %s %d %d %d %d R 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
          )
      elif(count%2)==0:#EVEN Pin Right
        ypos = top - (align*100)
        xpos = right + plen
        txt.append(\
          "X %s %d %d %d %d L 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
          )
        align += 1 #After every even pin the line changes
      count += 1
    # Consolidate the Pins Array  
    d["pins"] = "\n".join(txt)
    return d
  #} End of CONN
  
def GetTemplate_QUAD(pins, d) :
  #{ Begin QUAD
    """ Generator Function for the QUAD Package"""
    print ">Working for QUAD Package"
    # Count the Number of pins
    pl = len(pins)
    if (pl%4)!=0:
      print "Package does not have pins in multiples of 4"
      sys.exit(-1)    
    # Width for the body according to Pin String
    wdiff = max([len(i[0]) for i in pins] )*50
    width = (wdiff*2)+100*pl/4
    # Height dependant on Number of Pins Spaced at 100mil
    height = width
    # Calculate the Co-ordinates
    left = -width/2
    top = height/2
    right = width/2
    bottom = -height/2
    # Locate the Reference Designators accordinly
    d["refname_y"] = str(0)
    d["compname_y"] = str(-100)
    # Segment the Pins into 4 parts
    left_p = pins[:pl/4]
    bottom_p = pins[pl/4:pl/2]
    right_p = pins[pl/2:3*pl/4]
    top_p =pins[3*pl/4:]
    # Make the Box Parameter
    d["box"] = "S %d %d %d %d 0 1 0 N"%(left,top,right,bottom)
    # Pin Length for SIP
    plen = 200
    # Pin Counter
    count = 1   
    # Result Array
    txt = []
    # For Left Pins
    align = 1 #Pin Location Counter
    for pin in left_p:
      ypos = top - (align*100) - wdiff + 50
      xpos = left - plen
      txt.append(\
          "X %s %d %d %d %d R 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
          )
      align +=1
      count +=1
    # For Bottom Pins
    align = 1 #Pin Location Counter
    for pin in bottom_p:
      ypos = bottom - plen
      xpos = left + (align*100) + wdiff - 50
      txt.append(\
          "X %s %d %d %d %d U 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
          )
      align +=1
      count +=1
    # For Right Pins
    align = 1 #Pin Location Counter
    for pin in right_p:
      ypos = bottom + (align*100) + wdiff - 50
      xpos = right + plen 
      txt.append(\
          "X %s %d %d %d %d L 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
          )
      align +=1
      count +=1
    # For Top Pins
    align = 1 #Pin Location Counter
    for pin in top_p:
      ypos = top + plen
      xpos = right - (align*100) - wdiff + 50
      txt.append(\
          "X %s %d %d %d %d D 50 50 1 1 %s"%\
        (pin[0],count,xpos,ypos,plen,pin[1])\
          )
      align +=1
      count +=1
    # Consolidate the Pins Array  
    d["pins"] = "\n".join(txt)
    return d
  #} End of QUAD
  
def GetTemplateDict(pins, d) :
  """Get the Kicad format lib file"""
  if not (d["package"] in ["DIP","PDIP","SIP","CONN","QUAD"]):
    print "Unsupported package"
    sys.exit(-1)
  if (d["package"] == "DIP") or (d["package"] == "PDIP"):
    d = GetTemplate_DIP(pins, d)
  elif (d["package"] == "SIP"):
    d = GetTemplate_SIP(pins, d)
  elif (d["package"] == "CONN"):
    d = GetTemplate_CONN(pins, d)
  elif (d["package"] == "QUAD"):
    d = GetTemplate_QUAD(pins, d)
  return d

############################################################################
#OTHER FUNCTIONS>
def Help_xml2lib():
  print """Usage: %s <spec file> <lib file>
  
Where <spec file> is a file containing the PIN descriptions
and <lib file> is the name of the generated component description.

<spec file> is an XML format file, containing the pin descriptions and
optional meta data.  It contains a single XML element 'component'.

example:
<component refname="Ref_des" compname="Comp_Name" package="PDIP">
PIN1DESCRIPTION,ETYPE
PIN2DESCRIPTION,ETYPE
...
</component>
Here Ref_des is your component Reference Designator and Comp_name
is an Valid component Name. PDIP is the package of the component.
ETYPE is the electrical type of the Pin:
I: INPUT 
O: OUTPUT
B: Bi-Directional
T: TRISTATE
P: PASSIVE
U: UNSPECIFIED
W: POWER INPUT
w: POWER OUTPUT
C: OPEN COLLECTOR
E: OPEN EMITTER
N: NOT CONNECTED

Additionally if no pin names are needed then PIN_N="<Number of Pins>"
needs to be used. The created pins would have PASSIVE electrical Type.
Example.
<component refname="J" compname="MOLEX_8" package="SIL" PIN_N="8">
</component>

Schematics Symbol Packages:-

DIP -
     1 _____________  N
  -----| 1       N |-----
       |           |
     2 |           | N-1
  -----| 2     N-1 |-----
   .....................
   .....................
N/2 -1 |           | N/2
  -----|N/2-1  N/2 |-----
       |___________|

SIP -
  ____________  1
  |        1 |------
  |          |  2
  |        2 |------
  |          |
...................
...................
  |          |  N
  |        N |-------
  |__________|

CONN -
     1 _____________  2
  -----| 1       2 |-----
       |           |
     3 |           |  4
  -----| 3       4 |-----
   .....................
   .....................
   N-1 |           |  N
  -----| N-1     N |-----
       |___________|

QUAD -
                    ..  
            |   |   ..   |   |
           N|   |   ..   |   |
            |   |   ..   |   |3N/4+1
            |   |   ..   |   |
        |-----------..----------|
     1  |   N       ..          |
--------| 1         ..          |--------
     2  |           ..          |
--------| 2         ..          |--------
...........................................
...........................................
    N/4 |           ..          | 2N/4+1
--------|N/4        ..   2N/4+1 |--------
        |-----------------------|
            |   |   ..   |   |
            |   |   ..   |   |
            |   |   ..   |   |
            |   |   ..   |   |
        
"""%os.path.split(sys.argv[0])[1]
  sys.exit(-1)
############################################################################
#Processing FUNCTION>
def xml2lib(srcxmlfile,destlibfile):
  #{ Begin Lib Gen
  """Fuction to convert the Xml Format to Kicad lib file format"""
  # Read in the XML file
  xmlcomp = xml.dom.minidom.parse( srcxmlfile )
  # Read Meta Data
  meta = MetaData(xmlcomp)  
  if _debug_message==1:
      print meta
  #Check for Existance of a Generic Parameter
  try:
    meta["PIN_N"]
  except KeyError:
    meta["PIN_N"] = None
  # Populate the Pins
  if meta["PIN_N"] != None: #if not Pins are Described
    pins = PinGen(int(meta["PIN_N"]))    
  else:
    pins = PinDescriptions(xmlcomp)
  if _debug_message==1:
      print pins
  # Create the Translation Dictionary
  d = GetTemplateDict(pins, meta)
  if _debug_message==1:
    print d
  # Apply the Formatting on Template
  out = template%d
  print out
  # Write The File
  file(destlibfile,"w").write(out)
  #} End of Lib Gen
  
############################################################################
#MAIN FUNCTION>
if __name__ == "__main__" :
  if not sys.argv[2:] :
    Help_xml2lib()
  if not os.path.isfile(sys.argv[1]) :
    Help_xml2lib()
  # Print the Introduction
  print __doc__
  print "Source File> "+sys.argv[1]
  print "Destination File> "+sys.argv[2]
  print
  # Process the files
  xml2lib(sys.argv[1],sys.argv[2])
  print "File %s written"%sys.argv[2]
