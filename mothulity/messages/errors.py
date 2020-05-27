#! /usr/bin/env python

"""
Error messages printed to the user before mothulity exists with code 1
"""

SLURM_SETTING_UNDEFINED = """
No SLURM settings defined.
"""
TEMPLATES_NOT_IN_CONFIG = """
Templates not found in config file! Quitting...
"""
ALIGN_DB_PATH_NOT_IN_CONFIG = """
Align database path not found in config file.
"""
TAX_DB_PATH_NOT_IN_CONFIG = """
Taxonomy database path not found in config file.
"""
CSS_NOT_IN_CONFIG = """
CSS links not found in config file! Output will not display properly!
"""
JS_NOT_IN_CONFIG = """
Javascript links not found in config file. Output will not display properly!
"""
SLURM_SETTINGS_NOT_CONFIG = """
SLURM setting not found in config file! Quitting...
"""
ALIGN_DB_PATH_NOT_ANY = """
No align database path defined in config nor command-line. Quitting...
"""
TAX_DB_PATH_NOT_ANY = """
No taxonomy database path defined in config nor command-line. Quitting...
"""
INPUT_DIR_NOT_FOUND = """
Input directory not found. Quitting...
"""
OUTPUT_DIR_NOT_FOUND = """
Output directory not found. Quitting...
"""
ALIGN_DB_NOT_FOUND = """
No align database found in {}. Quitting...
"""
TAX_DB_NOT_FOUND = """
No taxonomy database found in {}. Quitting...
"""
MULTIPLE_SHARED_FILES_FOUND = """
More than 1 shared files found. Quitting...
"""
DASHES_NOT_REJECTED = """
Mothur does not accept dashes in the paths. Please rename:\n{}
"""
SHARED_NOT_FOUND = """
No shared file found. Quitting...
"""
SHARED_ALREADY_EXISTS = """
Found shared file but you do not want to run the analysis on it. Running
preprocessing would overwrite it. Quitting...
"""
DB_CUT_END_BEFORE_START = """
Error: DB cut start position higher then the end one.
"""
DB_CUT_NON_ALPHA_CHARS = """
Error: DB alignment region coordinates contain both '-' and charaters different then numbers.
"""
DB_CUT_TOO_MANY_REGIONS = """
Wrong alignment customization specification: {}.
"""
DB_CUT_FAILURE = """
Type proper region name/coordinates for db cutting or use already existing database.
"""
COMPLETE_NONSENSE = """
I don't know what you what me to do!!! There are no files I can recognize in here!
"""
