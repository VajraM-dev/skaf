import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from skaf.config import get_templates_directories, GLOBAL_TEMPLATES_DIR
from skaf.templates import list_templates
from skaf.init import initialize_project

app = typer.Typer(
    help="skaf: A simple project scaffolding tool",
    no_args_is_help=True,
    add_completion=False
)
console = Console()

@app.command()
def list():
    """List all available templates."""
    templates = list_templates(get_templates_directories())
    if not templates:
        console.print("[yellow]No templates found.[/yellow]")
        console.print(f"\n[dim]Tip: Add templates to {GLOBAL_TEMPLATES_DIR}[/dim]")
        return

    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="magenta")
    table.add_column("Variables", style="green")

    for name, template in templates.items():
        table.add_row(
            name, 
            template.manifest.description, 
            ", ".join(template.manifest.variables) if template.manifest.variables else "None"
        )
    
    console.print(table)
    console.print("\n[bold blue]Next Step:[/bold blue] Run `skaf init <name> <path>` to start a project.")

@app.command()
def info(template_name: str):
    """Show detailed information about a template and its required variables."""
    templates = list_templates(get_templates_directories())
    if template_name not in templates:
        console.print(f"[red]Error:[/red] Template '{template_name}' not found.")
        raise typer.Exit(1)
    
    template = templates[template_name]
    console.print(f"[bold cyan]Template:[/bold cyan] {template_name}")
    console.print(f"[bold magenta]Description:[/bold magenta] {template.manifest.description}")
    
    extra_info = template.manifest.get_extra_info()
    if extra_info:
        for key, value in extra_info.items():
            # Format key: replace underscores with spaces and capitalize
            display_key = key.replace("_", " ").title()
            console.print(f"[bold yellow]{display_key}:[/bold yellow] {value}")

    console.print(f"[bold green]Required Variables:[/bold green]")
    if template.manifest.variables:
        for var in template.manifest.variables:
            console.print(f" - {var}")
    else:
        console.print(" None")
    console.print(f"\n[dim]Location: {template.path}[/dim]")

@app.command()
def init(
    template_name: str = typer.Argument(..., help="The name of the template to use"),
    output_dir: Path = typer.Argument(..., help="The directory where the project will be created"),
    python: Optional[str] = typer.Option(None, "--python", "-p", help="Python version to use (e.g. 3.11)")
):
    """Initialize a new project."""
    templates = list_templates(get_templates_directories())
    if template_name not in templates:
        console.print(f"[red]Error:[/red] Template '{template_name}' not found.")
        raise typer.Exit(1)

    template = templates[template_name]
    variables = {}
    
    # Ask for python version if not provided
    if not python:
        python = typer.prompt("Python version (leave empty for default)", default="", show_default=False)
        if python == "": python = None

    if template.manifest.variables:
        console.print(f"\n[bold]Configuring {template_name}...[/bold]")
        for var in template.manifest.variables:
            value = typer.prompt(f"Enter value for {var}")
            variables[var] = value

    try:
        initialize_project(template, output_dir, variables, python_version=python)
        console.print(f"\n[bold green]✨ Successfully initialized {template_name} in {output_dir}[/bold green]")
        console.print(f"\n[bold blue]Next Steps:[/bold blue]")
        console.print(f" 1. cd {output_dir}")
        console.print(" 2. uv sync")
        console.print(" 3. Start coding!")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
