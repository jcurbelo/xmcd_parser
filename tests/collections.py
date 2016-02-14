import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from lxml import etree
tree = etree.parse(os.path.join(path, 'tests', 'test.xmcd'))
utree = etree.parse(os.path.join(path, 'tests', 'unit_tests.xml'))

uroot = utree.getroot()
root = tree.getroot()

maths = root.findall('.//xmlns:math', {'xmlns': 'http://schemas.mathsoft.com/worksheet30'})
umaths = uroot.findall('.//xmlns:math', {'xmlns': 'http://schemas.mathsoft.com/worksheet30'})

id_defines = maths[:20]
id_define_dict1 = id_defines[0]
id_define_dict2 = id_defines[1]

div_with_two_literals = umaths[1].getchildren()[0]
div_with_two_access = umaths[0].getchildren()[0]
min_with_div_and_mult = umaths[2].getchildren()[0]
div_with_minus_and_parens = umaths[3].getchildren()[0]
if_then_node = umaths[4].getchildren()[0]

# div_with_one_literal_one_access = {"ml:apply": {
#     "ml:div": None,
#     "ml:id": {
#         "#text": "n",
#         "@subscript": "y",
#         "@xml:space": "preserve"
#     },
#     "ml:real": "1"
# }}
#
# pow_with_two_literals = {"ml:apply": {
#     "ml:pow": None,
#     "ml:real": [
#         "3.1416",
#         "2"
#     ]
# }}
#
# div_with_mult = {"ml:apply": {
#     "ml:apply": {
#         "ml:id": [
#             {
#                 "#text": "K",
#                 "@subscript": "t",
#                 "@xml:space": "preserve"
#             },
#             {
#                 "#text": "n",
#                 "@subscript": "u",
#                 "@xml:space": "preserve"
#             }
#         ],
#         "ml:mult": None
#     },
#     "ml:div": None,
#     "ml:id": {
#         "#text": "F",
#         "@subscript": "tu",
#         "@xml:space": "preserve"
#     }}}
