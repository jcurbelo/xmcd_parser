from xmcd_parser.ast.ast import *

unwanted_keys = [
    '@xmlns:ml',
    '@placeholderMultiplicationStyle',
    '@xmlns',
    '@disable-calc',
    '@optimize',
    '@xml:space',
]

keywords = {
    'min': lambda rt, xa, s: MinNode(raw_text=rt, xml_attr=xa, scope=s)
}

operators = {
    'ml:div': lambda el, s: DivNode(operator_name='div', expression_list=el, scope=s),
    'ml:mult': lambda el, s: MultNode(operator_name='mult', expression_list=el, scope=s),
    'ml:plus': lambda el, s: PlusNode(operator_name='plus', expression_list=el, scope=s),
    'ml:minus': lambda el, s: MinusNode(operator_name='minus', expression_list=el, scope=s),
    'ml:pow': lambda el, s: PowNode(operator_name='pow', expression_list=el, scope=s),
}


def _clean_dict(dict):
    for uk in unwanted_keys:
        if uk in dict:
            del dict[uk]


def _literal(dict, scope):
    if 'ml:real' in dict:
        lst = dict['ml:real']
        if type(lst) == list:
            return [FloatNode(raw_text=l, scope=scope) for l in lst]
        return FloatNode(raw_text=lst, scope=scope)


def _identifier(dict, scope):
    lst = dict['ml:id']
    if type(lst) == list:
        return [IdNode(raw_text=l, xml_attr=l, scope=scope) for l in lst]
    text = lst['#text']
    default = lambda rt, xa, s: IdNode(raw_text=rt, xml_attr=xa, scope=s)
    return keywords.get(text, default)(lst['#text'], lst, scope)


def _instruction(dict, scope):
    inner_dict = dict['ml:apply'].copy()
    for k in operators.keys():
        if k in inner_dict:
            del inner_dict[k]
            elst = []
            for ik, v in inner_dict.iteritems():
                e = adaptor({ik: v}, scope)
                if type(e) == list:
                    elst += e
                else:
                    elst.append(e)
            return operators[k](elst, scope)


def _definition(dict, scope):
    inner_dict = dict['ml:define']
    left = {'ml:id': inner_dict['ml:id']}
    body = {}
    if 'ml:real' in inner_dict:
        body = {'ml:real': inner_dict['ml:real']}
    if 'ml:apply' in inner_dict:
        body = {'ml:apply': inner_dict['ml:apply']}
    return DefinitionNode(scope=scope, left=adaptor(left, scope), body=adaptor(body, scope))


def adaptor(dict, scope):
    _clean_dict(dict)
    if 'ml:real' in dict:
        return _literal(dict, scope)
    if 'ml:id' in dict:
        return _identifier(dict, scope)
    if 'ml:define' in dict:
        return _definition(dict, scope)
    if 'ml:apply' in dict:
        return _instruction(dict, scope)
    if 'ml:parens' in dict:
        return adaptor(dict['ml:parens'], scope)
