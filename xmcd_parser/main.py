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
                n.eval()
            except Exception as e:
                print 'ERROR IN NODE[{0}] \n {1}'.format(i, e)
    print scope


if __name__ == '__main__':
    main()
