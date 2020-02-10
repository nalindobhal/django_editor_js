import json
from html.parser import HTMLParser


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
    'figure': ['<figure>', '</figure>'],
    'image': '<img src="%s" alt="%s" />',
    'caption': ['<figcaption>', '</figcaption>'],
    'image_withBorder': image_withBorder,
    'image_withBackground': image_withBackground,
    'quote': ['<blockquote>', '</blockquote>']
}

inline_tag_mapper = {
    'img': ['<img', '/>'],
}

_inline_classes = {
        'code': 'inline-code',
        'mark': 'cdx-marker',
}


class HtmlTagParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag, attrs)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


class JsonToHtml(object):

    def __init__(self, tag_map=_tag_mapper):

        self.tag_map = tag_map
        if tag_map is None:
            self.tag_map = _tag_mapper
        self._inline_classes = _inline_classes
        self.parent_tag = parent_tag
        self.image_count = 0
        self._html = []
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
            func_name = self.get_rendeing_function_name(i)
            self.json_block = i
            getattr(self, func_name)()
        return "".join(self._html)


    def get_rendeing_function_name(self, json_dict):

        tag = json_dict['type']
        return 'render_%s_html' %tag

    def render_header_html(self):
        block=self.json_block
        h_level = block['data']['level']
        h_tag = self.tag_map[block['type']]
        return self.create_rendered_html("<%s%s>%s</%s%s>", (h_tag, h_level, block['data']['text'], h_tag, h_level))

    def render_paragraph_html(self):
        block=self.json_block
        p_tag = self.tag_map[block['type']]
        return self.create_rendered_html("%s".join(p_tag), (block['data']['text']))

    def render_list_html(self):
        block=self.json_block
        list_type = block['data']['style']
        list_tag = self.tag_map[block['type'] + '_' + list_type]
        list_items = self.tag_map[block['type'] + '_' + 'items']
        list_items_html = "".join([list_items[0] + i + list_items[1] for i in block['data']['items']])
        return self.create_rendered_html("<%s>%s</%s>", (list_tag, list_items_html, list_tag))

    def render_code_html(self):
        block=self.json_block
        code_tag = self.tag_map[block['type']]
        return self.create_rendered_html("%s".join(code_tag), (block['data']['code']))    

    def render_delimiter_html(self):
        block=self.json_block
        hr_tag = self.tag_map[block['type']]
        return self.create_rendered_html(hr_tag)

    def render_image_html(self):
        self.image_count += 1
        block=self.json_block
        figure_tag = self.tag_map['figure']
        figure_caption_tag = self.tag_map['caption']
        img_tag = self.tag_map[block['type']]
        img_data = block['data']
        rendering_list = []
        rendering_list.append(figure_tag[0])
        rendering_list.append(img_tag % (img_data['file']['url'], "Image-{}".format(self.image_count)))
        rendering_list.extend([figure_caption_tag[0], img_data['caption'], figure_caption_tag[1]])
        rendering_list.append(figure_tag[1])
        return self.create_rendered_html("".join(rendering_list))

    def render_quote_html(self):
        block=self.json_block
        quote_tag = self.tag_map[block['type']]
        quote_data = block['data']
        figure_tag = self.tag_map['figure']
        figure_caption_tag = self.tag_map['caption']
        rendering_list = []
        rendering_list.append(figure_tag[0])
        rendering_list.append(quote_data['text'].join(quote_tag))
        rendering_list.extend([figure_caption_tag[0], quote_data['caption'], figure_caption_tag[1]])
        rendering_list.append(figure_tag[1])
        return self.create_rendered_html("".join(rendering_list))    

    def create_rendered_html(self, markup, params=None):
        if params:
            markup = markup % params    
        self._html.append(markup)



js = None
with open("demo.json", 'r') as js_file:
    parse = JsonToHtml()
    print(parse.convertToHtml(js_file.read()))
    # p = HtmlTagParser()
    # p.feed("<b>Some Bold Text.</b>")
