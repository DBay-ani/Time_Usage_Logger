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

def cleanStrings(thisString):
    return thisString.replace(" ", "").replace("\t", "").replace("\n", "");

typicalSetOfTagsToIgnore = {"orderingInLogData", "machineTimeLogEntryFinishedAndClosed", \
        "machineTimeLogEntryStarted", "commitLogFile", "exitAfterEntry", "timeActivityBegan", \
        "timeActivityFinished", "timezone"};

def printNonEmptyElemsWithIndents(thisElem, tabSoFar, ignoreTypicallyUninterestingTags):
    if((thisElem.tag in typicalSetOfTagsToIgnore) and ignoreTypicallyUninterestingTags):
        return "";
    stringToReturn= tabSoFar + thisElem.tag;
    returnNonEmpty = False;
    if(thisElem.get("uuid") is not None):
        stringToReturn=stringToReturn + "\t" + thisElem.get("uuid") +"\n" + tabSoFar;
    if((thisElem.text is not None) and (cleanStrings(thisElem.text) != "")):
        returnNonEmpty = True;
        stringToReturn = stringToReturn + " :\t"  + thisElem.text.replace("\n", ""); 
    for thisChild in thisElem.getchildren():
        thisResult = printNonEmptyElemsWithIndents(thisChild, tabSoFar + "\t", ignoreTypicallyUninterestingTags);
        if(thisResult != ""):
            returnNonEmpty = True;
            stringToReturn = stringToReturn + "\n" + thisResult + "\n";

    if(returnNonEmpty):
        return stringToReturn;
    return "";

import config;

logSoFar = ET.ElementTree(file=config.pathToLogFile);
logEntries = logSoFar.find("logEntries");
numberOfLogEntries = len(logEntries.getchildren());
import argparse;
parser=argparse.ArgumentParser(description="Print the last k entries of the timeLog in a more human-readable way.");
parser.add_argument("-k", type=int, default=1);
parser.add_argument("--dontIgnore", \
    help="Print all elements that have some text - don't ignore the tags that tend to have uninteresting information.", \
    action="store_true", default=False);
args=parser.parse_args();

for thisLogEntry in logEntries.getchildren():#iterating from oldest to newest
    if(numberOfLogEntries <= args.k):
        print("\n\n====================================================================================\nnumber from end: " + \
            str(numberOfLogEntries)+ "\n\n", flush=True);
        print(str(printNonEmptyElemsWithIndents(thisLogEntry, "", ignoreTypicallyUninterestingTags=(not args.dontIgnore) )));
    numberOfLogEntries = numberOfLogEntries - 1;
    assert(numberOfLogEntries >= 0);








