try:
    from xmcd_parser.ast.ast import *
except ImportError:
    from ast.ast import *

operators = {
    'div': lambda el, s: DivNode(operator_name='div', expression_list=el, scope=s),
    'mult': lambda el, s: MultNode(operator_name='mult', expression_list=el, scope=s),
    'plus': lambda el, s: PlusNode(operator_name='plus', expression_list=el, scope=s),
    'minus': lambda el, s: MinusNode(operator_name='minus', expression_list=el, scope=s),
    'pow': lambda el, s: PowNode(operator_name='pow', expression_list=el, scope=s),
    'min': lambda el, s: MinNode(operator_name='div', expression_list=el, scope=s),
    'max': lambda el, s: MaxNode(operator_name='max', expression_list=el, scope=s),
    'sqrt': lambda el, s: SqrtNode(operator_name='sqrt', expression_list=el, scope=s),
    'lessOrEqual': lambda el, s: LessOrEqualNode(operator_name='less_or_equal', expression_list=el, scope=s),
    'lessThan': lambda el, s: LessOrEqualNode(operator_name='less_than', expression_list=el, scope=s),
    'greaterThan': lambda el, s: GreaterThanNode(operator_name='greater_than', expression_list=el, scope=s),
}


def _literal(el, scope):
    # Currently only converts to FloatNode
    # TODO: Find if there are more 'literal' values such as true, false, <string>, etc
    return FloatNode(raw_text=el.text, xml_attr=el.attrib, scope=scope)


def _identifier(el, scope):
    return IdNode(raw_text=el.text, xml_attr=el.attrib, scope=scope)


def _instruction(els, scope):
    # This refers to <apply>
    op = els[0]
    # Removing namespace
    tag = op.tag.split('}')[1]
    if tag == 'id':
        tag = op.text
    el_list = []
    for el in els[1:]:
        if 'sequence' in el.tag:
            el_list += el.getchildren()
        else:
            el_list.append(el)
    return operators[tag]([adaptor(el, scope) for el in el_list], scope)


def _cond_instruction(els, scope):
    # IfThen nodes etc
    cond = els[0]
    expr = els[1]
    return IfThenNode(scope=scope, cond=adaptor(cond, scope), expr=adaptor(expr, scope))


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
    if 'ifThen' in el.tag:
        return _cond_instruction(el.getchildren(), scope)
    # List of instructions
    if 'program' in el.tag:
        return [adaptor(e, scope) for e in el.getchildren()]
