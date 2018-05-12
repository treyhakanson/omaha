import re
from functools import reduce
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


def build_header(types=[], attrs=[], pre_cols=[]):
    header = [*pre_cols]
    if len(types) > 0:
        for type in types:
            for attr in attrs:
                col = "%s__%s" % (type, attr)
                header.append(col)
    else:
        for attr in attrs:
            header.append(attr)
    return header


def log_query(cursor, query, args):
    if len(args) > 0:
        cursor.execute("SELECT " + ", ".join(["quote(?)" for i in args]), args)
        quoted_values = cursor.fetchone()
        for quoted_value in quoted_values:
            query = query.replace('?', str(quoted_value), 1)
    print(query)


def avg_cols(mat):
    res = []
    rows = len(mat)
    cols = len(mat[0])
    for j in range(cols):
        sum = 0
        for i in range(rows):
            sum += mat[i][j]
        res.append(sum / rows)
    return res
