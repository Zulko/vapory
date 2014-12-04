WIKIREF = "http://wiki.povray.org/content/Reference:"

def vectorize(arr):
    """ transforms [a, b, c] into string "<a, b, c>"" """
    return "<%s>" % ",".join([str(e) for e in arr])

def format_if_necessary(e):
    """ If necessary, replaces -3 by (-3), and [a, b, c] by <a, b, c> """

    if isinstance(e, (int, float)) and e<0:
        # This format because POVray interprets -3 as a substraction
        return "( %s )"%str(e)
    if hasattr(e, '__iter__') and not isinstance(e, str):
        # lists, tuples, numpy arrays, become '<a,b,c,d >'
        return vectorize(e)
    else:
        return e
