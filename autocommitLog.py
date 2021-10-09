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

import os;
import re;
from contracts import *;
from subprocess import Popen, PIPE ;
import config;
from getPathToThisDirectory import getPathToThisDirectory;

def autocommitBackupData():
    pathToFolderHoldingLog = getPathToThisDirectory() + config.relativePathToFolderHousingLogFile;
    stringCommandToCommitFile = """
        cd {0}; 
        git add {1};
        git commit -m "AUTOCOMMIT";
        exit;""".format(pathToFolderHoldingLog, config.logFileName);
    fh = open("tempStringForAutoCommit.sh", "w");
    fh.write(stringCommandToCommitFile);
    fh.flush();
    fh.close();
    thisProc = Popen(["bash",  "tempStringForAutoCommit.sh" ], stdout=PIPE);
    thisProc.wait();
    output = thisProc.communicate();
    if(output[-1] not in {0, None}):
        raise Exception("Unknown error while committing backup content.");
    print("Autocommitted time log.", flush=True);
    return;

if(__name__ == "__main__"):
    autocommitBackupData();
