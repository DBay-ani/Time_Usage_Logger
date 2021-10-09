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

from contracts import *;
import re;
import uuid;
import xml.etree.ElementTree as ET;

def formTimeElement(tag, timeZone, seconds, minutes, hours, days, months, years, note=None):
    for thisArg in [seconds, minutes, hours, days, months, years]:
        requires( (thisArg is None) or isinstance(thisArg, int));
        requires( (thisArg is None) or (thisArg >= 0));
    requires( (tag is None) or (isinstance(tag, str)));
    requires( (tag is None) or (len(tag) > 0));
    alphanumericValues = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMM1234567890";
    requires( (tag is None) or (re.match( "^[" + alphanumericValues + "]*$", tag) is not None));
    requires( (note is None) or (isinstance(note, str)));
    requires( (note is None) or (len(note) > 0));
    # below, notice that spaces, dashes, underscores, and commas are allowed in the note.
    requires( (note is None) or (re.match( "^[" + alphanumericValues + " :;\\.\\(\\),_\\-" +"]*$", note) is not None));
    requires( (timeZone is None) or (isinstance(timeZone, str)));
    requires( (timeZone is None) or (len(timeZone) > 0));
    # below, notice that spaces, dashes, underscores and commas are allowed in the note.
    requires( (timeZone is None) or (re.match( "^[" + alphanumericValues + " ,_\\-" +"]*$", timeZone) is not None));


    baseString = """
    <{0} {8} {9}>
        <second>{2}</second>
        <minute>{3}</minute>
        <hour>{4}</hour>
        <day>{5}</day>
        <month>{6}</month>
        <year>{7}</year>
        <timezone>{1}</timezone>
    </{0}>
    """
    # Given how many headaches I have had specifying times correctly on systems and saying when
    # one is right or wrong, I figure it is better to give this a UUID so I can just talk about it 
    # directly.
    uuidToSubstituteIn = " uuid=\"" + str(uuid.uuid4()) + "\" "; # TODO: check this string.
    stringToIncludeForNote = "";
    if(note is not None):
        stringToIncludeForNote = " note=\"" + note +"\" ";

    thisTimeElement = \
        baseString.format(\
            tag, \
            timeZone, \
            seconds, minutes, hours, days, months, years, \
            stringToIncludeForNote, \
            uuidToSubstituteIn \
        );
    print(thisTimeElement);
    return ET.fromstring(thisTimeElement);


def test_formTimeElement():
    print(str(formTimeElement("test1", "PST", None, 1,2,3,4,5,note="test time element")));
    print(str(formTimeElement("test2", "fake", seconds=None, minutes=1,hours=2,days=3,months=4,years=None)));
    print(str(formTimeElement("test3", "fake", note="this is trying the note with named elements", seconds=None, minutes=1,hours=2,days=3,months=4,years=None)));
    # the below trials should not pass.
    try:
        print(str(formTimeElement("test4  ", "PST", None, 1,2,3,4,5,note="test time element")));
        print("FAIL");
    except:
        print("Passed");

    try:
        print(str(formTimeElement("test5", "time zone here :) nice", seconds=None, minutes=1,hours=2,days=3,months=4,years=None)));
        print("FAIL");
    except:
        print("Passed");

    try:
        print(str(formTimeElement("test6", "fake", \
            note="notes should note have to many special characters. For instance: />", seconds=None, minutes=1,hours=2,days=3,months=4,years=None)));
        print("FAIL");
    except:
        print("Passed");

    return;

# Note the compatibility of python's datetime module with python's time module :
#     https://docs.python.org/3/library/time.html#module-time
#     https://docs.python.org/3/library/datetime.html
# It is also good to be aware of INcompatability of certain Python time-related modules,
# as diligently pointed out by: Paul Ganssle in his blog post (archived version): 
#     https://web.archive.org/web/20211007171210/https://blog.ganssle.io/articles/2018/03/pytz-fastest-footgun.html
import time;
import datetime;

def formTimeElementForCurrentTime(tag, note=None):

    # The below commented-out line is not wrong
    # in the sense of getting the correct regional
    # timezones, but it fails to indicate which
    # one is currently in effect. While it would
    # be possible to determine the timezone currently
    # in effect from the rest of the timing information,
    # that would seem to be more a source of work and
    # confusion than aid.
    ### timeZone = ",".join(time.tzname);
    timeNowStruct = time.localtime();

    #V~V~V~V~V~V~V~V~V~V~V~V~V~V
    #Below section of code from https://discuss.python.org/t/get-local-time-zone/4169 ,
    #visited day7 month10 year2021
    #===========================
    now = datetime.datetime.now();
    local_now = now.astimezone();
    local_tz = local_now.tzinfo;
    local_tzname = local_tz.tzname(local_now);
    #^_^_^_^_^_^_^_^_^_^_^_^_^_^
    assert(isinstance(local_tzname, str));
    timeZone = local_tzname;

    return formTimeElement(tag, \
        timeZone=timeZone, \
        seconds=timeNowStruct.tm_sec, \
        minutes=timeNowStruct.tm_min, \
        hours=timeNowStruct.tm_hour, \
        days=timeNowStruct.tm_mday, \
        months=timeNowStruct.tm_mon, \
        years=timeNowStruct.tm_year, \
        note=note);

