import os
import json
import questionary
from pathlib import Path
import secrets
import json
from jinja2 import Environment, FileSystemLoader
import typer
from rich import print as rprint

from nbimports.utils import escape_slashes_winpath

templates_dir = os.path.join(os.path.dirname(__file__), "templates")

environment = Environment(loader=FileSystemLoader(templates_dir))
notebook_template = environment.get_template("notebook.template")
config_template = environment.get_template("config.template")
app = typer.Typer()

curr_path = os.path.abspath(os.getcwd())


@app.command()
def init():
    rprint("[bold green]Initializing for first time usage[/bold green]")
    rel_path = questionary.path(
        "Please enter the relative path to module you want to add: "
    ).ask()
    rel_path = os.path.abspath(rel_path)

    curr_path_json = json.dumps(repr(curr_path))
    rel_path_json = json.dumps(repr(rel_path))

    context = {"notebook_dir": curr_path_json, "import_dirs": [rel_path_json]}

    config_path = os.path.join(curr_path, "nbimport_conf.json")
    with open(config_path, "w") as fp:
        fp.write(config_template.render(context))
    rprint(f"[bold green]set up nbimport config in {config_path}[/bold green]")


@app.command()
def generate():
    rprint("Generating empty notebook")
    config_path = os.path.join(curr_path, "nbimport_conf.json")
    if not os.path.exists(config_path):
        rprint("[bold red]no nbimport config found. Skipping.[/bold red]")
        exit()

    with open(config_path) as fp:
        config = json.loads(fp.read())

    filename = questionary.text("Enter file name [optional]").ask()
    filename = filename or str(secrets.token_hex())
    filename = f"{filename}.ipynb"
    imports_dir = config["imports_dir"][0]
    with open(os.path.join(curr_path, filename), "w") as fp:
        fp.write(notebook_template.render(modules_dir=imports_dir))


if __name__ == "__main__":
    app()
