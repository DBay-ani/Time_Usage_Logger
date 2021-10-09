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

def extractLogFileAndAncestorInfo(thisLogEntryElem):
    # TODO: requires and ensures

    elementOrderingInLogData = thisLogEntry.findall("orderingInLogData");
    assert(isinstance(elementOrderingInLogData, list));
    assert(len(elementOrderingInLogData) == 1);
    elementOrderingInLogData = elementOrderingInLogData[0];

    elementLogFileUUID = elementOrderingInLogData.findall("uuidOfLog");
    assert(isinstance(elementLogFileUUID, list));
    assert(len(elementLogFileUUID) == 1);
    elementLogFileUUID = elementLogFileUUID[0];
    thisLogFileUUID = cleanStrings(elementLogFileUUID.text);

    elementLastLogEntryUUIDs = elementOrderingInLogData.findall("lastLogEntryUUIDs");
    assert(isinstance(elementLastLogEntryUUIDs, list));
    assert(len(elementLastLogEntryUUIDs) == 1);
    elementLastLogEntryUUIDs = elementLastLogEntryUUIDs[0];
    elementsUuidsOfAncestorLogUUIDs = elementLastLogEntryUUIDs.findall("i");
    assert(isinstance(elementsUuidsOfAncestorLogUUIDs, list));
    uuidsOfAncestorLogUUIDs = [cleanStrings(elem.text) for elem in elementsUuidsOfAncestorLogUUIDs];

    return {"thisLogFileUUID" : thisLogFileUUID, "uuidsOfAncestorLogUUIDs" : uuidsOfAncestorLogUUIDs};



from timeElements import convertTimeElementToSeconds; 

def extractTimingInfoForLog(thisLogEntryElem):
    tagsOfTimeElementsToExtract = {\
        "srtsw", "timeActivityBegan", "timeActivityFinished", "srtfw", \
        "machineTimeLogEntryStarted", "machineTimeLogEntryFinishedAndClosed"
        };
    timingElements = [{"tag": x, "result" : thisLogEntryElem.findall(x)} for \
        x in tagsOfTimeElementsToExtract];
    assert(all([len(y["result"]) == 1 for y in timingElements]));
    dictToReturn = {\
        x["tag"] : convertTimeElementToSeconds(x["result"][0]) for x in timingElements};
    return dictToReturn;

def getUUIDOfHeadLogElement(thisLogFileRoot):
    # TODO: requires and ensures
    # TODO: this function needs to be made more robust
    elementForBookkeeping = thisLogFileRoot.findall("bookKeepingData")[0];
    elementsForLastLogEntryUUIDs = elementForBookkeeping.findall("lastLogEntryUUIDs")[0];
    headsOfLogFile = elementsForLastLogEntryUUIDs.findall("i");
    if(len(headsOfLogFile) > 1):
        raise Exception("More than one head was detected in the log file. We do not currently support this.");
    if(len(headsOfLogFile) == 0):
        raise Exception("Log file missing head log UUID - head is either non-existant or not properly recorded.");
    return cleanStrings(headsOfLogFile[0].text);

def getProperTimes(thisLogEntryTimeInfo, parentOfThisLogEntryTimeInfo):
    # takes in elements with content returned by extractTimingInfoForLog
    # returns {"combinedEvidence_startTimeOfEvent", "combinedEvidence_endTimeOfEvent_startLogWritting", "combinedEvidence_endTimeLogWritting"}
    print("        " + str(thisLogEntryTimeInfo["srtsw"]), flush=True);
    if(parentOfThisLogEntryTimeInfo != None):
        print("        " + str(parentOfThisLogEntryTimeInfo["srtsw"]), flush=True);
    return ;# results;


import config;

logSoFar = ET.ElementTree(file=config.pathToLogFile);
logEntries = logSoFar.find("logEntries");
numberOfLogEntries = len(logEntries.getchildren());
import argparse;
parser=argparse.ArgumentParser(description="Print the last d days of entries in a human-readable way.");
parser.add_argument("-d", type=int, default=1);
# parser.add_argument("--dontIgnore", \
#    help="Print all elements that have some text - don't ignore the tags that tend to have uninteresting information.", \
#    action="store_true", default=False);
args=parser.parse_args();