"""
def getDifferenceInTimeElements(timeElementA, timeElementB):
    # NOTE: below code does NOT properly handle leap-years.

    # orderToConsiderSubElements : (tag, number_of_seconds_it_corresponds_to)
    orderToConsiderSubElements = [\
        ("year", 365 * 24 * 60 * 60), \
        ("month", # oh... this needs to map a month to how many days it has ... 
"""
def cleanTextInTimeElements(thisText):
    return thisText.upper().replace(" ", "").replace("\t", "").replace("\n", "");

import re;

def cleanTextInTimeElementsAndConvertToInt(thisTextInTimeElementRead):
    requires(isinstance(thisTextInTimeElementRead, str));
    temp =  cleanTextInTimeElements(thisTextInTimeElementRead);
    tempIsAfternoonHour = ("PM" in temp);
    tempIsMorningHour = ("AM" in temp);
    if(tempIsAfternoonHour and tempIsMorningHour):
        raise Exception("Unknown value in time element: " + str(thisTextInTimeElementRead));
    temp = temp.replace("PM", "").replace("AM", ""); # this could hide a lot of problems, but it is hueristic afterall....
    if(re.match("^[0-9]*$", temp) is None):
        raise Exception("Unable to read element in time element: " + str(thisTextInTimeElementRead));
    if(len(temp) == 0):
        return None;
    temp = int(temp);
    if(tempIsAfternoonHour):
        # The modular arithmetic is to properly handle 12am and 12pm
        temp = (temp % 12) + 12;
    if(tempIsMorningHour):
        # The modular arithmetic is to properly handle 12am and 12pm
        temp = (temp % 12);
    return temp;

def hack_convertTimeZoneToGMTOffsetInSeconds(thisTimeZone):
    requires(isinstance(thisTimeZone, str));
    numberOfSecondsPerHour = 3600.0;
    thisDict= {"EDT" : 4.0, "EST" : 5.0, "UTC": 0.0, "GMT" : 0.0, "PST" : 8.0, "PDT" : 7.0};
    timeZoneSplit = [x.upper() for x in thisTimeZone.split(",") if len(x) > 0];
    setOfTimeOffSets = set();
    for thisSubTZ in timeZoneSplit:
        if(thisSubTZ not in thisDict):
            raise Exception("Unrecognized timezone: " + str(thisSubTZ));
        setOfTimeOffSets.add(thisDict[thisSubTZ] * numberOfSecondsPerHour);
    if(len(setOfTimeOffSets) != 1):
        raise Exception("Multiple timezones specified and do not share common offset from UTC. Timezones provided: " + str(thisTimeZone));
    return list(setOfTimeOffSets)[0];


from calendar import timegm as convertTimeInGMTConvertedToSecondsSinceEpoch;


def convertTimeElementToSeconds(thisTimeElement):
    requires(isinstance(thisTimeElement, ET.Element)); 
    childrenElems = thisTimeElement.getchildren();
    tagsInChildren = [x.tag for x in childrenElems];
    if(not set(tagsInChildren).issubset({'timezone', 'year', 'second', 'hour', \
                                         'minute', 'month', 'day'}) ):
        raise Exception("Time Element contains child with tag not among the values" + \
                        " {'timezone', 'year', 'second', 'hour', 'minute', 'month', 'day'}");
    if(len(set(tagsInChildren)) != len(childrenElems)):
        raise Exception("Time Element has children specifying the same quantity twice");
    orderToConsiderValues = ['year', 'month', 'day', 'hour', 'minute', 'second']; # In descending order of unit size.
    dictOfValuesSpecifiedUpToGranularityProvided = dict();
    rawDictTranslation = {x.tag : cleanTextInTimeElementsAndConvertToInt(x.text) \
                              for x in thisTimeElement.getchildren() if ( (x.text is not None) and (x.tag != 'timezone'))};
    unitOfPrecision=None;
    for thisKey in orderToConsiderValues:
        if(thisKey not in rawDictTranslation):
            break;
        if(rawDictTranslation[thisKey] is None):
            break;
        unitOfPrecision = thisKey;
        dictOfValuesSpecifiedUpToGranularityProvided[thisKey] = rawDictTranslation[thisKey];

    assert((unitOfPrecision is None) or (len(dictOfValuesSpecifiedUpToGranularityProvided) > 0));
    
    timeAsSecondsGMT = convertTimeInGMTConvertedToSecondsSinceEpoch( ( \
        dictOfValuesSpecifiedUpToGranularityProvided.get("year", 2020), \
        dictOfValuesSpecifiedUpToGranularityProvided.get("month", 1), \
        dictOfValuesSpecifiedUpToGranularityProvided.get("day", 1), \
        dictOfValuesSpecifiedUpToGranularityProvided.get("hour", 0), \
        dictOfValuesSpecifiedUpToGranularityProvided.get("minute", 0), \
        dictOfValuesSpecifiedUpToGranularityProvided.get("second", 0) \
        )  );
    timesAsSecondsProperlyAdjustedForTimeZone = timeAsSecondsGMT;
    for thisChildElem in thisTimeElement.getchildren():
        if(thisChildElem.tag == "timezone"):
            timesAsSecondsProperlyAdjustedForTimeZone = \
                timesAsSecondsProperlyAdjustedForTimeZone + \
                hack_convertTimeZoneToGMTOffsetInSeconds(cleanTextInTimeElements(thisChildElem.text));

    ensures(unitOfPrecision in {None, 'year', 'second', 'hour', 'minute', 'month', 'day'});
    return {"unitOfPrecision" : unitOfPrecision, \
            "timeInSecondsSinceEpoch" : timesAsSecondsProperlyAdjustedForTimeZone };



