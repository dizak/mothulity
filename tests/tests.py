# -*- coding: utf-8 -*-


import unittest
import ConfigParser
import subprocess as sp


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
        self.config = ConfigParser.SafeConfigParser()
        self.config.read("mothulity.config")

    def test_config_file(self):
        """
        Tests records from the config file.
        """
        self.assertEqual(self.config.get("templates", "preproc"),
                         "preproc_template.sh.j2")
        self.assertEqual(self.config.get("templates", "analysis"),
                         "analysis_template.sh.j2")
        self.assertEqual(self.config.get("templates", "output"),
                         "output_template.html.j2")
        self.assertEqual(self.config.get("templates", "venn"),
                         "venn_diagrams_template.html.j2")
        self.assertEqual(self.config.get("file_globs", "shared"),
                         "*shared")
        self.assertEqual(self.config.get("file_globs", "tax_sum"),
                         "*cons.tax.summary")
        self.assertEqual(self.config.get("file_globs", "design"),
                         "*design")
        self.assertEqual(self.config.get("css", "w3"),
                         '''<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">''')
        self.assertEqual(self.config.get("css", "datatables"),
                         '''<link rel="stylesheet" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css">''')
        self.assertEqual(self.config.get("js", "slideshow"), "slideshow.js")
        self.assertEqual(self.config.get("js", "datatables"), "datatables.js")
        self.assertEqual(self.config.get("N", "partition"), "long")
        self.assertEqual(self.config.get("N", "nodes"), "1")
        self.assertEqual(self.config.get("N", "ntasks_per_node"), "1")
        self.assertEqual(self.config.get("N", "processors"), "12")
        self.assertEqual(self.config.get("S", "partition"), "long")
        self.assertEqual(self.config.get("S", "nodes"), "2")
        self.assertEqual(self.config.get("S", "ntasks_per_node"), "1")
        self.assertEqual(self.config.get("S", "processors"), "24")
        self.assertEqual(self.config.get("M", "partition"), "long")
        self.assertEqual(self.config.get("M", "nodes"), "10")
        self.assertEqual(self.config.get("M", "ntasks_per_node"), "1")
        self.assertEqual(self.config.get("M", "processors"), "120")
        self.assertEqual(self.config.get("L", "partition"), "long")
        self.assertEqual(self.config.get("L", "nodes"), "20")
        self.assertEqual(self.config.get("L", "ntasks_per_node"), "1")
        self.assertEqual(self.config.get("L", "processors"), "240")
        self.assertEqual(self.config.get("XL", "partition"), "long")
        self.assertEqual(self.config.get("XL", "nodes"), "40")
        self.assertEqual(self.config.get("XL", "ntasks_per_node"), "1")
        self.assertEqual(self.config.get("XL", "processors"), "480")
        self.assertEqual(self.config.get("PHI", "partition"), "accel")
        self.assertEqual(self.config.get("PHI", "nodes"), "1")
        self.assertEqual(self.config.get("PHI", "ntasks_per_node"), "1")
        self.assertEqual(self.config.get("PHI", "processors"), "32")
        self.assertEqual(self.config.get("JUMBO", "partition"), "accel")
        self.assertEqual(self.config.get("JUMBO", "nodes"), "4")
        self.assertEqual(self.config.get("JUMBO", "ntasks_per_node"), "1")
        self.assertEqual(self.config.get("JUMBO", "processors"), "128")
