import re
from bs4 import BeautifulSoup as bs, Comment


def getyear(s):
    '''get the year from a well-formatted file name.'''
    return int(re.match(r"(\d+)\.week\d+\.htm", s).group(1))


def getweek(s):
    '''get the week from a well-formatted file name.'''
    return int(re.match(r"2017\.week(\d+)\.htm", s).group(1))


def soupify_comment(soup, id, el="div"):
    '''
    Retrieve comment from soup by id, and convert into a soup object.
    args:
        s (bs) - soup object to search
        id (str) - str id to find in s
    returns:
        retrieved comment as a soup object
    '''
    wrapper = soup.find(el, {"id": id})
    comment = wrapper.find(text=lambda txt: isinstance(txt, Comment))
    return bs(comment, "html.parser")
