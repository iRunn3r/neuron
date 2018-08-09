from jinja2 import Template
import data
import os
import unidecode
import datetime


def create_table(rows):
    template_dir = os.path.join(data.PROJECT_ROOT, 'table_template.html')
    with open(template_dir, 'r') as template_file:
        template = Template(template_file.read())
        with open(os.path.join(data.PROJECT_ROOT, 'page.html'), 'w') as out_file:
            page = str(template.render(rows=rows, date=datetime.datetime.now().replace(microsecond=0)))
            out_file.write(unidecode.unidecode(page))
