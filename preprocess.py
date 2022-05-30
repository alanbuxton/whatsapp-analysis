import re
import pandas as pd

def merge_lines(lines):
    data = {"date":[],"time":[],"msg":[]}
    date = None
    time = None
    msg_lines = []
    for row in lines:
        res = re.search(r"^(\d+/\d+/\d+), (\d+:\d+) - (.+)$",row)
        if res is None:
            # not a new message
            msg_lines.append(row)
        else:
            # is a new message
            # if already have a message, add it to DF
            if date:
                data["date"].append(date)
                data["time"].append(time)
                data["msg"].append("".join(msg_lines))
                date = None
                time = None
                msg_lines = []
            # get new message ready
            groups = res.groups()
            date = groups[0]
            time = groups[1]
            msg_lines = [groups[2]]
    data["date"].append(date)
    data["time"].append(time)
    data["msg"].append("".join(msg_lines))
    return data





### Person: sent a message

def message_sender(row):
    matches = re.search(r"^(.+?): (.+)$",row.msg,re.MULTILINE)
    if matches is None:
        return None, None
    else:
        grouped = matches.groups()
        sender = grouped[0]
        message = grouped[1]
        return sender, message



### Person added People

def x_added_y(row):
    matches = re.search(r"^(.+) added (.+)",row.msg)
    if matches is None:
        return None,None
    else:
        people = matches.groups()
        adder = people[0]
        first_last_addees = people[1].split(" and ")
        addees = first_last_addees[0].split(",")
        if len(first_last_addees) > 1:
            addees.append(first_last_addees[1])
        addees = [x.strip() for x in addees if x != '']
        return adder, addees


### Person left
def left(row):
    matches = re.search(r"^(.+) left$",row.msg)
    if matches is None:
        return None
    else:
        leaver = matches[0]
        return leaver


### Person joined using XXX

def joiner(row):
    matches = re.search(r"^(.+) joined using",row.msg)
    if matches is None:
        return None
    else:
        joiner = matches.groups()[0]
        return joiner


### <PEOPLE> 'were added'

def unspecified_joiner(row):
    matches = re.search(r"(.+) were added",row.msg)
    if matches is None:
        return None
    else:
        first_last_joiners = matches.groups()[0].split(" and ")
        joiners = first_last_joiners[0].split(",")
        joiners.append(first_last_joiners[1])
        joiners = [x.strip() for x in joiners if x != '']
        return joiners


### Did an action

def did_an_action(row):
    matches = re.search(r"(.+) turned o.+ disappearing",row.msg)
    if matches is None:
        return None
    else:
        return matches.groups()[0].strip()
