from xmcd_parser.ast.ast import *
from collections import *
from xmcd_parser.utils.node_adaptor import adaptor
from xmcd_parser.utils.scope import VARIABLES

session = VARIABLES


def test_adaptor_definition_id_node():
    id_define_list = [id_define_dict1, id_define_dict2]
    for id in id_define_list:
        node = adaptor(id, session)
        assert isinstance(node, DefinitionNode)
