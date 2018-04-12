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
        self.ref_values = [('templates', 'preproc', 'preproc_template.sh.j2'),
                           ('templates', 'analysis', 'analysis_template.sh.j2'),
                           ('templates', 'output', 'output_template.html.j2'),
                           ('templates', 'venn', 'venn_diagrams_template.html.j2'),
                           ('file_globs', 'shared', '*shared'),
                           ('file_globs', 'tax_sum', '*cons.tax.summary'),
                           ('file_globs', 'design', '*design'),
                           ('css', 'w3', '<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">'),
                           ('css', 'datatables', '<link rel="stylesheet" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css">'),
                           ('js', 'slideshow', 'slideshow.js'),
                           ('js', 'datatables', 'datatables.js'),
                           ('N', 'partition', 'long'),
                           ('N', 'nodes', '1'),
                           ('N', 'ntasks_per_node', '1'),
                           ('N', 'processors', '12'),
                           ('S', 'partition', 'long'),
                           ('S', 'nodes', '2'),
                           ('S', 'ntasks_per_node', '1'),
                           ('S', 'processors', '24'),
                           ('M', 'partition', 'long'),
                           ('M', 'nodes', '10'),
                           ('M', 'ntasks_per_node', '1'),
                           ('M', 'processors', '120'),
                           ('L', 'partition', 'long'),
                           ('L', 'nodes', '20'),
                           ('L', 'ntasks_per_node', '1'),
                           ('L', 'processors', '240'),
                           ('XL', 'partition', 'long'),
                           ('XL', 'nodes', '40'),
                           ('XL', 'ntasks_per_node', '1'),
                           ('XL', 'processors', '480'),
                           ('PHI', 'partition', 'accel'),
                           ('PHI', 'nodes', '1'),
                           ('PHI', 'ntasks_per_node', '1'),
                           ('PHI', 'processors', '32'),
                           ('JUMBO', 'partition', 'accel'),
                           ('JUMBO', 'nodes', '4'),
                           ('JUMBO', 'ntasks_per_node', '1'),
                           ('JUMBO', 'processors', '128'),
                           ('databases', 'align', 'null'),
                           ('databases', 'taxonomy', 'null')]
        self.config = ConfigParser.SafeConfigParser()
        self.config.read("mothulity.config")

    def test_config_file_read(self):
        """
        Tests records from the config file.
        """
        self.test_values = []
        for s in self.config.sections():
            for o in self.config.options(s):
                self.test_values.append((s, o, self.config.get(s, o)))
        self.assertEqual(self.ref_values, self.test_values)
