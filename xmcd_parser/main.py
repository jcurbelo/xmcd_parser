from lxml import etree
from utils.node_adaptor import adaptor
from utils.scope import VARIABLES


def main():
    tree = etree.parse('test.xmcd')
    root = tree.getroot()
    maths = root.findall('.//xmlns:math', {'xmlns': 'http://schemas.mathsoft.com/worksheet30'})
    # m = maths[36]
    # etree.dump(m)
    scope = VARIABLES
    # scope['S_element.bend'] = 3.9
    # scope['S_2'] = 34.0
    # scope['L_b'] = 56.0
    # scope['r_y'] = 45.8
    # scope['C_b'] = 45.9
    # scope['E'] = 45.0
    # scope['S_1'] = 3.9
    # scope['F_cy'] = 3.9
    # scope['n_y'] = 3.9
    # scope['B_c'] = 3
    # scope['F_cy'] = 4
    # scope['D_c'] = 40
    nodes = [adaptor(m.getchildren()[0], scope) for m in maths]
    # n = adaptor(m.getchildren()[0], scope)
    # print n.eval()
    # print nodes
    l = len(nodes)
    for i in xrange(l):
        n = nodes[i]
        if i == 36:
            pass
        if n:
            try:
                n.eval()
                # print n.str_tree(0)
                # print
            except Exception as e:
                print 'ERROR IN NODE[{0}]({1}) \n {2}'.format(i, n.__class__.__name__, e)
                # pass
    print
    print '#' * 5 + 'SCOPE'
    # print scope
    import json
    print json.dumps(scope, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
