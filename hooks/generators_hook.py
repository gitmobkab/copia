import os

from copia.generators import GENERATORS_REGISTRY
from copia.generators._documentation import generate_generator_markdown


def on_pre_build(config):
    out = "docs/generators"
    os.makedirs(out, exist_ok=True)

    sorted_names = sorted(GENERATORS_REGISTRY.keys())

    # index.md — list of links
    links = "\n".join(f"- [{name}]({name}.md)" for name in sorted_names)
    with open(f"{out}/index.md", "w", encoding="utf-8") as f:
        f.write("# Generators\n\n")
        f.write(links + "\n")

    # one page per generator
    for name in sorted_names:
        func = GENERATORS_REGISTRY[name]
        with open(f"{out}/{name}.md", "w", encoding="utf-8") as f:
            f.write(generate_generator_markdown(name, func, True))

    # update nav dynamically
    generators_nav = [{"Overview": "generators/index.md"}] + [
        {name: f"generators/{name}.md"} for name in sorted_names
    ]
    for section in config["nav"]:
        if isinstance(section, dict) and "Generators" in section:
            section["Generators"] = generators_nav
            break