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


def _clean_dict(dict):
    for uk in unwanted_keys:
        if uk in dict:
            del dict[uk]


def _literal(dict, scope):
    if 'ml:real' in dict:
        return FloatNode(raw_text=dict['ml:real'], scope=scope)


def _identifier(dict, scope):
    if 'ml:id' in dict:
        return IdNode(raw_text=dict['ml:id']['#text'], xml_attr=dict['ml:id'], scope=scope)
    if 'ml:min' in dict:
        return


def adaptor(dict, scope):
    _clean_dict(dict)
    if 'ml:real' in dict:
        return _literal(dict, scope)
    if 'ml:id' in dict:
        return IdNode(raw_text=dict['ml:id']['#text'], xml_attr=dict['ml:id'], scope=scope)
    if 'ml:define' in dict:
        inner_dict = dict['ml:define']
        left = {'ml:id': inner_dict['ml:id']}
        body = {}
        if 'ml:real' in inner_dict:
            body = {'ml:real': inner_dict['ml:real']}
        if 'ml:apply' in inner_dict:
            body = {'ml:apply': inner_dict['ml:apply']}
        return DefinitionNode(scope=scope, left=adaptor(left, scope), body=adaptor(body, scope))
