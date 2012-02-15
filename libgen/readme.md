libgen - Library Generator Program for Kicad Schematics V0.0
===========================================================

This *Python* based tool designed to create library symbols for Kicad schematics.
The output from the generation is a `.lib file` that can be imported into the `user library`.
The input for this generation uses `XML file` to get the pins.
This tool in multiple ways emulates the 
[Quick KICAD Library Component Builder](http://kicad.rohrbacher.net/quicklib.php) 
online tool for generating the symbols.
However seting up the attibutes for each pin might be difficult.
The XML file can be generated using a CSV from the spread sheet.
The examples in the subsequemt sections show this.

Usage
-----
`python libgen <.xml file> <.lib file>`
  
Where `<.xml file>` is a file containing the *PIN descriptions*
and `<.lib file>` is the name of the generated component description.

`<.xml file>` is an XML format file, containing the *pin descriptions* and
optional meta data.  It contains a single XML element `<component>`.

Example:

    <component refname="Ref_des" compname="Comp_Name" package="PDIP">
    PIN1DESCRIPTION,ETYPE
    PIN2DESCRIPTION,ETYPE
    ...
    </component>

Here `Ref_des` is your component *Reference Designator* and `Comp_name`
is an *Valid component Name*. `PDIP` is the *package* of the component.

**ETYPE** is the electrical type of the Pin:

**I:** INPUT 

**O:** OUTPUT

**B:** Bi-Directional

**T:** TRISTATE

**P:** PASSIVE

**U:** UNSPECIFIED

**W:** POWER INPUT

**w:** POWER OUTPUT

**C:** OPEN COLLECTOR

**E:** OPEN EMITTER

**N:** NOT CONNECTED

Additionally **if no pin names are needed** then `PIN_N="<Number of Pins>"`
needs to be used. The created pins would have `PASSIVE` **EType**.

Example:

    <component refname="J" compname="MOLEX_8" package="SIL" PIN_N="8">
    </component>

Schematics Symbol Packages Currently supported
-----------------------------------------------

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


Designed By
-----------
**A.D.H.A.R Labs Research,Bharat(India)**

Abhijit Bose [info@adharlabs.in](mailto:info@adharlabs.in)

[http://adharlabs.in](http://adharlabs.in)

Credits(Attribution)
--------------------
Thanks to bifferos (bifferos@yahoo.co.uk) For his DIP Generator
[Link](http://tech.groups.yahoo.com/group/kicad-users/files/DIP%20generation%20helper/)

Version History
---------------
version 0.0 - Initial Release (2012-02-08)
 *  Support for DIP Package type Symbol

 *  Support for SIP Package type Symbol

 *  Support for CONN Package type Symbol

 *  Support for QUAD Package type Symbol

Limitation in Present Design
-----------------------------
The generator works to give only one component at a time however there are 
plans to expand it for multiple components using a single XML file.


License
--------
Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported

[CC BY-NC-SA 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/)

[Full Text](http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode)


