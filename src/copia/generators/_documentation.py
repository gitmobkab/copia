import inspect
import textwrap
from typing import Callable, get_args, get_origin, Literal, TypedDict


class ParsedDocstring(TypedDict):
    description: str
    locale: bool
    args: dict[str, str]
    returns: str
    note: str

def _format_type(annotation) -> str:
    """Format a type annotation as a readable string."""
    if annotation is inspect.Parameter.empty:
        return "—"
    if get_origin(annotation) is Literal:
        values = ", ".join(f"'{v}'" for v in get_args(annotation))
        return f"Literal[{values}]"
    if hasattr(annotation, "__name__"):
        return annotation.__name__
    return str(annotation)


def _format_default(default: inspect.Parameter) -> str:
    if default is inspect.Parameter.empty:
        return "—"
    if isinstance(default, str):
        return f"'{default}'"
    return str(default)


def _parse_docstring(doc: str) -> ParsedDocstring:
    """Parse a Google-style docstring into sections."""
    result = ParsedDocstring(
        description="",
        locale=False,
        args={},
        returns="",
        note=""
    )

    if not doc:
        result["description"] = "No description provided"
        return result

    lines = textwrap.dedent(doc).splitlines()

    # Description: everything before the first section header
    section = "description"
    desc_lines = []
    arg_name = None

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.lower() in ( "locale dependent:", "args:", "returns:" ,"note:"):
            if section == "description":
                result["description"] = " ".join(desc_lines).strip()
            section = stripped_line[:-1].lower()
            continue

        if section == "description":
            if stripped_line:
                desc_lines.append(stripped_line)

        elif section == "locale dependent":
            if stripped_line:
                result["locale"] = stripped_line.lower() == "yes"
                
        elif section == "args":
            # Each arg line: "    param: Description."
            # Continuation lines are indented further
            if stripped_line and not line.startswith("\t\t"):
                # New arg
                if ":" in stripped_line:
                    arg_name, arg_desc = stripped_line.split(":", 1)
                    arg_name = arg_name.strip()
                    result["args"][arg_name] = arg_desc.strip()
            elif stripped_line and arg_name:
                # Continuation of previous arg description
                result["args"][arg_name] += " " + stripped_line

        elif section == "returns":
            if stripped_line:
                result["returns"] += (" " if result["returns"] else "") + stripped_line

        elif section == "note":
            if stripped_line:
                result["note"] += (" " if result["note"] else "") + stripped_line


    if section == "description":
        result["description"] = " ".join(desc_lines).strip()

    return result


def _build_signature(name: str, sig: inspect.Signature) -> str:
    """Build a readable signature string."""
    parts = []
    for param in sig.parameters.values():
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            parts.append(f"*{param.name.capitalize()}")
        else:
            chunk = param.name
            if param.annotation is not inspect.Parameter.empty:
                chunk += f": {_format_type(param.annotation)}"
            if param.default is not inspect.Parameter.empty:
                chunk += f" = {_format_default(param.default)}"
            parts.append(chunk)

    return_str = ""
    if sig.return_annotation is not inspect.Parameter.empty:
        return_str = f" -> {_format_type(sig.return_annotation)}"

    return f"{name}({', '.join(parts)}){return_str}"

def _build_locale_note(locale: bool) -> str:
    """Build a note about locale dependence."""
    checkbox = "[x]" if locale else "[ ]"
    return f"{checkbox} Locale dependent"

def _build_args_table(sig: inspect.Signature, parsed_args: dict) -> str:
    """Build the markdown arguments table."""
    params = [
        param for param in sig.parameters.values()
    ]

    if not params:
        return ""

    rows = []
    for param in params:
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            type_str = "Any"
            default_str = "—"
            desc = parsed_args.get(param.name, "")
            rows.append(f"| `*{param.name}` | {type_str} | {default_str} | {desc} |")
        else:
            type_str = _format_type(param.annotation)
            default_str = _format_default(param.default)
            desc = parsed_args.get(param.name, "")
            rows.append(f"| `{param.name}` | {type_str} | {default_str} | {desc} |")

    header = (
        "**Arguments**\n\n"
        "| Param | Type | Default | Description |\n"
        "|-------|------|---------|-------------|"
    )
    return header + "\n" + "\n".join(rows)


def generate_generators_markdown(registry: dict[str, Callable]) -> str:
    """Generate a Markdown reference for all registered generators.

    Args:
        registry: The GENERATOR_REGISTRY dict mapping names to callables.

    Returns:
        A formatted Markdown string documenting all generators.
    """
    sections = ["# Generators\n"]

    for name, func in sorted(registry.items()):
        sections.append(generate_generator_markdown(name, func))
        
    return "\n---\n\n".join(sections)

def generate_generator_markdown(name: str, func: Callable, page_mode: bool = False) -> str:
    """Generate a markdown reference for a specific generator.

    Args:
        name (str): the name of the generator.
        func (Callable): the callable associed with the generator.
        page_mode (bool, optional): this affects if the heading should use # for the title, rather than ##.
            Defaults to False.

    Returns:
        str: A formatted Markdown string documenting the generator.
    """
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or ""
    parsed = _parse_docstring(doc)
    

    signature_str = _build_signature(name, sig)
    return_type = (
        _format_type(sig.return_annotation)
        if sig.return_annotation is not inspect.Parameter.empty
        else "—"
    )

    heading = f"# {name}\n" if page_mode else f"## `{name}`\n"
    block = [heading]
    block.append(f"> {signature_str}\n")

    if parsed["description"]:
        block.append(parsed["description"] + "\n")
    
    locale_note = _build_locale_note(parsed["locale"])
    block.append(f"- {locale_note}\n")

    args_table = _build_args_table(sig, parsed["args"])
    if args_table:
        block.append(args_table + "\n")

    returns_desc = parsed["returns"]
    if returns_desc:
        block.append(f"**Returns** `{return_type}` — {returns_desc}\n")
    elif return_type != "—":
        block.append(f"**Returns** `{return_type}`\n")

    if parsed["note"]:
        block.append(f"> ⚠️ {parsed['note']}\n")
        
    return "\n".join(block)