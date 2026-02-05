from html.parser import HTMLParser

class _IndexHTMLCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.links = []
        self.anchors = []
        self.iframes = []
        self.forms = []
        self.inputs = []
        self.tags_with_style_attr = 0
        self._in_form_stack = []

    @staticmethod
    def _attrs_to_dict(attrs):
        return {k.lower(): v if v is not None else "" for k, v in attrs}

    def handle_starttag(self, tag, attrs):
        a = self._attrs_to_dict(attrs)
        if 'style' in a:
            self.tags_with_style_attr += 1
        t = tag.lower()
        if t == 'script':
            self.scripts.append(a)
        elif t == 'link':
            self.links.append(a)
        elif t == 'a':
            self.anchors.append(a)
        elif t == 'iframe':
            self.iframes.append(a)
        elif t == 'form':
            self._in_form_stack.append({'attrs': a, 'has_password': False})
        elif t == 'input':
            self.inputs.append(a)
            if self._in_form_stack and a.get('type','').lower() == 'password':
                self._in_form_stack[-1]['has_password'] = True

    def handle_endtag(self, tag):
        if tag.lower() == 'form' and self._in_form_stack:
            self.forms.append(self._in_form_stack.pop())
