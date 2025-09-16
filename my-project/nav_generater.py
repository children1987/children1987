# gen_nav.py
import os
from pathlib import Path
import yaml

docs_dir = Path("docs")
nav = []

for item in sorted(docs_dir.iterdir()):
    if item.is_dir():
        section = {item.name: []}
        for subitem in sorted(item.iterdir()):
            if subitem.suffix == ".md" and subitem.name != "index.md":
                title = subitem.stem.replace("_", " ").title()
                section[item.name].append({title: str(subitem)})
        nav.append(section)
    elif item.suffix == ".md":
        title = item.stem.replace("_", " ").title()
        nav.append({title: str(item)})

with open("mkdocs.generated.yml", "w") as f:
    yaml.dump({"nav": nav}, f, allow_unicode=True, default_flow_style=False)
