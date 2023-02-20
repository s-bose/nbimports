import os
import json
import questionary
import secrets
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import typer
from rich import print as rprint


templates_dir = os.path.join(os.path.dirname(__file__), "templates")

environment = Environment(loader=FileSystemLoader(templates_dir))
notebook_template = environment.get_template("notebook.template")
config_template = environment.get_template("config.template")
app = typer.Typer()

curr_path = os.path.abspath(os.getcwd())


@app.command()
def init():
    rprint("[bold green]Initializing for first time usage[/bold green]")

    import_paths = set()
    is_add_more = True

    while is_add_more:
        rel_path = questionary.path(
            "Please enter the path to module you want to add: "
        ).ask()
        rel_path = os.path.abspath(rel_path)
        import_paths.add(repr(rel_path))

        is_add_more = questionary.confirm("Add another directory?", default=False).ask()

    curr_path_json = json.dumps(repr(curr_path))

    context = {
        "notebook_dir": curr_path_json,
        "import_dirs": json.dumps(list(import_paths)),
    }

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
    import_dirs = config["imports_dir"]

    with open(os.path.join(curr_path, filename), "w") as fp:
        fp.write(notebook_template.render(modules_dir=import_dirs))


if __name__ == "__main__":
    app()
