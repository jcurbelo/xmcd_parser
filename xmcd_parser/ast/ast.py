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


class InstructionNode(ExpressionNode):
    pass


class OperatorNode(ExpressionNode):
    def __init__(self, *args, **kwargs):
        super(OperatorNode, self).__init__(*args, **kwargs)
        self.operator_name = kwargs.get('operator_name', None)
        self.expression_list = kwargs.get('expression_list', [])
        self.op_func = None

    def eval(self, *args, **kwargs):
        super(OperatorNode, self).eval(*args, **kwargs)
        return reduce(self.op_func, [e.eval() for e in self.expression_list])


class IdNode(ExpressionNode):
    def __init__(self, *args, **kwargs):
        super(IdNode, self).__init__(*args, **kwargs)
        self.id = self.get_id()

    def eval(self, *args, **kwargs):
        super(IdNode, self).eval(*args, **kwargs)
        return self.scope.get(self.id, None)

    def get_id(self, *args, **kwargs):
        id = self.raw_text or 'UNKNOWN'
        if 'subscript' in self.xml_attr:
            return '{0}_{1}'.format(id, self.xml_attr['subscript'])
        return id


class MinNode(OperatorNode):
    def __init__(self, *args, **kwargs):
        super(MinNode, self).__init__(*args, **kwargs)
        self.op_func = lambda x, y: min(x, y)


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


class LiteralNode(ExpressionNode):
    pass


class FloatNode(LiteralNode):
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

    def eval(self, *args, **kwargs):
        super(DefinitionNode, self).eval(*args, **kwargs)
        # Assuming IdNode
        id = self.left.id
        value = self.body.eval()
        self.scope[id] = value
        # Return evaluation
        return value
