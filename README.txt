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


V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Overview
===============================================================================

This repo houses a light-weight implementation of a time-tracker/time-recorder
that, for the purposes of this documentation and license, we call TimeLogger.

The operation of TimeLogger is relatively straight forward. After the first-time
setup, one simply invokes the program from terminal. From there, an empty
log-entry appears in gedit, which the user may fill whenever they feel it is 
appropriate. Saving and then closing the gedit window results in the log-entry 
being added into the record with previous entries, and automatically brings a 
new, blank entry up to be filled next. Log-entries themselves are displayed as
an XML document for which users fill whatever subset of the fields they feel
necessary to adequately describe their activity; in particular, users don't have
to enter any XML structural information, just text between tags (the "fields" 
for them to fill). 

A number of fields - such as time start / time finished - are 
automatically filled behind the scenes, but the log-entry template does provide
a spot for users to provide that information themselves if they feel it is 
necessary (for example, if their system clock is not set properly or because of
special circumstances). Error 
handling - for example, because a user enters something syntactically poisonous -
is implemented.

To see the default fields supported for entries, see:
    templateForLogEntries.xml
Note that users may fill any of the fields they like in an entry, but are 
not required to fill any. For example, one does not need to provide a value for
"explicit exercise" if they did not exercise since the time of the previous
log-entry. Users are free to modify this template as they like. We advise that,
unless one is willing to examine the code, modification be limited to additions
to the template (i.e., not removing fields). Users interested in expanding the
template may also like to visit:
    config.py
which lists options for the automatic addition of attributes to elements. In
the config.py file, users can also modify where their log-file is saved. 

While the log-file itself is saved in an XML format, roughly as readable as
the log-entries users initially provide, we do also supply two scripts to 
print recent log-entries in an easier-to-read format. "Easier to read" here
includes not printing fields for which the user did not provide a value (for
instance, the "explicitExercise"-element would not print for an entry in which
the user did not indicate they explicitly exercised). Since UUIDs 
(Universally Unique Identifiers) are automatically added to elements of interest
(see config.py for which elements), users may wish to refer to their earlier
activity in order to retrieve UUIDs of elements which they wish to make 
reference to. Naturally, there are numerous reasons why a person may
wish to review their logs from the relatively-recent past. Motivations aside,
two scripts facilitate this easy review:
    printLastKInHumanReadableWay.py
        As the name entails, prints the previous k entries. Type --help for
        information on use.
    printLogs_timeBase.py
        Prints logs from the previous d-days, where d is a user-specified
        parameter. Type --help for information on use.

        This program is not completed, but points the way to implementing
        other useful features. See TODOS.txt and the below section "Other 
        Technical Details".
Obviously, the output of either script can be redirected (redirected in the 
Unix I/O redirection sense), enabling further review / filtering.

See the DEPENDENCIES.txt file for required software, LICENSE.txt for license
information, and TODOS.txt for some items that would be nice to implement. In
regard to dependencies: most versions of Ubuntu Linux that have Python 3.6
should be able to run this code without the need of additional software
installation.

As of the initial public commit of this software, most code here was written in
late March to mid-June 2020. Some cleaning and touch-ups were done in October
2021 prior to the public release of the code. 

^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Typical Operation
===============================================================================

After performing the initial-setup steps ( see the section called
"Things to Do Before First Use" below), typical operations proceeds as follows:

To Start the Program:
     python3.6 timeLogger.py 

