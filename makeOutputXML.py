# TimeLogger: A Light-Weight Implementation of a Time-Tracker/Recorder for Individuals' Personal Use
# Copyright (C) 2021  David Bayani
# 
# This file is part of TimeLogger.
# 
# TimeLogger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# 
# Contact Information:
# 
# Use the "discussion" or "issues" tab on the GitHub repo housing the original
# public copy of this work, https://github.com/DBay-ani/TimeLogger
#


import xml.etree.ElementTree as ET;
from contracts import *;

import sys;


def buildStartUpMenu(fileNameToSaveTo):
    requires(isinstance(fileNameToSaveTo, str));
    requires(len(fileNameToSaveTo) > 0);
    # TODO: check that fileNameToWriteTo is appropraite in 
    #     more ways than just the above line...

    # Below now only checks that the template is in a readable XML format.
    tree =  ET.ElementTree(file="templateForLogEntries.xml"); 
    fh = open("templateForLogEntries.xml", "r");
    fileContent = fh.read();
    fh.close();
    fh = open(fileNameToSaveTo, "w");
    fh.write(fileContent);
    fh.flush();
    fh.close();

    return;



from subprocess import Popen, PIPE ;

def displayDocumentAndWaitForItToBeFilled(fileNameToSaveTo):
    requires(isinstance(fileNameToSaveTo, str));
    requires(len(fileNameToSaveTo) > 0);
    # TODO: check that fileNameToWriteTo is appropraite in 
    #     more ways than just the above two lines...
    thisProc = Popen(["gedit", "--wait", fileNameToSaveTo],stdout=PIPE); 
    thisProc.wait();
    output = thisProc.communicate();
    if(output[-1] not in {0, None}):
        raise Exception("Unknown error occurred while displaying document");
    return;

def displayDocumentAndDoNotWaitForItToBeFilled(fileNameToSaveTo):
    requires(isinstance(fileNameToSaveTo, str));
    requires(len(fileNameToSaveTo) > 0);
    # TODO: check that fileNameToWriteTo is appropraite in 
    #     more ways than just the above two lines...
    thisProc = Popen(["gedit",  fileNameToSaveTo],stdout=PIPE);
    # output = thisProc.communicate();
    # if(output[-1] not in {0, None}):
    #     raise Exception("Unknown error occurred while displaying document");
    return;


