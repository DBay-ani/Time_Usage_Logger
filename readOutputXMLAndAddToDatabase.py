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

import uuid;

from getGitCommitHash import gitCommitHashAtStartOfRun;

from config import tagsToAddUUIDsTo, tagsToAddGitHashTo; 

def readStartupMenu(fileNameToSaveTo):
    requires(isinstance(fileNameToSaveTo, str));
    requires(len(fileNameToSaveTo) > 0);
    # TODO: check that fileNameToWriteTo is appropraite in 
    #     more ways than just the above two lines...
    properTree = ET.ElementTree(file=fileNameToSaveTo);
    print("=====================");
    print("=====================");
    print(str(ET.dump(properTree)));
    for thisElem in properTree.iter():# tag="startUpMenu"):
        if(thisElem.tag in tagsToAddUUIDsTo):
            if(thisElem.get("uuid", default=None) is not None):
                raise Exception("""thisElem.get("uuid", default=None) is not None""");
            thisElem.set("uuid", str(uuid.uuid4()));
        if(thisElem.tag in tagsToAddGitHashTo):
            if(thisElem.get("gitHash", default=None) is not None):
                raise Exception("""thisElem.get("uuid", default=None) is not None""");
            thisElem.set("gitHash", gitCommitHashAtStartOfRun);

    print("------------------");
    print(str(ET.dump(properTree)));
    return properTree.getroot();



