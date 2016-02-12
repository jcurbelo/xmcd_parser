from xmcd_parser.utils.node_adaptor import adaptor
from xmcd_parser.utils.scope import VARIABLES
from collections import *

scope = VARIABLES


def test_eval_definition_id_node():
    id_define_list = [id_define_dict1, id_define_dict2]
    result_list = [38.0, 24.0]
    l = len(result_list)
    for i in xrange(l):
        node = adaptor(id_define_list[i], scope)
        assert result_list[i] == node.eval()


def test_eval_div_with_two_literals():
    node = adaptor(div_with_two_literals, scope)
    assert node.eval() == 1. / 2


def test_eval_div_with_two_ids():
    scope['B_p'] = 1.
    scope['E'] = 2
    node = adaptor(div_with_two_access, scope)
    assert node.eval() == 1. / 2


def test_eval_div_with_one_id_one_literal():
    scope['n_y'] = 4.
    node = adaptor(div_with_one_literal_one_access, scope)
    assert node.eval() == 4. / 1


def test_eval_pow_with_two_literals():
    node = adaptor(pow_with_two_literals, scope)
    assert node.eval() == 3.1416 ** 2


def test_eval_div_with_mult():
    scope['K_t'] = 4.55
    scope['n_u'] = 3.434
    scope['F_tu'] = 0.44
    node = adaptor(div_with_mult, scope)
    assert node.eval() == 0.44 / (4.55 * 3.434)
