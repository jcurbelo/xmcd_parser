from xmcd_parser.ast.ast import *


keywords = {
    'min': lambda rt, xa, s: MinNode(raw_text=rt, xml_attr=xa, scope=s)
}

operators = {
    'div': lambda el, s: DivNode(operator_name='div', expression_list=el, scope=s),
    'mult': lambda el, s: MultNode(operator_name='mult', expression_list=el, scope=s),
    'plus': lambda el, s: PlusNode(operator_name='plus', expression_list=el, scope=s),
    'minus': lambda el, s: MinusNode(operator_name='minus', expression_list=el, scope=s),
    'pow': lambda el, s: PowNode(operator_name='pow', expression_list=el, scope=s),
}


def _literal(el, scope):
    # Currently only converts to FloatNode
    # TODO: Find if there are more 'literal' values such as true, false, <string>, etc
    return FloatNode(raw_text=el.text, xml_attr=el.attrib, scope=scope)


def _identifier(el, scope):
    default = lambda rt, xa, s: IdNode(raw_text=rt, xml_attr=xa, scope=s)
    return keywords.get(el.text, default)(el.text, el.attrib, scope)


def _instruction(els, scope):
    # This refers to <apply>
    op = els[0]
    # Removing namespace
    op = op.tag.split('}')[1]
    return operators[op]([adaptor(el, scope) for el in els[1:]], scope)


def _definition(els, scope):
    left = els[0]
    body = els[1]
    return DefinitionNode(scope=scope, left=adaptor(left, scope), body=adaptor(body, scope))


def adaptor(el, scope):
    if 'real' in el.tag:
        return _literal(el, scope)
    if 'id' in el.tag:
        return _identifier(el, scope)
    if 'define' in el.tag:
        return _definition(el.getchildren(), scope)
    if 'apply' in el.tag:
        return _instruction(el.getchildren(), scope)
    if 'parens' in el.tag:
        return adaptor(el.getchildren()[0], scope)
