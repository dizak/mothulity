# -*- coding: utf-8 -*-


import unittest
import ConfigParser
import subprocess as sp
from mothulity import *


class PathTests(unittest.TestCase):
    """
    Tests of the $PATH system variable.
    """
    def test_path(self):
        """
        Tests if mothulity is in the system $PATH variable.
        """
        self.assertEqual(sp.check_output(["which", "mothulity.py"]).strip().split("/")[-1],
                         "mothulity.py")


class ConfigTests(unittest.TestCase):
    """
    Tests of the config file.
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.
        """
        self.ref_values = ["preproc_template.sh.j2",
                           "analysis_template.sh.j2",
                           "output_template.html.j2",
                           "venn_diagrams_template.html.j2",
                           "*shared",
                           "*cons.tax.summary",
                           "*design",
                           '''<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">''',
                           '''<link rel="stylesheet" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css">''',
                           "slideshow.js",
                           "datatables.js",
                           "long",
                           "1",
                           "1",
                           "12",
                           "long",
                           "2",
                           "1",
                           "24",
                           "long",
                           "10",
                           "1",
                           "120",
                           "long",
                           "20",
                           "1",
                           "240",
                           "long",
                           "40",
                           "1",
                           "480",
                           "accel",
                           "1",
                           "1",
                           "32",
                           "accel",
                           "4",
                           "1",
                           "128",
                           "null",
                           "null"]
        self.config = ConfigParser.SafeConfigParser()
        self.config.read("mothulity.config")

    def test_config_file_read(self):
        """
        Tests records from the config file.
        """
        self.test_values = []
        for s in self.config.sections():
            for o in self.config.options(s):
                self.test_values.append(self.config.get(s, o))
        self.assertEqual(self.ref_values, self.test_values)
