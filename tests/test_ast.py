from xmcd_parser.utils.node_adaptor import adaptor
from xmcd_parser.utils.scope import VARIABLES
from collections import *

session = VARIABLES


def test_eval_definition_id_node():
    id_define_list = [id_define_dict1, id_define_dict2]
    result_list = [38.0, 24.0]
    l = len(result_list)
    for i in xrange(l):
        node = adaptor(id_define_list[i], session)
        assert result_list[i] == node.eval()
