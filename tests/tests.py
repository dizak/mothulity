
from __future__ import print_function
import six
import unittest
from six.moves import configparser
import subprocess as sp
from mothulity import utilities
import pandas as pd


class PathTests(unittest.TestCase):
    """
    Tests of the $PATH system variable.
    """
    def test_mothulity_path(self):
        """
        Tests if mothulity is in the system $PATH variable.
        """
        self.assertEqual(sp.check_output(["which", "mothulity"]).decode('utf-8').strip().split("/")[-1],
                         "mothulity")

    def test_mothulity_dbaser_path(self):
        """
        Tests if mothulity_dbaser is in the system $PATH variable.
        """
        self.assertEqual(sp.check_output(["which", "mothulity_dbaser"]).decode('utf-8').strip().split("/")[-1],
                         "mothulity_dbaser")

    def test_mothulity_draw_path(self):
        """
        Tests if mothulity_draw is in the system $PATH variable.
        """
        self.assertEqual(sp.check_output(["which", "mothulity_draw"]).decode('utf-8').strip().split("/")[-1],
                         "mothulity_draw")

    def test_mothulity_fc_path(self):
        """
        Tests if mothulity_fc is in the system $PATH variable.
        """
        self.assertEqual(sp.check_output(["which", "mothulity_fc"]).decode('utf-8').strip().split("/")[-1],
                         "mothulity_fc")

    def test_mothur_path(self):
        """
        Tests if mothur is in the system $PATH variable.
        """
        self.assertEqual(sp.check_output(["which", "mothur"]).decode('utf-8').strip().split("/")[-1],
                         "mothur")


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
        self.config = configparser.ConfigParser()
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
        self.config_1 = configparser.ConfigParser()
        self.config_1.read("tests/test1.config")
        self.config_2 = configparser.ConfigParser()
        self.config_2.read("tests/test2.config")

        self.ref_tax_summary_df = pd.read_csv(
            'test_data/utilities/ref_daughter_df.csv',
            sep='\t',
            index_col=[0],
        )
        print(self.ref_tax_summary_df)
        self.tax_summary_path = 'test_data/analysis/mltp_smpl/shared_tax/travis_job.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.agc.unique_list.0.03.pick.0.03.cons.tax.summary'
        self.tax_summary_df = pd.read_csv(self.tax_summary_path, sep='\t')
        self.mother_taxon = 'Actinobacteria'
        self.mother_rank = '0.1.1.1' 
        self.tax_level = 3

    def test_get_daughter_df(self):
        """
        Test if daughter taxa are propely selected from the pandas.DataFrame
        representing the tax.summary file.
        """
        pd.testing.assert_frame_equal(
            self.ref_tax_summary_df,
            utilities.get_daughter_df(
                self.tax_summary_df,
                self.mother_taxon,
                self.mother_rank,
                self.tax_level,
            ),
        )
