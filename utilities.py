#! /usr/bin/env python


from __author import __author__
from __version import __version__
import sys
import os
import shelve
from glob import glob


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
    >>> get_dir_path() # doctest: +SKIP
    '/home/user/program/bin/'
    >>> get_dir_path("foo") # doctest: +SKIP
    '/home/user/program/bin/foo'
    """
    prog_path = sys.argv[0].replace(sys.argv[0].split("/")[-1],
                                    file_name)
    return os.path.abspath(prog_path)


def path2name(path,
              slash="/",
              hid_char=".",
              extension=False):
    """
    Returns just filename with or without extension from the full path.

    Parameters
    -------
    path: str
        Input path.
    slash: str
        Slash to use. Backslash does NOT work properly yet. Default: </>.
    hid_char: str
        Character indicating that file is hidden. Default: <.>
    extension: bool
        Return filename with extension if <True>. Remove extension\
        otherwise. Default: <False>.

    Returns
    -------
    str
        Filename from the path.

    Examples
    -------
    >>> path2name("/home/user/foo.bar")
    'foo'
    >>> path2name("/home/user/.foo.bar")
    'foo'
    >>> path2name("/home/user/foo.bar", extension=True)
    'foo.bar'
    >>> path2name("/home/user/.foo.bar", extension=True)
    'foo.bar'
    """
    if extension is True:
        return str(path.split(slash)[-1].strip(hid_char))
    else:
        return str(path.split(slash)[-1].strip(hid_char).split(".")[0])


def dict2cache(cache_name,
               input_dict):
    """
    Save dict to cache.

    Parameters
    -------
    cache_name: str
        Name of cache to be saved.
    input_dict: dict
        Dict to create cache from.

    Examples
    -------
    >>> my_dict = {"foo": "bar"}
    >>> dict2cache("./tests/foobar", my_dict)
    """
    try:
        cache = shelve.open(cache_name)
        for i in input_dict:
            cache[i] = input_dict[i]
    finally:
        cache.close()


def cache2dict(cache_name):
    """
    Read from cache to dict.

    Parameters
    -------
    cache_name: str
        Cache to create dict from.

    Examples
    -------
    >>> my_dict = cache2dict("./tests/foobar")
    >>> my_dict
    {'foo': 'bar'}
    """
    try:
        cache = shelve.open(cache_name)
        return dict(cache)
    finally:
        cache.close()


def find_cache(directory,
               hidden=True):
    """
    Finds proper cache for shelve by files extensions and compare whether the\
    first part of the name matches with all three extensions.

    Parameters
    -------
    directory: str
        Input directory
    hidden: bool
        Searches for files starting with the dot if <True>. Default: <True>.

    Examples
    -------
    >>> find_cache(directory="./tests/", hidden=True)
    ['foobar']
    >>> find_cache(directory="./tests/", hidden=False)
    ['foobar']
    """
    if hidden is True:
        hid_char = "."
    else:
        hid_char = ""
    dir_list = glob("{}/{}*dir".format(directory, hid_char))
    dat_list = glob("{}/{}*dat".format(directory, hid_char))
    dir_lognames = [path2name(i) for i in dir_list]
    dat_lognames = [path2name(i) for i in dat_list]
    commong_lognames = [i for i in dat_lognames if i in dir_lognames]
    return commong_lognames


def main():
    pass


if __name__ == '__main__':
    main()
