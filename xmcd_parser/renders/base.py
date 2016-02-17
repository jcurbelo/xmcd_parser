from ast.ast import *


class ASTRender(object):
    """
    Base class
    """
    operator_symbols = {}
    func_symbols = {}

    def __init__(self, *args, **kwargs):
        self.root = args[0]

    def render(self):
        return self._render_adaptor(self.root)

    def _render_adaptor(self, node):
        if isinstance(node, IdNode):
            return self._render_id_node(node)
        if isinstance(node, IfThenElseNode):
            return self._render_if_then_else_node(node)
        if isinstance(node, OperatorNode):
            return self._render_operator_node(node)
        if isinstance(node, MathFuncNode):
            return self._render_math_func_node(node)
        if isinstance(node, LiteralNode):
            return self._render_literal_node(node)
        if isinstance(node, MathFuncNode):
            return self._render_matrix_node(node)
        if isinstance(node, DefinitionNode):
            return self._render_definition_node(node)
        # list of expressions
        if type(node) is list:
            return self._render_expression_list(node)
        return ''

    def _render_if_then_else_node(self, node):
        pass

    def _render_operator_node(self, node):
        pass

    def _render_id_node(self, node):
        pass

    def _render_math_func_node(self, node):
        pass

    def _render_literal_node(self, node):
        pass

    def _render_matrix_node(self, node):
        pass

    def _render_definition_node(self, node):
        pass

    def _render_expression_list(self, node):
        pass
