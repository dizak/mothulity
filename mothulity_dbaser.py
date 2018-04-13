#!/usr/bin/env python


from __author import __author__
from __version import __version__
import os
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
    else:
        print "Status code {0}".format(status_code)


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
    args = parser.parse_args()

    if args.unite_ITS_02:
        download_path = "{0}/Unite_ITS_02.zip".format(args.download_directory)
        print "Downloading to {0}".format(download_path)
        get_db("https://www.mothur.org/w/images/4/49/Unite_ITS_02.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        os.system("unzip {0} -d {1}".format(download_path,
                                            args.download_directory))
        os.system("rm {0}".format(download_path))
        print "Unpacking done!"

    if args.unite_ITS_s_02:
        download_path = "{0}/Unite_ITS_s_02.zip".format(args.download_directory)
        print "Downloading to {0}/Unite_ITS_s_02.zip".format(args.download_directory)
        get_db("https://www.mothur.org/w/images/2/27/Unite_ITS_s_02.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        os.system("unzip {0} -d {1}".format(download_path,
                                            args.download_directory))
        os.system("rm {0}".format(download_path))

    if args.silva_102:
        download_path = "{0}/Silva.bacteria.zip".format(args.download_directory)
        print "Downloading to {0}/Silva.bacteria.zip".format(args.download_directory)
        get_db("https://www.mothur.org/w/images/9/98/Silva.bacteria.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        os.system("unzip {0} -d {1}".format(download_path,
                                            args.download_directory))
        os.system("rm {0}".format(download_path))
        print "Unpacking done!"
        download_path = "{0}/Silva.archaea.zip".format(args.download_directory)
        print "Downloading to {0}/Silva.archaea.zip".format(args.download_directory)
        get_db("https://www.mothur.org/w/images/3/3c/Silva.archaea.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        os.system("unzip {0} -d {1}".format(download_path,
                                            args.download_directory))
        os.system("rm {0}".format(download_path))
        print "Unpacking done!"
        download_path = "{0}/Silva.eukarya.zip".format(args.download_directory)
        print "Downloading to {0}/Silva.eukarya.zip".format(args.download_directory)
        get_db("https://www.mothur.org/w/images/1/1a/Silva.eukarya.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        os.system("unzip {0} -d {1}".format(download_path,
                                            args.download_directory))
        os.system("rm {0}".format(download_path))
        print "Unpacking done!"

    if args.silva_119:
        download_path = "{0}/Silva.nr_v119.tgz".format(args.download_directory)
        print "Downloading to {0}/Silva.nr_v119.tgz".format(args.download_directory)
        get_db("http://www.mothur.org/w/images/2/27/Silva.nr_v119.tgz",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        os.mkdir("{0}/Silva.nr_v119".format(args.download_directory))
        os.system("tar -xf {0} --directory {1}".format(download_path,
                                                       "{0}/Silva.nr_v119".format(args.download_directory)))
        os.system("rm {0}".format(download_path))
        print "Unpacking done!"

    if args.silva_123:
        download_path = "{0}/Silva.nr_v123.tgz".format(args.download_directory)
        print "Downloading to {0}/Silva.nr_v123.tgz".format(args.download_directory)
        get_db("https://www.mothur.org/w/images/b/be/Silva.nr_v123.tgz",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        os.mkdir("{0}/Silva.nr_v123".format(args.download_directory))
        os.system("tar -xf {0} --directory {1}".format(download_path,
                                                       "{0}/Silva.nr_v123".format(args.download_directory)))
        os.system("rm {0}".format(download_path))
        print "Unpacking done!"


if __name__ == '__main__':
    main()
