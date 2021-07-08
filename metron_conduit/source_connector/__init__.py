"""
Customized package loading when imported in a following way: `from metron_conduit.source_connector import *`.
This allows to collect programmatically all child classes of *Abstract Connector* class and avoids maintaining manually
list of all child classes, which easy code basis extension from the future perspective - class renaming,
adding new ones, etc...

The list of all child classes is useful when class attributes are collected or to determine class instance during
on the fly.

Getting of all child classes is illustrated in this code snippet:
```
from metron_conduit.source_connector import * # imports all modules in the package, so Python can see all the children
from metron_conduit.source_connector.abstract_source import AbstractConnector # manual import for statical IDE analysis

all_children = source_connector.AbstractConnector.__subclasses__()
```
"""


import os.path as os_path
import glob

modules = glob.glob(os_path.join(os_path.dirname(__file__), "*.py"))
__all__ = [os_path.basename(f)[:-3] for f in modules if os_path.isfile(f) and not f.endswith("__init__.py")]
