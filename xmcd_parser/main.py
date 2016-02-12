from lxml import etree
from utils.node_adaptor import adaptor
from utils.scope import VARIABLES


def main():
    tree = etree.parse('test.xmcd')
    root = tree.getroot()
    maths = root.findall('.//xmlns:math', {'xmlns': 'http://schemas.mathsoft.com/worksheet30'})

    scope = VARIABLES
    nodes = [adaptor(m.getchildren()[0], scope) for m in maths]
    # print nodes
    l = len(nodes)
    for i in xrange(l):
        n = nodes[i]
        if n:
            try:
                # n.eval()
                print n.str_tree(0)
                print
            except Exception as e:
                print 'ERROR IN NODE[{0}]({1}) \n {2}'.format(i, n.__class__.__name__, e)
                # pass
    print
    print '#' * 5 + 'SCOPE'
    print scope


if __name__ == '__main__':
    main()
