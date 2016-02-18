# coding=utf-8
from ast.ast import LiteralNode, IdNode, StrNode
from base import ASTRender


class AsciiMathRender(ASTRender):
    def __init__(self, *args, **kwargs):
        ASTRender.__init__(self, *args, **kwargs)
        self.func_symbols = {
            'sqrt': 'sqrt',
            'cot': 'cot',
            'tan': 'tan',
            'cos': 'cos',
            'sin': 'sin',
            'neg': 'neg',
            'absval': 'abs',
            'min': 'min',
            'max': 'max',
        }
        self.operator_symbols = {
            'div': '/',
            'mult': '*',
            'plus': '+',
            'minus': '-',
            'pow': '^',
            'less_or_equal': '<=',
            'greater_or_equal': '>=',
            'less_than': '<',
            'greater_than': '>',
            'equal': '=',
        }

    def _render_matrix_node(self, node):
        ASTRender._render_matrix_node(self, node)
        result = '['
        for row in node.np_matrix:
            inner = reduce(lambda x, y: '{0}, {1}'.format(x, y), [self._render_adaptor(el) for el in row])
            result += '[{0}]'.format(inner)
        result += ']'
        return result

    def _render_literal_node(self, node):
        ASTRender._render_literal_node(self, node)
        if isinstance(node, StrNode):
            return 'tt"\'{}\'"'.format(node.raw_text)
        return node.raw_text

    def _render_math_func_node(self, node):
        ASTRender._render_math_func_node(self, node)
        func = self.func_symbols[node.func_name]
        func += '({0})'.format(reduce(lambda x, y: '{0}, {1}'.format(x, y),
                                      [self._render_adaptor(el) for el in node.expression_list]))
        return func

    def _render_expression_list(self, node):
        super(AsciiMathRender, self)._render_expression_list(node)
        result = '{'
        l = len(node)
        for i in xrange(l - 1):
            result += '({0}),'.format(self._render_adaptor(node[i]))
        result += '({0}):}}'.format(self._render_adaptor(node[-1]))
        return result

    def _render_id_node(self, node):
        ASTRender._render_id_node(self, node)
        return node.id

    def _render_operator_node(self, node):
        ASTRender._render_operator_node(self, node)
        op = self.operator_symbols[node.operator_name]

        def str_func(n, str_n):
            return '{0}'.format(str_n) \
                if isinstance(n, LiteralNode) or isinstance(n, IdNode) \
                else '({0})'.format(str_n)

        result = reduce(
                lambda x, y: '{0} {1} {2}'.format(
                        str_func(x[0], x[1]), op, str_func(y[0], y[1])),
                [(el, self._render_adaptor(el)) for el in node.expression_list])

        return result

    def _render_if_then_else_node(self, node):
        ASTRender._render_if_then_else_node(self, node)
        result = '{0} if {1}{2}'.format(
                self._render_adaptor(node.then_expr),
                self._render_adaptor(node.cond),
                '  text(otherwise)  {}'.format(
                        self._render_adaptor(node.else_expr)) if node.else_expr else '')
        return result

    def _render_definition_node(self, node):
        ASTRender._render_definition_node(self, node)
        return '{0} := {1}'.format(self._render_adaptor(node.left), self._render_adaptor(node.body))
