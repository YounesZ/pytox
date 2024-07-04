import os
import inspect
import importlib
from types import FunctionType, ModuleType
from typing import List, Any, Tuple, Dict, Union, TypeVar
from apps.lib.localvars import PATH_TO_CODE


def get_all_functions_in_package(package_name: str,
                                 exclude_paths: List[str] = None,
                                 exclude_modules: List[str] = None) -> List[Tuple[str, str, Any]]:
    if exclude_modules is None:
        exclude_modules = []

    if exclude_paths is None:
        exclude_paths = []
    else:
        exclude_paths = [os.path.join(PATH_TO_CODE, package_name, i_) for i_ in exclude_paths]

    functions = []
    package = importlib.import_module(package_name)
    package_path = package.__path__[0]

    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith(".py") and not any(i_ in root for i_ in exclude_paths) and (file not in exclude_modules):
                module_name = os.path.relpath(os.path.join(root, file), package_path)
                module_name = module_name.replace(os.path.sep, ".").rsplit(".", 1)[0]
                full_module_name = f"{package_name}.{module_name}"

                if any(full_module_name.startswith(f"{package_name}.{ex_mod}") for ex_mod in exclude_modules):
                    continue

                try:
                    module = importlib.import_module(full_module_name)
                    for name, obj in inspect.getmembers(module, inspect.isfunction):
                        if obj.__module__ == full_module_name:
                            functions.append((name, full_module_name, obj))
                except ImportError as e:
                    print(f"Failed to import {full_module_name}: {e}")

    return functions


def get_function_input_output_signature(fcn: FunctionType) -> Tuple[List[Dict], Union[type, TypeVar]]:
    sig = inspect.signature(fcn)

    # Print details of each parameter
    input = []
    for param_name, param in sig.parameters.items():
        # Get annotation
        annotation = param.annotation
        # Add to output
        input += [{'name': param_name,
                    'value': param,
                    'typing': annotation}]

    output = sig.return_annotation
    return input, output


def get_variables_in_module(module: ModuleType) -> List[str]:
    variables = []
    for name in dir(module):
        if not name.startswith('__'):  # Skip built-in attributes
            value = getattr(module, name)
            # Check if it's a variable (excluding functions, classes, and modules)
            if not callable(value) and not isinstance(value, type(module)):
                variables.append(name)
    return variables



if __name__ == '__main__':
    # Example usage:
    excluded_modules = ["__init__.py"]
    package_functions = get_all_functions_in_package("apps")

    for name, func in package_functions:
        print(f"Function name: {name}, Function: {func}")
        print( get_function_input_output_signature(func) )
        print('')