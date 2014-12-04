""" vapory/__init__.py """


from .vapory import *
from .version import __version__

 
__all__ = [k for k in locals().keys() if k not in
           ['webbrowser',
            'deepcopy',
            'WIKIREF',
            'vectorize',
            'format_if_necessary']]
