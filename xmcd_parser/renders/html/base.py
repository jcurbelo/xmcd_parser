class HTMLRender(object):
    """
    Base class
    """

    def __init__(self, *args, **kwargs):
        self.root = args[0]

    def render(self):
        return self._render_adaptor(self.root)

    def _render_adaptor(self, tree):

        tag = tree.tag.split('}')[1]
        if 'regions' == tag:
            return self._render_regions(tree)
        if 'region' == tag:
            return self._render_region(tree)
        if 'text' == tag:
            return self._render_text(tree)
        if 'p' == tag:
            return self._render_p(tree)
        if 'f' == tag:
            return self._render_f(tree)
        if 'b' == tag:
            return self._render_b(tree)
        if 'inlineAttr' == tag:
            return self._render_inline_attr(tree)
        if 'sub' == tag:
            return self._render_sub(tree)
        if 'sub' == tag:
            return self._render_sup(tree)
        if 'math' == tag:
            return self._render_math(tree)
        return ''

    def _render_region(self, tree):
        pass

    def _render_math(self, tree):
        pass

    def _render_sub(self, tree):
        pass

    def _render_inline_attr(self, tree):
        pass

    def _render_b(self, tree):
        pass

    def _render_f(self, tree):
        pass

    def _render_p(self, tree):
        pass

    def _render_text(self, tree):
        pass

    def _render_regions(self, tree):
        pass

    def _render_sup(self, tree):
        pass
