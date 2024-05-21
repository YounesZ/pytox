import os
import inspect
import importlib
from typing import List, Callable, Tuple


def get_all_functions_in_package(package_name: str, exclude_modules: List[str] = None) -> List[Tuple[str, Callable]]:
    if exclude_modules is None:
        exclude_modules = []

    functions = []
    package = importlib.import_module(package_name)
    package_path = package.__path__[0]

    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_name = os.path.relpath(os.path.join(root, file), package_path)
                module_name = module_name.replace(os.path.sep, ".").rsplit(".", 1)[0]
                full_module_name = f"{package_name}.{module_name}"

                if any(full_module_name.startswith(f"{package_name}.{ex_mod}") for ex_mod in exclude_modules):
                    continue

                try:
                    module = importlib.import_module(full_module_name)
                    for name, obj in inspect.getmembers(module, inspect.isfunction):
                        if obj.__module__ == full_module_name:
                            functions.append((name, obj))
                except ImportError as e:
                    print(f"Failed to import {full_module_name}: {e}")

    return functions


def get_function_input_signature(fcn):
    sig = inspect.signature(fcn)

    # Print the signature
    print(f"Signature: {sig}")

    # Print details of each parameter
    output = []
    for param_name, param in sig.parameters.items():
        # Get annotation
        annotation = param.annotation
        # Add to output
        output += [{'name': param_name,
                    'value': param,
                    'typing': annotation}]
    return output


if __name__ == '__main__':
    # Example usage:
    excluded_modules = ["__init__.py"]
    package_functions = get_all_functions_in_package("apps")

    for name, func in package_functions:
        print(f"Function name: {name}, Function: {func}")
        print( get_function_input_signature(func) )
        print('')