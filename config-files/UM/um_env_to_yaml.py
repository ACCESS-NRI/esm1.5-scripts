#!/usr/bin/env python3
# Copyright 2024 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

# =========================================================================================
# Convert depreciated um_env.py configuration files for ESM1.5 simulations into yaml, for
# use with the newer versions of payu.
#
# To run:
#   python um_env_to_yaml.py <input_filepath> [--ofile <output_filepath>]
#
# If --ofile is not specified, it defaults to the same directory as  <input_filepath>
# with filename "um_env.yaml"
#
# Contact:
#   Spencer Wong <spencer.wong@anu.edu.au>
#
# Dependencies:
#    pyyaml
# =========================================================================================


import importlib.util
import sys
import argparse
import os
import errno
import yaml


def default_output_path(input_path):
    """
    Produce a default output path based on the path to the 
    input um_env.py file.

    Parameters
    ----------
    input_path (str): Path to um_env.py file for conversion.

    Returns
    -------
    output_path (str): Default path for writing converted yaml file.
    """
    input_dir = os.path.dirname(input_path)
    output_path = os.path.join(input_dir, "um_env.yaml")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a um_env.py configuration file to yaml"
    )
    parser.add_argument(
        "input_filepath", type=str, help="Path to the um_env.py file for conversion."
    )
    parser.add_argument(
        "--ofile", "-o",
        type=str,
        help=(
            "Filepath for the output yaml file. Defaults to "
            "same directory as the 'input_filepath', with name 'um_env.yaml'."
        ),
    )
    args = parser.parse_args()
    python_input_path = args.input_filepath

    if args.ofile is not None:
        yaml_output_path = args.ofile
    else:
        yaml_output_path = default_output_path(python_input_path)

    # Source the input um_env python file to get environment variable dictionary.
    # Based on example at
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    if not os.path.isfile(python_input_path):
        raise FileNotFoundError(
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            python_input_path
        )

    spec = importlib.util.spec_from_file_location("um_env", python_input_path)
    um_env = importlib.util.module_from_spec(spec)
    sys.modules["um_env"] = um_env
    spec.loader.exec_module(um_env)

    um_vars = um_env.vars

    # Export the dictionary to a yaml file
    with open(yaml_output_path, 'w') as file:
        file.write(
            yaml.dump(um_vars, default_flow_style=False, sort_keys=False)
        )