uuidOfLogFile = None;
uuidOfLastLog = None;


dictMappingUUIDToLogEntryElement = dict();
dictMappingUUIDToAncestorsAndLogFile = dict()
dictMappingUUIDToTimingInfo = dict();
dictMappingUUIDToProperTime = dict();


setOfLogFileUUIDsSeen = set();
setOfLogFileUUIDsSeen.add(logSoFar.getroot().get("uuid"));

import sys;

for thisLogEntry in logEntries.getchildren():#iterating from oldest to newest

    #V~V~V~VV~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
    # checking that log reported is the proper one....
    #====================================================================
    thisLogUUID = cleanStrings(thisLogEntry.get("uuid"));

    # TODO: make a reasonable try-except loop to handle errors...


    print(thisLogUUID, flush=True);

    if(thisLogUUID in dictMappingUUIDToLogEntryElement):
        raise Exception("LogEntry UUID repeated when traversing the file.");

    dictMappingUUIDToLogEntryElement[thisLogUUID] = thisLogEntry;

    tempResult = extractLogFileAndAncestorInfo(thisLogEntry);
    if(len(tempResult["uuidsOfAncestorLogUUIDs"]) > 1):
        raise Exception("We currently do not support non-linear chains of logs. This code will need to be implemented later. Exitting.");
        
    if( tempResult["thisLogFileUUID"] not in setOfLogFileUUIDsSeen):
         print("""
         \n\nNote: multiple log-files were used to form the log entries present. In this case, we encountered
         the log-uuid """ + str(tempResult["thisLogFileUUID"]) + """ when, up to this point in scanning the log-file, 
         we were only aware of the following log files being encorporated in:\n""" + str(setOfLogFileUUIDsSeen) + """\n\n
         If you are fine with this, press enter to continue. Otherwise, press ctrl+C .""", flush=True);
         sys.readline();

    setOfLogFileUUIDsSeen.add(tempResult["thisLogFileUUID"]);
    dictMappingUUIDToAncestorsAndLogFile[thisLogUUID] = tempResult;

    try:
        dictMappingUUIDToTimingInfo[thisLogUUID] = extractTimingInfoForLog(thisLogEntry);
        # TODO: correct the below code - it makes the assumption that all ancestors have appeared earlier in the scan <----------------------------
        ancestorUUIDs = dictMappingUUIDToAncestorsAndLogFile[thisLogUUID]["uuidsOfAncestorLogUUIDs"];
        assert(isinstance(ancestorUUIDs, list));
        if(len(ancestorUUIDs) > 1):
            raise Exception("We do not currently support going through the times on logs that have more than one parent");
        dictMappingUUIDToProperTime[thisLogUUID] = getProperTimes(dictMappingUUIDToTimingInfo[thisLogUUID], \
                                                                 ( dictMappingUUIDToTimingInfo[ancestorUUIDs[0]] if (len(ancestorUUIDs) ==1 ) else None)  );
    except:
        print("WARNING: error computing time-values for log with UUID " + str(thisLogUUID), flush=True);
        dictMappingUUIDToTimingInfo[thisLogUUID] = None;
    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


assert(set(dictMappingUUIDToLogEntryElement.keys()) == set(dictMappingUUIDToAncestorsAndLogFile.keys()));
assert(set(dictMappingUUIDToLogEntryElement.keys()) == set(dictMappingUUIDToTimingInfo.keys()));


dictMappingLogsToTimesWithCombinedEvidence = dict();

uuidOfHeadLogEntry = getUUIDOfHeadLogElement(logSoFar.getroot());
if(uuidOfHeadLogEntry not in set(dictMappingUUIDToLogEntryElement.keys()) ):
    raise Exception("Head-log-entry does not appear to be among the elements in the log file.");




