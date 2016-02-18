class HTMLRender(object):
    """
    Base class
    """

    def __init__(self, *args, **kwargs):
        self.root = args[0]

    def render(self):
        return self._render_adaptor(self.root)

    def _render_adaptor(self, tree):
        if 'region' in tree.tag:
            return self._render_region(tree)
        if 'text' in tree.tag:
            return self._render_text(tree)
        if 'p' in tree.tag:
            return self._render_p(tree)
        if 'f' in tree.tag:
            return self._render_f(tree)
        if 'b' in tree.tag:
            return self._render_b(tree)
        if 'inlineAttr' in tree.tag:
            return self._render_inline_attr(tree)
        if 'sub' in tree.tag:
            return self._render_sub(tree)
        if 'math' in tree.tag:
            return self._render_math(tree)

    def _render_region(self, tree):
        pass

    def _render_paragraph(self, tree):
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
