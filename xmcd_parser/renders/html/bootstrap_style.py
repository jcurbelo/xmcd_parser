from ast.ast import IdNode, DefinitionNode
from renders.html.base import HTMLRender


class BootstrapRender(HTMLRender):
    def __init__(self, *args, **kwargs):
        super(BootstrapRender, self).__init__(*args, **kwargs)
        self.ast_scope = kwargs.get('ast_scope', {})
        self.ast_adaptor = kwargs.get('ast_adaptor', lambda _: _)
        self.ast_render = kwargs.get('ast_render', lambda _: _)

    def _render_f(self, tree):
        super(BootstrapRender, self)._render_f(tree)
        return self._render_inline_attr(tree)

    def _render_b(self, tree):
        super(BootstrapRender, self)._render_b(tree)
        self._render_tag(tree, 'b')

    def _render_regions(self, tree):
        super(BootstrapRender, self)._render_regions(tree)
        return reduce(lambda x, y: '{0}\n{1}'.format(x, y), [self._render_adaptor(el) for el in tree.getchildren()])

    def _render_region(self, tree):
        super(BootstrapRender, self)._render_region(tree)
        return '<div class="row">{}</div>'.format(
                reduce(
                        lambda x, y: '{0}\n{1}'.format(x, y),
                        [self._render_adaptor(t) for t in tree.getchildren()]
                ))

    def _render_math(self, tree):
        super(BootstrapRender, self)._render_math(tree)
        node = self.ast_adaptor(tree.getchildren()[0], self.ast_scope)
        if not node:
            return ''

        render = self.ast_render(node)
        id = ''
        if isinstance(node, DefinitionNode):
            id = node.left.id
        try:
            value = node.eval()
        except Exception as e:
            return ''
        str_value = render.render()
        result = """
                <section class="row">
                    <div class="col col-md-4">
                        <form class="form-inline">
                            <div class="form-group">
                                <label>`{0}`</label>
                                <div class="input-group">
                                    <input value={1} title="Input Data" type="text" class="form-control" placeholder="Input">
                                </div>
                            </div>
                        </form>
                    </div>

                     <div class="col col-md-8">
                        `{2}`
                     </div>
                 </section>
                 <br>
                 """.format(id, value, str_value)
        return result

    def _render_inline_attr(self, tree):
        super(BootstrapRender, self)._render_inline_attr(tree)
        return self._render_tag(tree, 'span')

    def _render_p(self, tree):
        super(BootstrapRender, self)._render_p(tree)
        return self._render_tag(tree, 'p')

    def _render_text(self, tree):
        super(BootstrapRender, self)._render_text(tree)
        return self._render_inline_attr(tree)

    def _render_sup(self, tree):
        super(BootstrapRender, self)._render_sup(tree)
        self._render_tag(tree, 'sub')

    def _render_sub(self, tree):
        super(BootstrapRender, self)._render_sub(tree)
        self._render_tag(tree, 'sub')

    def _render_tag(self, tree, tag):
        children = tree.getchildren()
        inner = tree.text
        if children:
            inner = reduce(lambda x, y: '{0}\n{1}'.format(x, y), [self._render_adaptor(el) for el in children])
            if inner:
                inner = inner.decode('utf-8')
        if inner is None:
            inner = ''
        return '<{0}>{1}</{2}>'.format(tag, inner.encode('utf-8'), tag)
