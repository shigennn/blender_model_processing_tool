import sys
from argparse import ArgumentParser, REMAINDER
from distutils.util import strtobool
from typing import List, Optional

HELP = 'help'


def get_cmdarg(*args: str) -> List[str|None] | bool:
    """
    Parse command-line arguments and return the values for the specified argument names.

    Arguments:
    *args: str - variable number of string arguments representing the names of the command-line arguments to retrieve.

    Returns:
    List[str] - a list of string values for each of the specified command-line arguments. If only one argument was specified,
                a list with a single string value will be returned.
    """
    parser = ArgumentParser()
    for argument_name in args:
        parser.add_argument('--' + argument_name, nargs=REMAINDER, help='help', required=False)

    # Get the arguments after the "--" separator
    sys_args = sys.argv[sys.argv.index("--") + 1:]
    args, unknown = parser.parse_known_args(sys_args)

    argument_values = []
    for argument_name in args.__dict__:
        if args.__dict__[argument_name]:
            argument_value = args.__dict__[argument_name]

            # If an argument starts with "--", all subsequent arguments should be treated as a new argument
            next_arg_index = None
            for i, arg in enumerate(argument_value):
                if arg.startswith("--"):
                    next_arg_index = i
                    break

            if next_arg_index is not None:
                argument_value = argument_value[:next_arg_index]

            # Get any additional arguments after the current argument
            additional_args = sys.argv[sys.argv.index("--") + 1:]
            for i, arg in enumerate(additional_args):
                if arg.startswith("--"):
                    break
                elif i >= len(argument_value):
                    argument_value.append(arg)

            argument_values.append(argument_value)
        else:
            argument_values.append([])

    # If only one argument was specified, return a list with a single string value
    argument_value = argument_values[0] if len(args.__dict__) == 1 else argument_values

    # If only one argument value and strbool supplyment, return str or bool
    if len(argument_value) == 1:
        try:
            argument_value = strtobool(argument_value[0])
        except:
            pass

    return argument_value