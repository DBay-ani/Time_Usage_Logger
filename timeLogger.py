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

import sys;
# Below is necessary because Python 3 handles Unicode more cleanly than 
# Python 2 with the Unicode type that had to be appended to places. Below, 
# we just use str, the python string object, to handle unicode, which would
# not have yeilded the desired results in python 2.
if(sys.version_info[0] != 3):
    raise Exception("This code requires python 3 to run.");

from contracts import *;

from readOutputXMLAndAddToDatabase import readStartupMenu;
from makeOutputXML import \
    displayDocumentAndWaitForItToBeFilled, displayDocumentAndDoNotWaitForItToBeFilled, \
    buildStartUpMenu ;


from subprocess import Popen, PIPE ;

from subprocess import Popen, PIPE ;
import re;

import sys;

import traceback; # to be able to get and record error messages (exceptions, etc.)


from getGitCommitHash import gitCommitHashAtStartOfRun;

import xml.etree.ElementTree as ET;

import config;

import uuid; 

from timeElements import formTimeElementForCurrentTime;

from autocommitLog import autocommitBackupData; 

def setUpLogIfNecessary(thisLogTree):
    rootOfTree = thisLogTree.getroot();
    if(rootOfTree.get("uuid") is None):
        rootOfTree.set("uuid", str(uuid.uuid4()));
    return;

def setMetaDataOfLogEntryAndLogFile(rootOfTree, thisLogEntryElement):

    #V~V~V~V~V~V~V~V~V~VV~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
    # Setting metadata in log-entry
    #------------------------------------------------------------------------
    uuidOfLog = rootOfTree.get("uuid");
    assert(uuidOfLog is not None);
    thisOrderInLogDataElement = ET.fromstring("""
        <orderingInLogData>
            <uuidOfLog></uuidOfLog>
        </orderingInLogData>
        """);
    thisOrderInLogDataElement.find("uuidOfLog").text = uuidOfLog;
    thisOrderInLogDataElement.append(rootOfTree.find("bookKeepingData").find("lastLogEntryUUIDs"));
    thisLogEntryElement.append(thisOrderInLogDataElement);
    #^_^_^_^_^_^_^_^_^_^_^^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^^_^_^_^_^

    #V~V~V~V~V~V~V~V~V~VV~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
    # Setting metadata of log file
    #------------------------------------------------------------------------
    uuidOfEntry = thisLogEntryElement.get("uuid");
    assert(uuidOfEntry is not None);
    elementForLastLogEntryUUIDs = ET.fromstring(
        """
        <lastLogEntryUUIDs>
            <i>{0}</i>
        </lastLogEntryUUIDs>
        """.format(uuidOfEntry)
    );
    logBookKeepingData = rootOfTree.find("bookKeepingData");
    oldElementForLastLogEntryUUIDs = logBookKeepingData.find("lastLogEntryUUIDs");
    logBookKeepingData.remove(oldElementForLastLogEntryUUIDs);
    logBookKeepingData.append(elementForLastLogEntryUUIDs);

    for thisTag in ["lastMachineReportedTime", "lastHumanReportedTime"]:
        oldElementReportedTime = logBookKeepingData.find(thisTag);
        if(oldElementReportedTime is not None):
            logBookKeepingData.remove(oldElementReportedTime);
        elementReportedTime = ET.fromstring("<" + thisTag + " />");
        dictMappingThisTagToElemInLogEntry = \
            {"lastMachineReportedTime" : "machineTimeLogEntryFinishedAndClosed", \
             "lastHumanReportedTime" : "srtfw"};
        for thisSubElem in thisLogEntryElement.find(dictMappingThisTagToElemInLogEntry[thisTag]).iter():
            if(thisSubElem.tag == dictMappingThisTagToElemInLogEntry[thisTag]):
                continue; # we don't want to include the element thisLogEntryElement.find(dictMappingThisTagToElemInLogEntry[thisTag]), only its children.
            elementReportedTime.append(thisSubElem);
        logBookKeepingData.append(elementReportedTime);
    #^_^_^_^_^_^_^_^_^_^_^^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^^_^_^_^_^


    return;

def frontEnd():

    repeatPrompt =True;
    fileNameForStartupMenu = "recentLogEntry.xml";
    buildStartUpMenu(fileNameForStartupMenu);
    while(repeatPrompt):
        try:
            timeElementForWhenStartedToFillLogEntry = formTimeElementForCurrentTime(\
                    tag="machineTimeLogEntryStarted", \
                    note="Automatically recorded time, based on the clock of the machine this form was being filled on, "+ \
                         "of when the log-entry form was first displayed to the user (accurate within a few seconds).");
            displayDocumentAndWaitForItToBeFilled(fileNameForStartupMenu);
            timeElementForWhenFinishedAndClosedLogEntry = formTimeElementForCurrentTime(\
                    tag="machineTimeLogEntryFinishedAndClosed", \
                    note="Automatically recorded time, based on the clock of the machine this form was being filled on, "+ \
                         "of when the log-entry was presumably finished and the window holding it was " +\
                         "closed by the used. ");
            thisLogEntryElement = readStartupMenu(fileNameForStartupMenu);
            thisLogEntryElement.append(timeElementForWhenStartedToFillLogEntry);
            thisLogEntryElement.append(timeElementForWhenFinishedAndClosedLogEntry);
            repeatPrompt = False;


            logThusFar = ET.ElementTree(file=config.pathToLogFile);
            setUpLogIfNecessary(logThusFar);
            setMetaDataOfLogEntryAndLogFile(logThusFar.getroot(), thisLogEntryElement);
            logEntriesElem = logThusFar.getroot().find("logEntries");
            logEntriesElem.append(thisLogEntryElement);
            logThusFar.write(config.pathToLogFile);
            if(thisLogEntryElement.find("commitLogFile").text == "Y"):
                autocommitBackupData();
            if(thisLogEntryElement.find("exitAfterEntry").text != "Y"):
                repeatPrompt = True;
                # Building fresh start menu.
                fileNameForStartupMenu = "recentLogEntry.xml";
                buildStartUpMenu(fileNameForStartupMenu);
        except:
            repeatPrompt = True;
            fileNameForErrorOutput = "errorOutput.txt";
            fh = open(fileNameForErrorOutput, "w");
            sys.stdout.flush();
            sys.stderr.flush();
            fh.flush();
            fh.write("V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V"  + "\n");
            fh.write("Error occured in processing file content put in by user. Details listed below."  + "\n");
            fh.write("===========================================================" + "\n");
            errorMessageIndented = "    " + traceback.format_exc().replace("\n", "\n    ");
            fh.write(errorMessageIndented  + "\n");
            fh.write("^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^" + "\n");
            fh.write("\n\n\n" + "\n");
            sys.stdout.flush();
            sys.stderr.flush();
            fh.flush();
            fh.close();
            displayDocumentAndDoNotWaitForItToBeFilled(fileNameForErrorOutput);


    return;
    

frontEnd();




