#! /usr/bin/env python

"""
Warnings informing that something went differently that intended. Does not
include messages before exiting with code 1
"""

CONFIG_OPEN_FAIL = """
Failed to find or open {} config file. Using default.
"""
NO_TAX_FILE_FOUND = """
WARNING!!! No proper tax.summary file found. The analysis will be incomplete.
"""
JUNK_GROUPS_DETECTED = """
{} can distort the analysis due to size too small
"""
JUNK_REMOVED = """
{} will be removed
"""
