from generate import *
import unittest
import copy
import os


class TestCrossword():
    @staticmethod
    def get_crossword():
        structure_path = os.path.join('data', 'structure0.txt')
        words_path = os.path.join('data', 'words0.txt')
        crossword = Crossword(structure_path, words_path)
        return CrosswordCreator(crossword)


class TestEnforceNodeConsistency(unittest.TestCase):
    def setUp(self):
        self.creator = TestCrossword.get_crossword()

    def test_enforce_node_consistency(self):
        self.creator.enforce_node_consistency()
        expected_result = {
            Variable(1, 4, 'down', 4): {'FOUR', 'NINE', 'FIVE'}, 
            Variable(0, 1, 'across', 3): {'TWO', 'SIX', 'ONE', 'TEN'}, 
            Variable(4, 1, 'across', 4): {'FOUR', 'NINE', 'FIVE'}, 
            Variable(0, 1, 'down', 5): {'SEVEN', 'EIGHT', 'THREE'}
        }
        self.assertEqual(self.creator.domains, expected_result)


class TestRevise(unittest.TestCase):
    def setUp(self):
        self.creator = TestCrossword.get_crossword()
        self.creator.enforce_node_consistency()
        self.x = Variable(0, 1, 'across', 3)
        self.y = Variable(0, 1, 'down', 5)

    def test_revise_return_value(self):
        self.assertTrue(self.creator.revise(self.x, self.y))

    def test_revise_domains(self):
        self.creator.revise(self.x, self.y)
        actual_result = {
            self.x: self.creator.domains[self.x],
            self.y: self.creator.domains[self.y],
        }
        expected_result = {
            Variable(0, 1, 'across', 3): {'SIX', 'TWO', 'TEN'}, 
            Variable(0, 1, 'down', 5): {'SEVEN', 'EIGHT', 'THREE'}
        }
        self.assertEqual(actual_result, expected_result)


class TestAC3(unittest.TestCase):
    def setUp(self):
        self.creator = TestCrossword.get_crossword()

    def test_ac3_return_value(self):
        self.assertTrue(self.creator.ac3())

    def test_ac3_upated_domains(self):
        self.creator.ac3()
        expected_result =  {
            Variable(1, 4, 'down', 4): {'FIVE', 'NINE'}, 
            Variable(0, 1, 'across', 3): {'SIX'}, 
            Variable(4, 1, 'across', 4): {'NINE'}, 
            Variable(0, 1, 'down', 5): {'SEVEN'}
        }
        self.assertEqual(self.creator.domains, expected_result)


class TestAssignmentComplete(unittest.TestCase):
    def setUp(self):
        self.creator = TestCrossword.get_crossword()
        self.creator.ac3()

    def test_assignment_complete_true(self):
        self.assertTrue(
            self.creator.assignment_complete(self.creator.domains)
        )

    def test_assignment_complete_false(self):
        self.creator.domains[Variable(0, 1, 'down', 5)] = None
        self.assertFalse(
            self.creator.assignment_complete(self.creator.domains)
        )


class TestConsistent(unittest.TestCase):
    def setUp(self):
        self.creator = TestCrossword.get_crossword()
        self.creator.ac3()

    def test_consistent_true(self):
        assignment =  {
            Variable(1, 4, 'down', 4): 'FIVE', 
            Variable(0, 1, 'across', 3): 'SIX',
        }
        self.assertTrue(self.creator.consistent(assignment))

    def test_consistent_true(self):
        assignment =  {
            Variable(1, 4, 'down', 4): 'FIVE', 
            Variable(0, 1, 'across', 3): 'FIVE',
        }
        self.assertFalse(self.creator.consistent(assignment))


class TestOrderDomainValues(unittest.TestCase):
    def setUp(self):
        self.creator = TestCrossword.get_crossword()
        self.creator.ac3()

    def test_order_domain_values(self):
        var = Variable(4, 1, 'across', 4) 
        self.creator.domains[var] = {'NINE', 'FIVE'}
        assignment = {Variable(0, 1, 'across', 3): 'SIX'}
        expected_result = ['NINE', 'FIVE']
        self.assertEqual(
            self.creator.order_domain_values(var, assignment), expected_result
        )


class TestSelectUnassignedVariable(unittest.TestCase):
    def setUp(self):
        self.creator = TestCrossword.get_crossword()
        self.creator.ac3()

    def test_order_domain_values(self):
        assignment = {Variable(4, 1, 'across', 4): 'NINE'}
        expected_result = Variable(0, 1, 'down', 5)

        self.assertEqual(
            self.creator.select_unassigned_variable(assignment), expected_result
        )


class TestBacktrack(unittest.TestCase):
    def setUp(self):
        self.creator = TestCrossword.get_crossword()
        self.creator.ac3()

    def test_backtrack(self):
        assignment = {Variable(4, 1, 'across', 4): 'NINE'}
        expected_result = {
            Variable(1, 4, 'down', 4): 'FIVE', 
            Variable(0, 1, 'across', 3): 'SIX', 
            Variable(4, 1, 'across', 4): 'NINE', 
            Variable(0, 1, 'down', 5): 'SEVEN'
        }

        self.assertEqual(
            self.creator.backtrack(assignment), expected_result
        )


if __name__ == '__main__':
    unittest.main()