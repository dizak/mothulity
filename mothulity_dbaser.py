#!/usr/bin/env python


from __author import __author__
from __version import __version__
import os, sys
import argparse
import requests as rq
from tqdm import tqdm


def get_db(url,
           save_path,
           chunk=8192):
    """
    Download from url to file. Handles different chunk sizes saving RAM. Shows
    progress with tqdm progress bar.

    Parameters
    -------
    url: str
        URL to download from.
    save_path: str
        Local URL to save to.
    chunk: int, default 8192
        Size of chunk the stream is divided to. Smaller it is less memory it
        uses.

    Examples
    -------
    >>> import os
    >>> get_db("http://google.com", "./tests/google.html")
    200
    >>> os.path.getsize("./tests/google.html") > 0
    True
    """
    res = rq.get(url, stream=True)
    total_len = int(res.headers.get("content-length"))
    if res.status_code == 200:
        with open(save_path, "wb") as fout:
            for i in tqdm(res.iter_content(chunk_size=chunk),
                          total=total_len / chunk):
                fout.write(i)
    return res.status_code


def download(download_directory,
             filename,
             url,
             command,
             input_arg,
             output_arg):
    """
    Download and unpack specified database into specified directory.

    Parameters
    -------
    db_type: str
        Database name which determines the download URL and archive type.
    download_directory: str
        Path where the database files would be downloaded.
    """
    download_path = "{}/{}".format(download_directory, filename)
    print "Download path: {}".format(download_path)
    print "Connecting..."
    try:
        res = get_db(url, download_path)
        if res == 200:
            print "Downloading done!"
            print "Unpacking..."
            os.system("{} {} {} {} {}".format(command,
                                              input_arg,
                                              download_path,
                                              output_arg,
                                              download_directory))
            os.system("rm {}".format(download_path))
            print "Unpacking done!"
        else:
            print "Failed to establish connection. Response code {}".format(res)
    except Exception as e:
        print "Failed to establish connection."


def main():
    parser = argparse.ArgumentParser(prog="mothulity_dbaser",
                                     usage="mothulity_dbaser [OPTION]",
                                     description="downloads mothur-suitable\
                                     databases",
                                     version=__version__)
    parser.add_argument(action="store",
                        dest="download_directory",
                        metavar="path/to/files",
                        default=".",
                        nargs="?",
                        help="Directory where the database is downloaded.")
    parser.add_argument("--unite-ITS-02",
                        action="store_true",
                        dest="unite_ITS_02",
                        help="Download UNITE ITS 02.")
    parser.add_argument("--unite-ITS-s-02",
                        action="store_true",
                        dest="unite_ITS_s_02",
                        help="Download UNITE ITS s 02.")
    parser.add_argument("--silva-102",
                        action="store_true",
                        dest="silva_102",
                        help="Download Silva v102.")
    parser.add_argument("--silva-119",
                        action="store_true",
                        dest="silva_119",
                        help="Download Silva v119.")
    parser.add_argument("--silva-123",
                        action="store_true",
                        dest="silva_123",
                        help="Download Silva v123.")

    if len(sys.argv)==1:
        parser.print_help()
        parser.exit()

    try:
        args = parser.parse_args()
    except SystemExit as error:
        if error.code == 2:
            parser.print_help()
        parser.exit()

    if args.unite_ITS_02:
        download(download_directory=args.download_directory,
                 filename="Unite_ITS_02.zip",
                 url="https://www.mothur.org/w/images/4/49/Unite_ITS_02.zip",
                 command="unzip",
                 input_arg="",
                 output_arg="-d")

    if args.unite_ITS_s_02:
        download(download_directory=args.download_directory,
                 filename="Unite_ITS_s_02.zip",
                 url="https://www.mothur.org/w/images/2/27/Unite_ITS_s_02.zip",
                 command="unzip",
                 input_arg="",
                 output_arg="-d")

    if args.silva_102:
        download(download_directory=args.download_directory,
                 filename="Silva.bacteria.zip",
                 url="https://www.mothur.org/w/images/9/98/Silva.bacteria.zip",
                 command="unzip",
                 input_arg="",
                 output_arg="-d")
        download(download_directory=args.download_directory,
                 filename="Silva.archaea.zip",
                 url="https://www.mothur.org/w/images/3/3c/Silva.archaea.zip",
                 command="unzip",
                 input_arg="",
                 output_arg="-d")
        download(download_directory=args.download_directory,
                 filename="Silva.eukarya.zip",
                 url="https://www.mothur.org/w/images/3/3c/Silva.archaea.zip",
                 command="unzip",
                 input_arg="",
                 output_arg="-d")

    if args.silva_119:
        download(download_directory=args.download_directory,
                 filename="Silva.nr_v119.tgz",
                 url="http://www.mothur.org/w/images/2/27/Silva.nr_v119.tgz",
                 command="tar",
                 input_arg="-xf",
                 output_arg="--directory")

    if args.silva_123:
        download(download_directory=args.download_directory,
                 filename="Silva.nr_v123.tgz",
                 url="https://www.mothur.org/w/images/b/be/Silva.nr_v123.tgz",
                 command="tar",
                 input_arg="-xf",
                 output_arg="--directory")

if __name__ == '__main__':
    main()
