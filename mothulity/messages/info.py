#! /usr/bin/env python

"""
Regular messages printed to the user when everything goes fine
"""

FILES_COPIED = """
Copying the test-run files into your CWD...
"""
DBCUT_PARAMS = """
Alignment region custamization will be executed with\n
the following parameters:\n
original database: {}\n
region coordinates: {}-{}
"""
CONFIG_USED = """
Using {} as config file.
"""
SHARED_FILE_FOUND = """
Found {} shared file
"""
TAX_FILE_FOUND = """
Found {} tax.summary file
"""
MULTIPLE_DESIGN_FILES_FOUND = """
More than 1 design files found. Will skip this part of analysis.
"""
GROUPS_LABEL_DETECTED = """
Detected {} groups with {} label
"""
KEEP_ALL = """
All groups will be kept due to --keep-all argument
"""
TEMPLATE_USED = """
\nTemplate used:\n\n{}
"""
