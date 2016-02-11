import xmltodict
from utils.node_adaptor import adaptor
from utils.scope import VARIABLES


def main():
    with open('test.xmcd') as fd:
        xmcd_dict = xmltodict.parse(fd.read())
        regions = xmcd_dict['worksheet']['regions']['region']
        maths = filter(lambda r: 'math' in r.keys(), regions)
        ast_dicts = [m['math'] for m in maths]
        scope = VARIABLES
        nodes = [adaptor(ast_dict, scope) for ast_dict in ast_dicts[:20]]
        print nodes
        for n in nodes:
            n.eval()
        print scope


if __name__ == '__main__':
    main()
