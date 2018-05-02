# -*- coding: utf-8 -*-


import unittest
import ConfigParser
import subprocess as sp
import utilities


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
                           ('JUMBO', 'processors', '128')]
        self.config = ConfigParser.SafeConfigParser()
        self.config.read("./tests/test.config")

    def test_config_file_read(self):
        """
        Tests records from the config file.
        """
        self.test_values = []
        for s in self.config.sections():
            for o in self.config.options(s):
                self.test_values.append((s, o, self.config.get(s, o)))
        self.assertEqual(self.ref_values, self.test_values)


class UtilitiesTests(unittest.TestCase):
    """
    Tests of mothulity.utilities module.
    """

    def setUp(self):
        """
        Sets up class level attributes for the tests.
        """
        self.cfg_file_name_1 = "./tests/test1.config"
        self.cfg_file_name_2 = "./tests/test2.config"
        self.ref_values_1 = [('section1', 'option1', 'value1'),
                             ('section1', 'option2', 'value2'),
                             ('section2', 'option1', 'value1'),
                             ('section2', 'option2', 'value2'),
                             ('section3', 'option1', 'value1'),
                             ('section3', 'option2', 'value2')]
        self.ref_values_2 = [('section1', 'option1', 'value1'),
                             ('section1', 'option2', 'value2'),
                             ('section2', 'option1', 'value1'),
                             ('section2', 'option2', 'value2'),
                             ('section3', 'option1', 'value1'),
                             ('section3', 'option2', 'value2'),
                             ('section3', 'option3', 'value3')]
        self.section = "section3"
        self.options_1 = ["option1", "option2"]
        self.values_1 = ["value1", "value2"]
        self.options_2 = ["option3"]
        self.values_2 = ["value3"]
        self.config_1 = ConfigParser.SafeConfigParser()
        self.config_1.read("tests/test1.config")
        self.config_2 = ConfigParser.SafeConfigParser()
        self.config_2.read("tests/test2.config")

    def test_set_config_new(self):
        """
        Test if configuration is properly set in the config file with complete
        section replacement.
        """
        utilities.set_config(filename=self.cfg_file_name_1,
                             section=self.section,
                             options=self.options_1,
                             values=self.values_1,
                             clean=True)
        self.test_values = []
        for s in self.config_1.sections():
            for o in self.config_1.options(s):
                self.test_values.append((s, o, self.config_1.get(s, o)))
        self.assertEqual(self.ref_values_1, self.test_values)

    def test_set_config_append_and_overwrite(self):
        """
        Test if configuration is properly set in the config file with just
        appending existing section with new options.
        """
        for i in range(2):
            utilities.set_config(filename=self.cfg_file_name_2,
                                 section=self.section,
                                 options=self.options_2,
                                 values=self.values_2)
            self.test_values = []
            for s in self.config_2.sections():
                for o in self.config_2.options(s):
                    self.test_values.append((s, o, self.config_2.get(s, o)))
            self.assertEqual(self.ref_values_2, self.test_values)
