import os
import typer
import questionary
from rich import print as rprint
import json
import secrets

from nbimports.constants import CONFIG_FILENAME
from nbimports.templates.jinja import config_template, notebook_template

app = typer.Typer()


@app.command()
def init():
    rprint("[bold green]Initializing for first time usage[/bold green]")

    curr_path = os.path.abspath(os.getcwd())

    import_paths = set()
    add_more: bool = True

    while add_more:
        rel_path = questionary.path(
            "Please enter the path to module you want to add: "
        ).ask()
        rel_path = os.path.abspath(rel_path)
        import_paths.add(repr(rel_path))

        add_more = questionary.confirm("Add another directory?", default=False).ask()

    curr_path_json = json.dumps(repr(curr_path))

    context = {
        "notebook_dir": curr_path_json,
        "import_dirs": json.dumps(list(import_paths)),
    }

    config_path = os.path.join(curr_path, CONFIG_FILENAME)
    print(config_path)
    with open(config_path, "w") as fp:
        fp.write(config_template.render(context))
    rprint(f"[bold green]set up nbimports config in {config_path}[/bold green]")
    rprint("[bold green]done! [/bold green]")


@app.command()
def generate():
    rprint("Generating empty notebook")

    curr_path = os.path.abspath(os.getcwd())

    config_path = os.path.join(curr_path, CONFIG_FILENAME)
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


@app.command()
def add():
    add_more: bool = True

    curr_path = os.path.abspath(os.getcwd())
    config_path = os.path.join(curr_path, CONFIG_FILENAME)

    with open(config_path) as fp:
        config = json.loads(fp.read())

    notebook_path = config["notebook_dir"].strip("'")
    if curr_path != notebook_path:

        rprint(
            "[bold red]Looks like you are trying to run the commands from another directory[/bold red]"
        )

    while add_more:
        rel_path = questionary.path(
            "Please enter the path to module you want to add: "
        ).ask()
        rel_path = os.path.abspath(rel_path)
        import_paths.add(repr(rel_path))

        add_more = questionary.confirm("Add another directory?", default=False).ask()