if(__name__ == '__main__'):
    test_formTimeElement();
    print("\n\n\n\n\n\n" + \
        str(convertTimeElementToSeconds( formTimeElementForCurrentTime("testOfCurrentTime", note="Should report the current time."))) + \
        "\n\n\n\n\n\n" , flush=True);
    A = ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry" uuid="c70412ac-e7f4-4b9b-85b6-01e70a702108">
    <minute>28</minute>
    <hour>5am</hour>
    <day>30</day>
    <month>5</month>
    <year>2020</year>
    <timezone>EDT</timezone>
</srtsw>
    """);
    print("\n\n\n\n\n\n" + str(convertTimeElementToSeconds( A )) + "\n\n\n\n\n\n" , flush=True);
    A = ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry" uuid="c70412ac-e7f4-4b9b-85b6-01e70a702108">
    <minute>28</minute>
    <hour>
		5pm
    </hour>
    <day>30</day>
    <month>

5
    </month>
    <year>2020</year>
    <timezone>EDT</timezone>
</srtsw>
    """);
    print("\n\n\n\n\n\n" + str(convertTimeElementToSeconds( A )) + "\n\n\n\n\n\n" , flush=True);
    A = ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry" uuid="c70412ac-e7f4-4b9b-85b6-01e70a702108">
    <minute>28</minute>
    <hour>5pm</hour>
    <day>30</day>
    <month>5</month>
    <year>2020</year>
    <timezone>GMT,UTC</timezone>
</srtsw>
    """);
    print("\n\n\n\n\n\n" + str(convertTimeElementToSeconds( A )) + "\n\n\n\n\n\n" , flush=True);
    A = ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry">
    <minute>
		
    </minute>
    <hour>	</hour>
    <day>		
</day>
    <month>
</month>
    <year>  </year>
    <timezone>EDT</timezone>
</srtsw>
    """);
    print("\n\n\n\n\n\n" + str(convertTimeElementToSeconds( A )) + "\n\n\n\n\n\n" , flush=True);

    A = ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry">
    <minute></minute>
    <hour></hour>
    <day></day>
    <month></month>
    <year>2019</year>
    <timezone>EDT</timezone>
</srtsw>
    """);
    print("\n\n\n\n\n\n" + str(convertTimeElementToSeconds( A )) + "\n\n\n\n\n\n" , flush=True);
    A1 =  ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry">
    <minute></minute>
    <hour>1PM</hour>
    <day>28</day>
    <month>2</month>
    <year>2019</year>
    <timezone>EDT</timezone>
</srtsw>
    """);
    A2 =  ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry">
    <minute></minute>
    <hour>1AM</hour>
    <day>1</day>
    <month>3</month>
    <year>2019</year>
    <timezone>EDT</timezone>
</srtsw>
    """);
    assert(convertTimeElementToSeconds( A2 )["timeInSecondsSinceEpoch"] - \
           convertTimeElementToSeconds( A1 )["timeInSecondsSinceEpoch"] == 12.0 * 3600.0);
    A1 =  ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry">
    <minute></minute>
    <hour>1PM</hour>
    <day>28</day>
    <month>2</month>
    <year>2020</year>
    <timezone>EDT</timezone>
</srtsw>
    """);
    A2 =  ET.fromstring("""
<srtsw note="Self-Reported Time Started Writting Log Entry">
    <minute></minute>
    <hour>1AM</hour>
    <day>1</day>
    <month>3</month>
    <year>2020</year>
    <timezone>EDT</timezone>
</srtsw>
    """);
    assert(convertTimeElementToSeconds( A2 )["timeInSecondsSinceEpoch"] - \
           convertTimeElementToSeconds( A1 )["timeInSecondsSinceEpoch"] == 36.0 * 3600.0);
    print(str(formTimeElementForCurrentTime("testOfCurrentTime", note="Should report the current time.")), flush=True);



