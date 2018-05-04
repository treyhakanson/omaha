import re


def getyear(s):
    '''get the year from a well-formatted file name.'''
    return int(re.match(r"(\d+)\.week\d+\.htm", s).group(1))


def getweek(s):
    '''get the week from a well-formatted file name.'''
    return int(re.match(r"2017\.week(\d+)\.htm", s).group(1))
