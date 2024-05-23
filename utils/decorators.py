import inspect
from functools import wraps
from typing import get_type_hints, Union, List, Dict, Tuple, Any


def validate_arguments(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the signature of the function
        sig = inspect.signature(func)

        # Bind the provided arguments to the signature
        try:
            bound_args = sig.bind(*args, **kwargs)
            # Apply default values to missing arguments
            bound_args.apply_defaults()
        except TypeError as e:
            raise ValueError(f"Invalid arguments: {e} for function {func}")

        # Extract type hints from the function
        type_hints = get_type_hints(func)

        # Validate each argument against its annotation
        for name, value in bound_args.arguments.items():
            if name in type_hints:
                expected_type = type_hints[name]
                if not is_instance_of_generic(value, expected_type):
                    raise TypeError(f"Argument '{name}' must be of type {expected_type.__name__}, but got {type(value).__name__}")

        return func(*args, **kwargs)

    return wrapper


def is_instance_of_generic(value, expected_type):
    origin = getattr(expected_type, '__origin__', None)
    args = getattr(expected_type, '__args__', [])

    if origin is None:
        if expected_type is Any:
            return True
        # Base case: not a generic, just check the type
        return isinstance(value, expected_type)

    # Handle Optional
    if origin is Union and type(None) in args:
        non_none_args = [arg for arg in args if arg is not type(None)]
        return value is None or any(is_instance_of_generic(value, arg) for arg in non_none_args)

    # Handle Union
    if origin is Union:
        return any(is_instance_of_generic(value, arg) for arg in args)

    # Handle List
    if origin in (list, List):
        return isinstance(value, list) and all(is_instance_of_generic(v, args[0]) for v in value)

    # Handle Dict
    if origin in (dict, Dict):
        cond = isinstance(value, dict)
        if len(args)>0:
            cond = cond and (all(is_instance_of_generic(k, args[0]) for k in value.keys()) and
                             all(is_instance_of_generic(v, args[1]) for v in value.values()))
        return cond

    # Handle Tuple
    if origin in (tuple, Tuple):
        if len(args) == 2 and args[1] is Ellipsis:
            return isinstance(value, tuple) and all(is_instance_of_generic(v, args[0]) for v in value)
        else:
            return (isinstance(value, tuple) and len(value) == len(args) and
                    all(is_instance_of_generic(v, t) for v, t in zip(value, args)))

    # Handle other generics
    if hasattr(expected_type, '__origin__'):
        return isinstance(value, expected_type.__origin__)

    return isinstance(value, expected_type)