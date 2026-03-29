import inspect

from rich import print as pprint


from copia.generators import GENERATORS


for name in GENERATORS:
    current_func = GENERATORS[name]
    func_signature = inspect.signature(current_func)
    
    pprint(f"[blue]{name}:[/]")
    pprint("\t[PARAMETERS]")
    pprint("\t\t[bold green]name\ttype[/]")
    for param_name in func_signature.parameters:
        param = func_signature.parameters[param_name]
        pprint(f"\t\t{param_name} \t {param}")