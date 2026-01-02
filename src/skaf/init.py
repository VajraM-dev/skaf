import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional
from rich.console import Console
from skaf.templates import Template

console = Console()

def initialize_project(template: Template, target_dir: Path, variables: Dict[str, str], python_version: Optional[str] = None):
    if target_dir.exists() and any(target_dir.iterdir()):
        raise FileExistsError(f"Target directory {target_dir} is not empty")

    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Run uv init with optional python version
    cmd = ["uv", "init", "--no-workspace"]
    if python_version:
        cmd.extend(["--python", python_version])
        
    try:
        subprocess.run(cmd, cwd=target_dir, check=True, capture_output=True)
        ver_str = python_version or "default"
        console.print(f"[blue]Info:[/blue] Initialized python project (version: {ver_str})")
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] Could not run 'uv init': {e}")

    files_dir = template.path / "files"
    if not files_dir.exists():
        return

    # Use rglob("*") but also handle hidden files explicitly if needed
    # Path.rglob("*") in Python 3.13+ handles hidden files, but let's be safe
    for src_path in files_dir.rglob("*"):
        if src_path.is_dir():
            continue
            
        rel_path = src_path.relative_to(files_dir)
        dest_path = target_dir / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            content = src_path.read_text(encoding="utf-8")
            for var, value in variables.items():
                content = content.replace(f"{{{{{var}}}}}", value)
            dest_path.write_text(content, encoding="utf-8")
            console.print(f"[green]Created:[/green] {rel_path}")
        except UnicodeDecodeError:
            # For binary files, just copy them
            shutil.copy2(src_path, dest_path)
            console.print(f"[green]Copied (binary):[/green] {rel_path}")
