import os
from jinja2 import Environment, FileSystemLoader

templates_dir = os.path.join(os.path.dirname(__file__))
environment = Environment(loader=FileSystemLoader(templates_dir))

notebook_template = environment.get_template("notebook.template")
config_template = environment.get_template("config.template")