Interacting with the Program:
    Look over the fields available and enter the information you believe is 
    reflective of how you used the time. Users are not required to provide
    values for any of the fields listed. Behind the scenes, TimeLogger adds
    some information to the content users provided, such as the UUIDs mentioned
    in the previous section. Additional information about automatically added 
    fields can be found in the section title "Other Technical Details" below.

    After a user finishes a log-entry, TimeLogger prints the full entry - with
    automatically added content - to the terminal. Among other things, this
    easily allows users to see the UUIDs of recently passed events and thus more 
    easily reference them. For those who find this output burdensome, you are
    of course free to pipe to /dev/null (i.e., python3.6 timeLogger > /dev/null)
    or run the program in a session of tmux (tmux: the Linux multiplexer 
    utility).

    While most user-provided values should be self-explanatory, a few may need
    further elaboration:

        srtsw ("Self-Reported Time Started Writing Log Entry")
            Users, if they would like, can record when they started writing 
            their log-entry here. This, for instance, is worthwhile if the user 
            wants to track how much time they spend on writing log-entries; 
            example motivations a user may have do doing this include: (1) 
            because they have a propensity for verbosity, (2) they expect that
            their current entry will take awhile to write, (3) they have an 
            honest curiosity about how quickly they can fill a log.

            It is worth noting that unlike the other optional time-related 
            information list here, this element cannot in general be inferred
            from the automatically provided time-information. The automatically
            recorded timing information attempts to capture when a log-entry 
            was created (which is typically when the previous log-entry ended) 
            and when a log-entry ends - this timing information includes both 
            duration of events reported in the log and time taken to write the
            log-entry itself. Thus, with the "srtsw"-element, users can provide 
            details about the duration of the reported events and, 
            independently, the time interval used to write the log-entry.

        description
            While the name of this field should give an idea of what it is meant
            for, it is worth explaining its role in respect to the other fields
            available. The primary intent of this field is to provide an option
            to list details that are difficult to phrase in the other, more 
            narrowly-focused fields, or provide any context/ nuance to the 
            entry's information which the user may otherwise believe is missing.
            This field is not required to be filled. If the user thinks the
            "completed"-element and "next"-element are enough to express what 
            they want, then there is likely no need to fill the description 
            field.

       "<i>" - present under "completed"-, "next"-, and
           "foodAndDrinkRelated"-elements

           These are the containing elements for items in a list. The "i" is for
           item. In order to list more than one item, simply copy-and-paste the 
           content in <i>[...]</i> .

       timeActivityBegan
           As described in the template:
              "Time the activity reported in this log began, if not roughly the 
              time the previous log finished (leave blank if this activity began
              roughly immediately after the previous log was finished being 
              written)."
           This is useful in many circumstances, such as if, hypothetically, one
           used TimeLogger to record their activity at a 9am-to-5pm job; in such
           a situation, their first entry of the work-day would indicate 
           activity started at 9am, as opposed to 5pm, the time that the 
           previous long entry ended. Note that this even provides distinct
           information from "machineTimeLogEntryStarted" (commented on in the 
           "Other Technical Details" section), since a person might
           retroactively record their activity or, in the job scenario, start 
           the TimeLogger shortly after setting up some other materials.  

       timeActivityFinished
           A natural counterpart to the "timeActivityBegan"-element that records
           when an activity ended. The motivations and uses of this element are
           similar to those of the "timeActivityBegan"-element. 

       srtfw ("Self-Reported Time Finished Writing Log Entry")
           Similar to the "srtsw"-element, except for listing the time that one
           finishes writing the log-entry.

           In contrast to the "srtsw"-element, which captures information not
           present anywhere else, the "srtfw"-element should - in normal 
           circumstances - be basically repetitive with the 
           "machineTimeLogEntryFinishedAndClosed"-element automatically added to 
           log-entries (see the section "Other Technical Details" below). In 
           normal circumstances, the "srtfw"-element and the 
           "machineTimeLogEntryFinishedAndClosed"-element
           may be different, but for trivial reasons - such as the user taking a
           few seconds to close a log-entry, or forgetting to close a log-entry 
           prior to walking away. An abnormal circumstance where they may differ
           is if the clock of the computer running TimeLogger is inaccurate. 
           Tangentially, we mention that TimeLogger stores log-entries as a 
           linked-list, joined in order of creation - thus, the chronological 
           order of entries in a single log-file will be accurate even if the
           host computer's clock has fluctuating accuracy. 


To Exit:
    As seen in the template, exit and committing of the log-records are 
    controlled in the bottom two fields. 

    If a user does not indicate that they wish to exit, then the default 
    behavior is to open another entry immediately after the current one closes.
    To change this default behavior for all log-entries, simply change the 
    respective value in the template ( see the "exitAfterEntry"-element in 
    templateForLogEntries.xml).
     
    To commit the log-file after adding the current log-entry, see the
    "commitLogFile"-element. Like the exit behavior, the default behavior for
    committing can also be changed by modifying the template. 


