import tomllib
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from pydantic import BaseModel, ConfigDict

class TemplateManifest(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    name: str
    description: str
    variables: List[str] = []

    def get_extra_info(self) -> Dict[str, Any]:
        """Return all fields except the standard ones."""
        standard_fields = {"name", "description", "variables"}
        return {k: v for k, v in self.model_dump().items() if k not in standard_fields}

class Template:
    def __init__(self, path: Path):
        self.path = path
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> TemplateManifest:
        manifest_path = self.path / "template.toml"
        
        # Auto-detect variables from files
        detected_vars = self.detect_variables()
        
        if not manifest_path.exists():
            return TemplateManifest(
                name=self.path.name,
                description=f"Template from {self.path.name}",
                variables=list(detected_vars)
            )
        
        with open(manifest_path, "rb") as f:
            data = tomllib.load(f)
            # Merge manifest variables with detected ones to be safe
            manifest_vars = data.get("variables", [])
            all_vars = list(set(manifest_vars) | detected_vars)
            data["variables"] = all_vars
            return TemplateManifest(**data)

    def detect_variables(self) -> Set[str]:
        variables = set()
        files_dir = self.path / "files"
        if not files_dir.exists():
            return variables
            
        # Regex to find {{variable_name}}
        pattern = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")
        
        for file_path in files_dir.rglob("*"):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding="utf-8")
                    matches = pattern.findall(content)
                    variables.update(matches)
                except (UnicodeDecodeError, PermissionError):
                    continue
        return variables

def list_templates(templates_dirs: List[Path]) -> Dict[str, Template]:
    templates = {}
    for t_dir in templates_dirs:
        if not t_dir.exists():
            continue
        for item in t_dir.iterdir():
            if item.is_dir() and item.name not in templates:
                templates[item.name] = Template(item)
    return templates
