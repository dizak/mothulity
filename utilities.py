#! /usr/bin/env python


from __author import __author__
from __version import __version__
import sys
import os
import shelve
from glob import glob
import ConfigParser


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


def set_config(filename,
               section,
               options,
               values,
               clean=False):
    if os.path.exists(filename):
        config = ConfigParser.SafeConfigParser()
        config.read(os.path.abspath(filename))
        if clean and section in config.sections():
            config.remove_section(section)
        if section not in config.sections():
            config.add_section(section)
        for o, v in zip(options, values):
            config.set(section, o, v)
        with open(filename, "wb") as fout:
            config.write(fout)
    else:
        return None


def main():
    pass


if __name__ == '__main__':
    main()