Handling Errors:
    If an error occurs as a result of users entering invalid content into the
    log-entry, an error message will appear and the log-entry causing the issue
    will be re-open in order for the user to correct it. When a log-entry is 
    reopened, it retains all the content the user had previously inserted into
    it.
    
    An error message appears as new document in gedit called "errorOutput.txt".
    errorOutput.txt simply informs the user of the issue, and can be closed 
    whenever the user would like. The error message should appear at the same
    time that the log-entry reopens - that is, one does not need to close the
    error message in order for the error-inducing log-entry to reappear.


Getting the Durations of Events:
    See TODOS.txt . Some code exists that is en route to being able to 
    report / collect event durations, but functionality in that direction is
    not yet complete.

Merging Multiple Log-Files into One:
    See the section "Other Technical Details" below.

^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Things to Do Before First Use
===============================================================================

Before the first use, the current implementation of TimeLogger requires some
minimal initial setup.

First, take a look at config.py . By default, the user should not have to modify
anything there in order for the program to function properly. However, if the
user would like to change the name of the log-file or where it is saved, this
is the location to make those changes. For the rest of this discussion, we will
assume the default values are used, but this is simply for ease of reference. 

Next, navigate to the folder that will hold the log-file - by default, this is
./houseForLog . Initialize a new, empty log-file by doing the following:
    cp templated_timeLog.xml timeLog.xml
The file templated_timeLog.xml is simply a template for log-files, and 
timeLog.xml is (unless changed in config.py) the name of the log-file with 
TimeLogger will write into. 

We suggest leveraging the benefits of version control to track and protect your
log-file(s). To facilitate that, log-entries have a "commitLogFile" field which,
when indicated by the user, automatically commits the log-file into a local git
repo. To use this feature, however, the log-file has to be located inside a 
git repo and not ignored by git (i.e., not listed in a .gitignore file for the
repo). Under the default settings, any content in the ./houseForLog folder
(other than the files provided with this code) are ignored by the git repo 
tracking this code. That is, by default, ./houseForLog/timeLog.xml is not 
tracked or backed-up, etc. We suggest doing the following to enable tracking
your log-file:
    cd ./houseForLog ; 
    git init . ;
    cd .. ;
Doing this will create a new, local git repo that is SEPARATE from the git repo
managing this code. This separation is good, preventing accidental spread of
personal information and maintaining a clear division between code and data.

You may find git submodules useful for you (see, for instance, 
https://git-scm.com/book/en/v2/Git-Tools-Submodules ), but you are not required
to use them here. For individual, personal use, there would appear to be little
added utility for pursuing this additional complexity, short of being a "power
user" of some sort.

^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Other Technical Details
===============================================================================

We suggest, after making a log-entry or two, looking at the content of the 
log-file to get a sense of the book-keeping done and the nature of the content
which is automatically added. For instance, certain elements - namely, those 
indicated in the config.py file - will have UUIDs added as attributes. Other 
elements will have the git-hash of the code added as an attribute (which is 
useful for any debugging or data-migrating needed in the future). 

In addition to attributes being added to log-entries, notice the elements that 
were automatically included in the log-file, such as 
"machineTimeLogEntryStarted" and "machineTimeLogEntryFinishedAndClosed" to house
automatically gathered timing information. Of particular interest are the 
"orderingInLogData"-elements added to each log-entry, which serves two 
functions: (1) listing which log-file the log-entry was originally added to, 
which provides some provenance information (2) listing the UUID(s) of the 
log-entry/entries that are immediately prior to the new log-entry, creating a
linked-list which accurately reflects the chronological order of logs, even if
the other timing information is missing or inaccurate. In the case where only a
single log-file is maintained, then (1) is simply a nicety, and the 
UUID-references in (2) form a single, straight chain. In the case where a user
has multiple log-files which they would like to combine, the motivation for (1) 
becomes much clearer, as does our use of plurals (UUID_s_ and log-entr_ies_ ) in
describing (2).

In addition to content mentioned in the previous paragraph, some limited 
book-keeping is maintained at the top-level of a log-file, such as the UUID
of the most recently added log-entry.

Outside of the log-file's composition, it is worth noting that some temporary
files may be generated in the process of TimeLogger running. In the current
implementation, these files will be located in the top-level director of the
git-repo. Git is configured to ignore these files (they are listed in the 
local .gitignore file).

For additional technical details and features to expand on, see TODOS.txt .

^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


