class ExpressionNode(object):
    """
    Abstract class from which all nodes inherits from
    """

    def __init__(self, *args, **kwargs):
        self.raw_text = kwargs.get('raw_text', '')
        self.xml_attr = kwargs.get('xml_attr', {})
        self.scope = kwargs.get('scope', {})

    def eval(self, *args, **kwargs):
        pass

    def str_tree(self, depth):
        pass


class InstructionNode(ExpressionNode):
    """
    Expression that returns a value
    """
    pass


class IfThenNode(InstructionNode):
    def __init__(self, *args, **kwargs):
        super(IfThenNode, self).__init__(*args, **kwargs)
        self.cond = kwargs.get('cond', None)
        self.expr = kwargs.get('expr', None)

    def eval(self, *args, **kwargs):
        super(IfThenNode, self).eval(*args, **kwargs)
        cond_value = self.cond.bool_eval()
        # if the condition was True, then we evaluate the expression
        # and return its value as result, otherwise we return False
        if cond_value:
            return self.expr.eval()
        return False


class OperatorNode(InstructionNode):
    def __init__(self, *args, **kwargs):
        super(OperatorNode, self).__init__(*args, **kwargs)
        self.operator_name = kwargs.get('operator_name', None)
        self.expression_list = kwargs.get('expression_list', [])
        self.op_func = None

    def str_tree(self, depth):
        result = '{2}<{0}>: {1}'.format(self.operator_name + 'Node',
                                        self.eval(),
                                        '\t' * depth)
        for e in self.expression_list:
            result += '\n{0}'.format(e.str_tree(depth + 1))
        return result

    def eval(self, *args, **kwargs):
        super(OperatorNode, self).eval(*args, **kwargs)
        return reduce(self.op_func, [e.eval() for e in self.expression_list])


class IdNode(ExpressionNode):
    def __init__(self, *args, **kwargs):
        super(IdNode, self).__init__(*args, **kwargs)
        self.id = self.get_id()

    def str_tree(self, depth):
        return '{2}<{0}>: "{1}"'.format(self.__class__.__name__,
                                        self.id,
                                        '\t' * depth)

    def eval(self, *args, **kwargs):
        super(IdNode, self).eval(*args, **kwargs)
        value = self.scope.get(self.id, None)
        if not value:
            raise ValueError('{0} has no value for {1}'.format(type(self), self.id))
        return value

    def get_id(self, *args, **kwargs):
        id = self.raw_text or 'UNKNOWN'
        if 'subscript' in self.xml_attr:
            return '{0}_{1}'.format(id, self.xml_attr['subscript'])
        return id


class MinNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(MinNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: min(x, y)


class MaxNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(MaxNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: max(x, y)


class DivNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(DivNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: x / y


class MultNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(MultNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: x * y


class PlusNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(PlusNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: x + y


class MinusNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(MinusNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: x - y


class PowNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(PowNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: x ** y


class SqrtNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(SqrtNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, _: x ** (1 / 2.)


class ComparisonOperator(OperatorNode):
    def eval(self, *args, **kwargs):
        return self.expression_list[-1].eval()

    def bool_eval(self, *args, **kwargs):
        return super(ComparisonOperator, self).eval(*args, **kwargs)


class LessOrEqualNode(ComparisonOperator):
    def __init__(self, *args, **kwargs):
        super(LessOrEqualNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: x <= y


class LessThanNode(ComparisonOperator):
    def __init__(self, *args, **kwargs):
        super(LessThanNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: x < y


class GreaterThanNode(ComparisonOperator):
    def __init__(self, *args, **kwargs):
        super(GreaterThanNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: x > y


class LiteralNode(ExpressionNode):
    pass


class FloatNode(LiteralNode):
    def str_tree(self, depth):
        return '{2}<{0}>: {1}'.format(self.__class__.__name__,
                                      self.eval(),
                                      '\t' * depth)

    def eval(self, *args, **kwargs):
        super(FloatNode, self).eval(*args, **kwargs)
        return float(self.raw_text)


class AssignmentNode(ExpressionNode):
    """
    Base class for assignments/definitions etc
    """

    left = None
    body = None


class DefinitionNode(AssignmentNode):
    def __init__(self, *args, **kwargs):
        super(DefinitionNode, self).__init__(*args, **kwargs)
        self.left = kwargs.get('left', None)
        self.body = kwargs.get('body', None)

    def str_tree(self, depth):
        return '{4}<{0}>: {1}\n{2}\n{3}'.format(self.__class__.__name__,
                                                self.eval(),
                                                self.left.str_tree(depth + 1),
                                                self.body.str_tree(depth + 1),
                                                '\t' * depth)

    def eval(self, *args, **kwargs):
        super(DefinitionNode, self).eval(*args, **kwargs)
        # Assuming IdNode
        id = self.left.id
        b = self.body
        if type(b) is list:
            # Get the first element that has a value
            # TODO: Find Lazy Evaluation solution
            value = next(v for v in [n.eval() for n in b] if v)
        else:
            value = b.eval()
        self.scope[id] = value
        # Return evaluation
        return value
