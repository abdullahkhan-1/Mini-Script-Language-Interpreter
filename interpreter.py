from nodes import (NumberNode, StringNode, IdentNode, BinOpNode,
                   ConditionNode, LetNode, AssignNode, PrintNode,
                   IfNode, WhileNode, ForNode, FuncDefNode, FuncCallNode, ReturnNode)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.env       = {}
        self.functions = {}

    def run(self, statements):
        for stmt in statements:
            self.execute(stmt, self.env)

    def execute(self, node, env):
        if isinstance(node, LetNode):
            if node.name in env:
                raise NameError(f'Variable "{node.name}" already declared. Use assignment instead.')
            env[node.name] = self.evaluate(node.value, env)

        elif isinstance(node, AssignNode):
            if node.name not in env and node.name not in self.env:
                raise NameError(f'Variable "{node.name}" not declared. Use let first.')
            if node.name in env:
                env[node.name] = self.evaluate(node.value, env)
            else:
                self.env[node.name] = self.evaluate(node.value, env)

        elif isinstance(node, PrintNode):
            val = self.evaluate(node.value, env)
            if isinstance(val, float) and val.is_integer():
                print(int(val))
            else:
                print(val)

        elif isinstance(node, IfNode):
            if self.evaluate(node.condition, env):
                for stmt in node.body:
                    self.execute(stmt, env)
            elif node.else_body is not None:
                for stmt in node.else_body:
                    self.execute(stmt, env)

        elif isinstance(node, WhileNode):
            while self.evaluate(node.condition, env):
                for stmt in node.body:
                    self.execute(stmt, env)

        elif isinstance(node, ForNode):
            start = self.evaluate(node.start, env)
            end   = self.evaluate(node.end,   env)
            env[node.var] = start
            while env[node.var] <= end:
                for stmt in node.body:
                    self.execute(stmt, env)
                env[node.var] += 1

        elif isinstance(node, FuncDefNode):
            self.functions[node.name] = node

        elif isinstance(node, FuncCallNode):
            self.call_function(node, env)

        elif isinstance(node, ReturnNode):
            raise ReturnSignal(self.evaluate(node.value, env))

        else:
            raise RuntimeError(f'Unknown statement node: {type(node).__name__}')

    def evaluate(self, node, env):
        if isinstance(node, NumberNode):
            return node.value

        elif isinstance(node, StringNode):
            return node.value

        elif isinstance(node, IdentNode):
            if node.name in env:
                return env[node.name]
            if node.name in self.env:
                return self.env[node.name]
            raise NameError(f'Variable "{node.name}" is not defined.')

        elif isinstance(node, BinOpNode):
            left  = self.evaluate(node.left,  env)
            right = self.evaluate(node.right, env)
            if node.op == '+': return left + right
            if node.op == '-': return left - right
            if node.op == '*': return left * right
            if node.op == '/':
                if right == 0:
                    raise ZeroDivisionError('Cannot divide by zero.')
                return left / right

        elif isinstance(node, ConditionNode):
            left  = self.evaluate(node.left,  env)
            right = self.evaluate(node.right, env)
            if node.op == '>':  return left >  right
            if node.op == '<':  return left <  right
            if node.op == '>=': return left >= right
            if node.op == '<=': return left <= right
            if node.op == '==': return left == right
            if node.op == '!=': return left != right

        elif isinstance(node, FuncCallNode):
            return self.call_function(node, env)

        else:
            raise RuntimeError(f'Unknown expression node: {type(node).__name__}')

    def call_function(self, node, env):
        if node.name not in self.functions:
            raise NameError(f'Function "{node.name}" is not defined.')

        func = self.functions[node.name]

        if len(node.args) != len(func.params):
            raise TypeError(
                f'Function "{node.name}" expects {len(func.params)} argument(s), '
                f'got {len(node.args)}.'
            )

        local_env = {
            param: self.evaluate(arg, env)
            for param, arg in zip(func.params, node.args)
        }

        try:
            for stmt in func.body:
                self.execute(stmt, local_env)
        except ReturnSignal as ret:
            return ret.value

        return None