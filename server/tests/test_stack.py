import unittest
from dtypes.stack import Stack


class TestStack(unittest.TestCase):
    def test_basic_stack_operations(self):

        """Test basic push, pop, peek operations"""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        self.assertEqual(str(stack), "Stack([1, 2])")
        self.assertEqual(stack.peek(), 2)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(str(stack), "Stack([1])")

    def test_arithmetic_operations(self):
        """Test ADD, SUB, MULT, DIV operations"""
        # Test ADD
        stack = Stack()
        stack.execute_instructions("5 3 ADD")
        self.assertEqual(str(stack), "Stack([8])")

        # Test SUB
        stack.execute_instructions("10 4 SUB")
        self.assertEqual(str(stack), "Stack([8, 6])")

        # Test MULT
        stack.execute_instructions("3 4 MULT")
        self.assertEqual(str(stack), "Stack([8, 6, 12])")

        # Test DIV
        stack.execute_instructions("10 2 DIV")
        self.assertEqual(str(stack), "Stack([8, 6, 12, 5.0])")  # Updated to expect float

        # Test DIV with non-integer result
        stack = Stack()  # Reset stack
        stack.execute_instructions("5 2 DIV")
        self.assertEqual(str(stack), "Stack([2.5])")  # Test non-integer division

    def test_comparison_operations(self):
        """Test LT, GT, EQ operations"""
        # Test LT
        stack = Stack()
        stack.execute_instructions("5 10 LT")
        self.assertEqual(str(stack), "Stack([1])")  # 5 < 10 is true (1)

        # Test GT
        stack.execute_instructions("15 10 GT")
        self.assertEqual(str(stack), "Stack([1, 1])")  # 15 > 10 is true (1)

        # Test EQ
        stack.execute_instructions("10 10 EQ")
        self.assertEqual(str(stack), "Stack([1, 1, 1])")  # 10 == 10 is true (1)

    def test_print_operation(self):
        """Test PRINT operation and print capture"""
        stack = Stack()
        stack.execute_instructions("42 PRINT")
        self.assertEqual(stack.prints, [42])
        self.assertEqual(str(stack), "Stack([])")

    def test_for_loop(self):
        """Test FOR loop with print"""
        stack = Stack()
        stack.execute_instructions("1 5 1 FOR DUP PRINT END")
        self.assertEqual(stack.prints, [1, 2, 3, 4, 5])
        self.assertEqual(str(stack), "Stack([1, 2, 3, 4, 5])")

    def test_while_loop(self):
        """Test WHILE loop with print"""
        stack = Stack()
        stack.execute_instructions("1 WHILE DUP 5 LT DO DUP PRINT 1 ADD END")
        self.assertEqual(stack.prints, [1, 2, 3, 4])
        self.assertEqual(str(stack), "Stack([5])")

    def test_if_else_construct(self):
        """Test IF/ELSE construct with both branches"""
        # Test true branch
        stack = Stack()  # Reset stack
        stack.execute_instructions("5 10 LT IF THEN 42 PRINT ELSE 24 PRINT END")
        self.assertEqual(stack.prints, [42])

        # Test false branch
        stack = Stack()  # Reset stack
        stack.execute_instructions("15 10 LT IF THEN 42 PRINT ELSE 24 PRINT END")
        self.assertEqual(stack.prints, [24])

    def test_complex_program(self):
        """Test complex program combining multiple features"""
        program = """
        10 DUP 5 LT IF THEN
            WHILE DUP 10 LT DO DUP PRINT 1 ADD END
        ELSE
            1 10 2 FOR DUP PRINT END
        END
        """
        stack = Stack()
        stack.execute_instructions(program)
        # Since 10 is not less than 5, it should execute the ELSE branch
        # which prints odd numbers from 1 to 9
        self.assertEqual(stack.prints, [1, 3, 5, 7, 9])
        self.assertEqual(str(stack), "Stack([10, 1, 3, 5, 7, 9])")

    def test_error_handling(self):
        """Test error cases"""
        # Test pop from empty stack
        stack = Stack()
        with self.assertRaises(IndexError):
            stack.pop()

        # Test division by zero
        with self.assertRaises(ZeroDivisionError):
            stack.execute_instructions("1 0 DIV")

        # Clear Stack
        stack = Stack()

        # Test insufficient operands
        with self.assertRaises(ValueError):
            stack.execute_instructions("1 ADD")  # ADD needs two operands

        # Test invalid command
        with self.assertRaises(ValueError):
            stack.execute_instructions("INVALID")

        # Test missing THEN in IF
        with self.assertRaises(SyntaxError):
            stack.execute_instructions("1 IF 2 END")

        # Test missing END in FOR
        with self.assertRaises(SyntaxError):
            stack.execute_instructions("1 5 1 FOR PRINT")


if __name__ == '__main__':
    unittest.main()
