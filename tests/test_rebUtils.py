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
        self.assertEqual(results['Idle_Current'], '15/15 values okay.')
        self.assertEqual(results['CS_Gate_Test'], 'Gain: 20.512 Offset: 78.811')
        self.assertEqual(results['ASPIC_Noise_Tests'],
                         '144/144 channels OK failcount: 0/0/0')

if __name__ == '__main__':
    unittest.main()

