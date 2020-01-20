import json

image_withBorder = 'border: 1px solid #e8e8eb;'
image_withBackground = 'background-color: #cdd1e0;'
image_stretched = 'width: 100%;'

parent_tag = ['<div>', "</div>"]

_tag_mapper = {
    'header': 'h',
    'paragraph': ['<p>', '</p>'],
    'list_unordered': 'ul',
    'list_ordered': 'ol',
    'list_items': ['<li>', '</li>'],
    'code': ['<code><pre>', '</pre></code>'],
    'delimiter': '<hr/>',
    'image': '<img />',
    'caption': ['<figcaption>', '</figcaption>'],
    'image_withBorder': image_withBorder,
    'image_withBackground': image_withBackground,
    'quote': 'blockquote'

}

_inline_classes = {
        'code': 'inline-code',
        'mark': 'cdx-marker',
}


class JsonToHtml(object):

    def __init__(self, tag_map=_tag_mapper):

        self.tag_map = tag_map
        if tag_map is None:
            self.tag_map = _tag_mapper
        self._inline_classes = _inline_classes
        self.parent_tag = parent_tag
        super().__init__()

    def convertToHtml(self, json_data):
        html = ""
        if not isinstance(json_data, dict):
            try:
                json_data = json.loads(json_data)
            except ValueError as e:
                raise ValueError("Not a valid json or Dict")
        
        # json_data = json.loads(json_data['blocks'])
        for i in json_data['blocks']:
            for k, v in i.items():
                func_name = self.get_rendeing_function_name(i)
                self.json_block = i
                getattr(self, func_name)()


    def get_rendeing_function_name(self, json_dict):

        tag = json_dict['type']
        return 'render_{}_html'.format(tag)

    def render_header_html(self):
        block=self.json_block
        h_level = block['data']['level']
        h_tag = self.tag_map[block['type']]
        return self.create_rendered_html("<%s%s>%s</%s%s>", (h_tag, h_level, block['data']['text'], h_tag, h_level))

    def render_paragraph_html(self):
        block=self.json_block
        p_tag = self.tag_map[block['type']]
        return self.create_rendered_html("%s".join(p_tag), (block['data']['text']))

    def create_rendered_html(self, markup, params):
        html = markup % params
        print(html)



js = None
with open("demo.json", 'r') as js_file:
    js = js_file.read()
    parse = JsonToHtml()
    parse.convertToHtml(js)