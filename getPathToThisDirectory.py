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

# below taken from : https://stackoverflow.com/questions/50499/how-do-i-get-the-path-and-name-of-the-file-that-is-currently-executing
# it prints the current directory that this code is found in....

import os
import inspect

def getPathToThisDirectory():
    pathToThisDirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
    return pathToThisDirectory + "/";
