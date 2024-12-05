class Stack:
    """A simple stack implementation."""
    commands: dict

    def __init__(self):
        self.stack = []
        self.prints = []
        self.commands = {
            "PUSH": self.push,
            "POP": self.pop,
            "PRINT": self.print_pop,
            "ADD": self.add,
            "SUB": self.sub,
            "MULT": self.mult,
            "DIV": self.div,
            "DUP": self.dup,
            "LT": self.lt,
            "GT": self.gt,
            "EQ": self.eq,
        }

    # Helper Methods
    def size(self):
        """Return the number of elements on the stack."""
        return len(self.stack)

    # Stack Operations
    def push(self, value):
        """Add a value to the top of the stack."""
        self.stack.append(value)

    def pop(self):
        """Remove and return the top element of the stack."""
        if not self.stack:
            raise IndexError("Pop from empty stack")
        return self.stack.pop()

    def peek(self):
        """Return the top element of the stack without removing it."""
        if not self.stack:
            raise IndexError("Peek from empty stack")
        return self.stack[-1]

    def dup(self):
        """Duplicate the top element of the stack."""
        self.push(self.peek())

    def print_pop(self):
        """Pop and print the top element of the stack."""
        res = self.pop()
        self.prints.append(res)
        print(res)

    # Arithmetic Operations
    def add(self):
        """Pop the top two elements (a, b) and push a + b onto the stack."""
        if self.size() < 2:
            raise ValueError("Not enough elements on the stack for addition")
        b = self.pop()
        a = self.pop()
        self.push(a + b)

    def sub(self):
        """Pop the top two elements (a, b) and push a - b onto the stack."""
        if self.size() < 2:
            raise ValueError("Not enough elements on the stack for subtraction")
        b = self.pop()
        a = self.pop()
        self.push(a - b)

    def mult(self):
        """Pop the top two elements (a, b) and push a * b onto the stack."""
        if self.size() < 2:
            raise ValueError("Not enough elements on the stack for multiplication")
        b = self.pop()
        a = self.pop()
        self.push(a * b)

    def div(self):
        """Pop the top two elements (a, b) and push a / b onto the stack."""
        if self.size() < 2:
            raise ValueError("Not enough elements on the stack for division")
        b = self.pop()
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        a = self.pop()
        self.push(a / b)

    # Comparison Operations
    def lt(self):
        """Pop the top two elements (a, b) and push 1 if a < b, else push 0."""
        if self.size() < 2:
            raise ValueError("Not enough elements on the stack for comparison")
        b = self.pop()
        a = self.pop()
        self.push(1 if a < b else 0)

    def gt(self):
        """Pop the top two elements (a, b) and push 1 if a > b, else push 0."""
        if self.size() < 2:
            raise ValueError("Not enough elements on the stack for comparison")
        b = self.pop()
        a = self.pop()
        self.push(1 if a > b else 0)

    def eq(self):
        """Pop the top two elements and push 1 if a == b, else push 0."""
        if self.size() < 2:
            raise ValueError("Not enough elements on the stack for comparison")
        b = self.pop()
        a = self.pop()
        self.push(1 if a == b else 0)

    # Conditional Operations
    def if_else(self, condition: list, true_body: list, false_body: list):
        """Handle an if/else condition.
        IF <condition> THEN <true_body> ELSE <false_body> END
        10 DUP 5 LT IF
            WHILE DUP 10 LT DO DUP PRINT 1 ADD END
        ELSE
            1 10 2 FOR DUP PRINT END
        END
        If the top of the stack is less than 5, print 1, 2, 3, 4
        Otherwise, print 1, 3, 5, 7, 9
        Prints: 1, 3, 5, 7, 9
        """
        # Evaluate the condition
        for command in condition:
            self.execute_command(command)

        # Check the result of the condition
        if self.pop():  # if true (non-zero), execute the true_body
            for command in true_body:
                self.execute_command(command)
        else:  # if false (zero), execute the false_body
            for command in false_body:
                self.execute_command(command)

    # Loops
    def for_loop(self, instructions: list):
        """Handle a for loop, iterating based on stack parameters.
        FOR <start> <end> <step> DO <body> END
        1 10 2 FOR DUP PRINT END
        For loop from 1 to 10 with step 2.
        Print 1, 3, 5, 7, 9
        """
        if self.size() < 3:
            raise ValueError("Stack must have start, end, and step values for the loop")

        step = self.pop()
        end = self.pop()
        start = self.pop()

        current = start
        while (step > 0 and current <= end) or (step < 0 and current >= end):
            self.push(current)  # push the loop variable onto the stack
            for command in instructions:
                self.execute_command(command)
            current += step

    def while_loop(self, condition: list, body: list):
        """Handle a while loop, executing the body while the condition evaluates to true.
        WHILE <condition> DO <body> END
        1 WHILE DUP 10 LT DO DUP PRINT 1 ADD END
        While stack top is less than 10, print and increment by 1 (1, 2, 3, ..., 9)
        """
        while True:
            # evaluate the condition
            for command in condition:
                self.execute_command(command)

            # check the result of the condition
            if not self.pop():  # if the top value is 0 (false), exit the loop
                break

            # execute the loop body
            for command in body:
                self.execute_command(command)


    # Execute Operations (Not For / While Loops)
    def execute_command(self, command):
        """Dynamically execute a command using the commands' dictionary.
        If instruction is a number, push it onto the stack.
        Otherwise, execute the corresponding method from the commands' dictionary.
        Handles ADD, SUB, MULT, DIV, DUP, POP, PRINT, LT, GT, EQ, etc.
        Does not handle loops (FOR, WHILE) or conditional flows (IF ELSE), use execute_instructions for that.
        """
        if command.isdigit():
            self.push(int(command))
        elif command in self.commands:
            self.commands[command]()  # call the corresponding method
        else:
            raise ValueError(f"Unknown command: {command}")

    # Parse and Execute Instructions
    def execute_instructions(self, text):
        tokens = text.split()
        i = 0

        while i < len(tokens):
            token = tokens[i]

            # Handle IF/ELSE
            if token == "IF":
                condition = []
                true_body = []
                false_body = []

                # Parse the condition
                i += 1
                while i < len(tokens) and tokens[i] != "THEN":
                    condition.append(tokens[i])
                    i += 1
                    if i >= len(tokens):
                        raise SyntaxError("Missing THEN in IF construct")

                # Move past THEN
                i += 1

                # Parse the true body until we hit ELSE or END
                while i < len(tokens) and tokens[i] not in ["ELSE", "END"]:
                    true_body.append(tokens[i])
                    i += 1

                # Check for ELSE
                if i < len(tokens) and tokens[i] == "ELSE":
                    i += 1  # Move past ELSE
                    # Parse the false body until END
                    while i < len(tokens) and tokens[i] != "END":
                        false_body.append(tokens[i])
                        i += 1

                if i >= len(tokens) or tokens[i] != "END":
                    raise SyntaxError("Missing END in IF construct")

                # Execute the if/else block
                self.if_else(condition, true_body, false_body)
                i += 1  # Move past END

            # Handle WHILE Loop
            elif token == "WHILE":
                condition = []
                body = []

                # Parse the condition
                i += 1
                while i < len(tokens) and tokens[i] != "DO":
                    condition.append(tokens[i])
                    i += 1
                    if i >= len(tokens):
                        raise SyntaxError("Missing DO in WHILE construct")

                # Parse the loop body
                i += 1  # move past "DO"
                while i < len(tokens) and tokens[i] != "END":
                    body.append(tokens[i])
                    i += 1
                    if i >= len(tokens):
                        raise SyntaxError("Missing END in WHILE construct")

                if tokens[i] != "END":
                    raise SyntaxError("Missing END in WHILE construct")

                # Execute the while loop
                self.while_loop(condition, body)
                i += 1  # Move past END

            # Handle FOR Loop
            elif token == "FOR":
                loop_body = []

                i += 1  # move past "FOR"
                while i < len(tokens) and tokens[i] != "END":
                    loop_body.append(tokens[i])
                    i += 1
                    if i >= len(tokens):
                        raise SyntaxError("Missing END in FOR construct")

                if tokens[i] != "END":
                    raise SyntaxError("Missing END in FOR construct")

                # Execute the for loop
                self.for_loop(loop_body)
                i += 1  # Move past END

            # Handle other commands
            else:
                if token not in ["THEN", "ELSE", "END", "DO"]:  # Skip special keywords
                    self.execute_command(token)
                i += 1

    def __str__(self):
        return f"Stack({self.stack})"
