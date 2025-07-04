from xmcd_parser.utils.node_adaptor import adaptor
from xmcd_parser.utils.scope import VARIABLES
from collections import *

scope = VARIABLES


def test_eval_definition_id_node():
    id_define_list = [id_define_dict1.getchildren()[0], id_define_dict2.getchildren()[0]]
    result_list = [38.0, 35.0]
    l = len(result_list)
    for i in xrange(l):
        node = adaptor(id_define_list[i], scope)
        assert result_list[i] == node.eval()


def test_eval_div_with_two_literals():
    node = adaptor(div_with_two_literals, scope)
    assert node.eval() == 1. / 2


def test_eval_div_with_two_ids():
    scope['F_{ty}'] = 1.
    scope['n_{y}'] = 2
    node = adaptor(div_with_two_access, scope)
    assert node.eval() == 1. / 2


def test_ast_min_with_div_and_mult():
    #  F_b = min(F_ty / n_y, F_tu / (K_t * n_u))
    F_ty, n_y, F_tu, K_t, n_u = 3.4, 50, 80, 45.90, 0.99
    scope.update({
        'F_{ty}': F_ty,
        'n_{y}': n_y,
        'F_{tu}': F_tu,
        'K_{t}': K_t,
        'n_{u}': n_u
    })
    node = adaptor(min_with_div_and_mult, scope)
    assert node.eval() == min(F_ty / n_y, F_tu / (K_t * n_u))


def test_ast_div_with_minus_and_parens():
    scope['B_{c}'] = 3.0
    scope['F_{cy}'] = 4.5
    scope['D_{c}'] = 4.00009
    node = adaptor(div_with_minus_and_parens, scope)
    assert node.eval() == -0.4499898752278073


def test_node_if_then():
    scope['S_{element.bend}'] = 3.9
    scope['S_{2}'] = 34.0
    scope['L_{b}'] = 56.0
    scope['r_{y}'] = 45.8
    scope['C_{b}'] = 45.9
    scope['E'] = 45.0
    node = adaptor(if_then_node, scope)
    assert node.eval() == -0.08438296787482133

# def test_eval_div_with_one_id_one_literal():
#     scope['n_y'] = 4.
#     node = adaptor(div_with_one_literal_one_access, scope)
#     assert node.eval() == 4. / 1
#
#
# def test_eval_pow_with_two_literals():
#     node = adaptor(pow_with_two_literals, scope)
#     assert node.eval() == 3.1416 ** 2
#
#
# def test_eval_div_with_mult():
#     scope['K_t'] = 4.55
#     scope['n_u'] = 3.434
#     scope['F_tu'] = 0.44
#     node = adaptor(div_with_mult, scope)
#     assert node.eval() == 0.44 / (4.55 * 3.434)
