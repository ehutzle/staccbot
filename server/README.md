# Staccbot

A Python Based API Server for interpreting and executing a stack based language.

### Commands:

- `PUSH <value>`: Pushes a value onto the stack.
- `POP`: Pops a value off the stack.
- `PRINT`: Pops a value off the stack and prints it to the console. (Also appends printed value to Stack object `prints`
  attribute)
- `ADD`: Pops two values off the stack, adds them together, and pushes the result back onto the stack.
- `SUB`: Pops two values off the stack, subtracts the first value popped from the second value popped, and pushes the
  result back onto the stack.
- `MUL`: Pops two values off the stack, multiplies them together, and pushes the result back onto the stack.
- `DIV`: Pops two values off the stack, divides the first value popped from the second value popped, and pushes the
  result back onto the stack.
- `DUP`: Duplicates the value on top of the stack.
- `LT`: Pops two values off the stack, compares them, and pushes 1 onto the stack if the second value popped is less
  than. 0 otherwise.
- `GT`: Pops two values off the stack, compares them, and pushes 1 onto the stack if the second value popped is greater.
  0 otherwise.
- `EQ`: Pops two values off the stack, compares them, and pushes 1 onto the stack if the two values popped are equal. 0
  otherwise.

### Conditional Logic:

- `IF`: IF `<condition>` THEN `<true_body>` ELSE `<false_body>` END
- `WHILE`: WHILE `<condition>` DO `<body>` END
- `FOR`: FOR `<start>` `<end>` `<step>` DO `<body>` END

### Example Instructions:

#### While stack top is less than 10, print and increment by 1 (1, 2, 3, ..., 9)

```python 
# While Loop With Conditional Logic
stack = Stack()
instructions = '10 DUP 5 LT IF THEN WHILE DUP 10 LT DO DUP PRINT 1 ADD END ELSE 1 10 2 FOR DUP PRINT END END'
stack.execute_instructions(instructions)
print(stack.prints)
> [1, 3, 5, 7, 9]
print(stack.stack)
> [10, 1, 3, 5, 7, 9]
```

#### For loop from 1 to 10, print each value

```python
# For Loop 
stack = Stack()
instructions = '1 10 1 FOR DUP PRINT END'
stack.execute_instructions(instructions)
print(stack.prints)
> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(stack.stack)
> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### Endpoints and Usage:

`/api/execute - POST`

##### body

```json
{
  "instructions": "10 DUP 5 LT IF THEN WHILE DUP 10 LT DO DUP PRINT 1 ADD END ELSE 1 10 2 FOR DUP PRINT END END"
}
```

##### return format

```json
{
  "prints": [
    1,
    3,
    5,
    7,
    9
  ],
  "final_stack": 'Stack([10, 1, 3, 5, 7, 9])',
  "status": "success"
}
```
