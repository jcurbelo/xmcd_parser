# coding=utf-8
from ast.ast import IdNode, DefinitionNode, LiteralNode
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
        return self._render_tag(tree, 'b')

    def _render_regions(self, tree):
        super(BootstrapRender, self)._render_regions(tree)
        return reduce(lambda x, y: '{0}\n{1}'.format(x, y), [self._render_adaptor(el) for el in tree.getchildren()])

    def _render_region(self, tree):
        super(BootstrapRender, self)._render_region(tree)
        return self._render_tag(tree, 'div')

    def _render_math(self, tree):
        super(BootstrapRender, self)._render_math(tree)
        node = self.ast_adaptor(tree.getchildren()[0], self.ast_scope)
        if not node:
            return ''

        render = self.ast_render(node)
        id, rendered_id = '', ''

        disabled = ''
        if isinstance(node, DefinitionNode):
            id = node.left.id
            rendered_id = self.ast_render(node.left).render()
            if not isinstance(node.body, LiteralNode):
                disabled = 'disabled'
        try:
            value = node.eval()
        except Exception as e:
            return ''
        rendered_value = render.render()
        result = """
                <section class="row">
                    <div class="panel panel-default">
                        <div class="panel-body">
                            <div class="col col-md-4">
                                <div class="input-group">
                                    <span class="input-group-addon">{3}</span>
                                    <input id="{0}" name="{0}" value={1} title="Input Data" type="text" class="form-control" {4}>
                                </div>
                            </div>

                             <div class="col col-md-8">
                                {2}
                             </div>
                         </div>
                     </div>
                 </section>
                 """.format(id, value, rendered_value, rendered_id, disabled)
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
        return self._render_tag(tree, 'sub')

    def _render_sub(self, tree):
        super(BootstrapRender, self)._render_sub(tree)
        return self._render_tag(tree, 'sub')

    def _render_tag(self, tree, tag, **kwargs):
        children = list(tree)
        inner = ''
        text = tree.text or ''
        tail = tree.tail or ''
        attrs = kwargs.get('attrs', None)
        str_attrs = ''
        if attrs:
            str_attrs = reduce(lambda x, y: '{0} {1}'.format(x, y),
                               ['{0}="{1}"'.format(k, v) for k, v in
                                attrs.iterkeys()])
            str_attrs = ' {}'.format(str_attrs)
        if children:
            inner = reduce(lambda x, y: '{0}\n{1}'.format(x, y), [self._render_adaptor(el) for el in children]) or ''
            inner = inner.decode('utf-8')
        return '<{0}{2}>{3}{1}</{0}>{4}'.format(
                tag,
                inner.encode('utf-8'),
                str_attrs,
                text.encode('utf-8'),
                tail.encode('utf-8'))
