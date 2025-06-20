from xmcd_parser.ast.ast import *
from collections import *
from xmcd_parser.utils.node_adaptor import adaptor
from xmcd_parser.utils.scope import VARIABLES

scope = VARIABLES


def test_adaptor_definition_id_node():
    id_define_list = [id_define_dict1.getchildren()[0], id_define_dict2.getchildren()[0]]
    for id in id_define_list:
        node = adaptor(id, scope)
        assert isinstance(node, DefinitionNode)


def test_adaptor_div_with_two_literals():
    node = adaptor(div_with_two_literals, scope)
    assert isinstance(node, DivNode)


def test_adaptor_div_with_two_literals_expression_list_types():
    node = adaptor(div_with_two_literals, scope)
    assert type(node.expression_list) == list


def test_adaptor_div_with_two_ids():
    node = adaptor(div_with_two_access, scope)
    assert isinstance(node, DivNode)


def test_adaptor_min_with_div_and_mult():
    node = adaptor(min_with_div_and_mult, scope)
    assert isinstance(node, DefinitionNode)


def test_adaptor_div_with_minus_and_parens():
    node = adaptor(div_with_minus_and_parens, scope)
    assert isinstance(node, DefinitionNode)


def test_adaptor_if_then():
    node = adaptor(if_then_node, {})
    assert isinstance(node, DefinitionNode)

# def test_adaptor_div_with_one_id_one_literal():
#     node = adaptor(div_with_one_literal_one_access, scope)
#     assert isinstance(node, DivNode)
#
#
# def test_adaptor_pow_with_two_literals():
#     node = adaptor(pow_with_two_literals, scope)
#     assert isinstance(node, PowNode)
#
#
# def test_adaptor_div_with_mult():
#     node = adaptor(div_with_mult, scope)
#     assert isinstance(node, DivNode)
