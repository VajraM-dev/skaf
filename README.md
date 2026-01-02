# skaf 🚀

A simple, lightweight project scaffolding tool built with Python, Typer, and Rich. `skaf` helps you jumpstart your projects by generating boilerplate from customizable templates.

## ✨ Features

- **Template-based:** Create new projects from predefined or custom templates.
- **Variable Replacement:** Supports `{{variable}}` placeholders in any file within your template.
- **Interactive CLI:** Automatically detects variables and prompts you for values.
- **Flexible Metadata:** Add custom fields like `author`, `version`, or `license` to your templates.
- **Platform Idiomatic:** Stores templates in standard config directories (`AppData` on Windows, `.config` on Linux/macOS).
- **Batteries Included:** Automatically installs default templates on the first run.
- **UV Integration:** Built-in support for initializing Python projects with `uv`.

## 🚀 Installation

The easiest way to install `skaf` is using [uv](https://github.com/astral-sh/uv):

```bash
uv tool install skaf
```

Alternatively, you can install it via pip:

```bash
pip install skaf
```

## 🛠️ Usage

### 1. List Available Templates
See all templates currently installed on your system.
```bash
skaf list
```

### 2. Get Template Details
View a template's description, required variables, and custom metadata.
```bash
skaf info <template_name>
```

### 3. Initialize a New Project
Create a new project from a template. `skaf` will guide you through the configuration.
```bash
skaf init <template_name> <output_directory>
```

**Example:**
```bash
skaf init python-web ./my-api --python 3.12
```

## 📂 Template Locations

`skaf` looks for templates in the following platform-specific directories:

- **Windows:** `%APPDATA%\skaf\templates\`
- **Linux/macOS:** `~/.config/skaf/templates/`

Each template should be a folder containing:
1.  `template.toml`: (Optional) Manifest file for metadata.
2.  `files/`: A directory containing the boilerplate files.

## ✍️ Creating Your Own Template

1. Create a folder in your templates directory (e.g., `my-template`).
2. Create a `files/` directory inside it and add your boilerplate. Use `{{variable_name}}` for placeholders.
3. (Optional) Create a `template.toml` to add metadata:

```toml
name = "My Awesome Template"
description = "A starter for high-performance APIs"
author = "Your Name"
version = "1.0.0"

# You can also pre-define variables (optional, skaf auto-detects them too)
variables = ["project_name", "db_type"]
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
