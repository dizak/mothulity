#! /usr/bin/env python


import sys
import os
import shelve


__author__ = "Dariusz Izak IBB PAS"
__version = "0.9.7"


def get_dir_path(file_name=""):
    """
    Find out what is the script system path and return its location. Optionally
    put desired file name at the end of the path. Facilitates access to files
    stored in the same directory as executed script. Requires the executed
    script being added to the system path
    Parameters
    --------
    file_name: str, default <"">
        File name to put at the end of the path. Use empty string if want just
        the directory.
    Returns
    --------
    str
        System path of the executable.
    Examples
    -------
    >>> get_dir_path()
    '/home/user/program/bin/'
    >>> get_dir_path("foo")
    '/home/user/program/bin/foo'
    """
    prog_path = sys.argv[0].replace(sys.argv[0].split("/")[-1],
                                    file_name)
    return os.path.abspath(prog_path)


def dict2cache(cache_name,
               input_dict):
    try:
        cache = shelve.open(cache_name)
        for i in input_dict:
            cache[i] = input_dict[i]
    finally:
        cache.close()


def cache2dict(cache_name):
    try:
        cache = shelve.open(cache_name)
        return dict(cache)
    finally:
        cache.close()


def main():
    pass


if __name__ == '__main__':
    main()
