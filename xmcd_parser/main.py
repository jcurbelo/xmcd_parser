from lxml import etree
from utils.node_adaptor import adaptor
from utils.scope import VARIABLES


def main():
    tree = etree.parse('test.xmcd')
    root = tree.getroot()
    maths = root.findall('.//xmlns:math', {'xmlns': 'http://schemas.mathsoft.com/worksheet30'})
    el1 = maths[0].getchildren()[0]
    el2 = maths[1].getchildren()[0]
    for el in [el1, el2]:
        adaptor(el, {})
    print ''
    scope = VARIABLES
    nodes = [adaptor(m.getchildren[0], scope) for m in maths[:20]]
    print nodes
    for n in nodes:
        n.eval()
    print scope


if __name__ == '__main__':
    main()
