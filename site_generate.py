from jinja2 import Template
import os
import json
import argparse
from os.path import join, split, exists
from os import makedirs
from re import sub
from markdown import markdown


DIR_TO_SAVE = 'site'
DIR_TO = 'site/index.html'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='type of file must be json')
    arg = parser.parse_args()

    return arg.file_path

def load_structure(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def convert_md_to_html(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as data:
        return markdown(data.read(), extensions=['codehilite', 'fenced_code'])


def create_dir_for_file(path):
    if not exists(split(path)[0]):
        makedirs(split(path)[0])


def generate_pages(data, filepath, template):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template.render(info=data))

def render_template(template):
    with open(template, encoding = 'utf-8') as html_page:
        template = Template(html_page.read())
        return template

def generate_articles_html(structure, template):
    for item in structure['articles']:
        text = convert_md_to_html(join('articles', item['source']))
        context = {
        'title': item['title'],
        'topic': item['topic'],
        'text' : text
        }
        path_to_save = join(DIR_TO_SAVE, item['source'])
        final_path = sub(r'&.+?.md$|.md$', '.html', path_to_save)
        create_dir_for_file(final_path)
        generate_pages(context, final_path, template) 


def generate_index_html(structure, template):
    for item in structure['articles']:
        path_to_save = join(DIR_TO_SAVE, item['source'])
        item['source'] = sub(r'&.+?.md$|.md$', '.html', path_to_save)
        generate_pages(structure, DIR_TO, template) 

if __name__ == '__main__':
    get_structure_location = get_args()
    structure = load_structure(get_structure_location)
    articles_template = render_template('templates/base.html')
    generate_articles_html(structure,articles_template)
    index_template = render_template('templates/index.html')
    generate_index_html(structure,index_template)