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


def getGitCommitHash():

    thisProc = Popen(["git", "log", "-n1"],stdout=PIPE);
    thisProc.wait();
    output = thisProc.communicate();
    if(output[-1] not in {0, None}):
        raise Exception("Unknown error while getting git hash.");
    
    firstLine = output[0].decode().split("\n")[0];
    assert(isinstance(firstLine, str));
    assert(len(firstLine) > 8); # at least 7 characters for the beginning "commit "
        # and one character for the ending newline.
    assert(firstLine[0:7] == "commit ");
    assert(firstLine[-1] != "\n");

    proposedCommitHash = firstLine[7:];
    # below assert is checking that we extracted the full hash in the range
    assert("commit " + proposedCommitHash  == firstLine);
    # the below assert checks that the proposed hash is an alphanumeric string from 
    # beginning to end
    assert(re.match("^[a-zA-Z0-9]*$", proposedCommitHash) != None);

    return proposedCommitHash;

gitCommitHashAtStartOfRun = getGitCommitHash();
