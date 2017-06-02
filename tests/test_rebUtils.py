"Unit tests for rebUtils module."
import os
import unittest
import rebUtils

class RebUtilsTestCase(unittest.TestCase):
    "TestCase class for rebUtils module."
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_REB5Test_results_file(self):
        "Unit test for parse_REB5Test_results_file function."
        infile = os.path.join(os.environ['REBTESTINGDIR'], 'tests',
                              'REB5_Test_17.04.26.15.50_0x18ed9a7b.txt')
        results = rebUtils.parse_REB5Test_results_file(infile)
        self.assertEqual(results['CCS_Path'], 'ccs-reb5-0')
        self.assertEqual(results['BoardID'], '0x18ed9a7b')
        self.assertEqual(results['Link_version'], '032')
        self.assertEqual(results['Parameter_Logging'], 'PASS')
        self.assertEqual(results['Idle_Current'], 'PASS')
        self.assertEqual(results['CS_Gate_Test'], 'PASS')
        self.assertEqual(results['ASPIC_Noise_Tests'], 'PASS')
        self.assertEqual(results['Diverging_PCK_Rails,_0V'], 'PASS')
        self.assertEqual(results['OG_Bias_Test'], 'FAIL')

    def test_check_REB_vivado_output(self):
        "Unit test for the check_REB_vivado_output function."
        infile = os.path.join(os.environ['REBTESTINGDIR'], 'tests',
                              'vivado_flash_success.log')
        rebUtils.check_REB_vivado_output(open(infile).readlines())

        infile = os.path.join(os.environ['REBTESTINGDIR'], 'tests',
                              'vivado_flash_failure.log')
        self.assertRaises(rebUtils.RebProgrammingError,
                          rebUtils.check_REB_vivado_output,
                          open(infile).readlines())

        expected_lines = ('End of startup status: HIGH',)

        infile = os.path.join(os.environ['REBTESTINGDIR'], 'tests',
                              'vivado_program_fpga_success.log')
        rebUtils.check_REB_vivado_output(open(infile).readlines(),
                                         expected=expected_lines)

        infile = os.path.join(os.environ['REBTESTINGDIR'], 'tests',
                              'vivado_program_fpga_failure.log')
        self.assertRaises(rebUtils.RebProgrammingError,
                          rebUtils.check_REB_vivado_output,
                          open(infile).readlines(),
                          expected=expected_lines)

if __name__ == '__main__':
    unittest.main()

