#!/usr/bin/env python

import os
import argparse
import requests as rq
from tqdm import tqdm


__author__ = "Dariusz Izak IBB PAS"


def get_db(url,
           save_path,
           chunk=8192):
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
                                     parsers",
                                     version="0.9.4")
    parser.add_argument("--unite-ITS-02",
                        action="store",
                        dest="unite_ITS_02",
                        metavar="",
                        default=None,
                        help="path/to/download-parser. Use if you want to\
                        download UNITE ITS 02 parser.")
    parser.add_argument("--unite-ITS-s-02",
                        action="store",
                        dest="unite_ITS_s_02",
                        metavar="",
                        default=None,
                        help="path/to/download-parser. Use if you want to\
                        download UNITE ITS s 02 parser.")
    parser.add_argument("--silva-102",
                        action="store",
                        dest="silva_102",
                        metavar="",
                        default=None,
                        help="path/to/download-parser. Use if you want to\
                        download Silva v102.")
    parser.add_argument("--silva-119",
                        action="store",
                        dest="silva_119",
                        metavar="",
                        default=None,
                        help="path/to/download-parser. Use if you want to\
                        download Silva v119.")
    parser.add_argument("--silva-123",
                        action="store",
                        dest="silva_123",
                        metavar="",
                        default=None,
                        help="path/to/download-parser. Use if you want to\
                        download Silva v123.")
    args = parser.parse_args()

    if args.unite_ITS_02 is not None:
        download_path = "{0}/Unite_ITS_02.zip".format(args.unite_ITS_02)
        print "Downloading to {0}".format(download_path)
        get_db("https://www.mothur.org/w/images/4/49/Unite_ITS_02.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0} -d {1}".format(download_path,
                                                args.unite_ITS_02))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
        quit()
    else:
        pass
    if args.unite_ITS_s_02 is not None:
        download_path = "{0}/Unite_ITS_s_02.zip".format(args.unite_ITS_s_02)
        print "Downloading to {0}/Unite_ITS_s_02.zip".format(args.unite_ITS_s_02)
        get_db("https://www.mothur.org/w/images/2/27/Unite_ITS_s_02.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0} -d {1}".format(download_path,
                                                args.unite_ITS_s_02))
            os.system("rm {0}".format(download_path))
            print "Failed to extract file... skipping"
        except:
            print "Unpacking done!"
        quit()
    else:
        pass
    if args.silva_102 is not None:
        download_path = "{0}/Silva.bacteria.zip".format(args.silva_102)
        print "Downloading to {0}/Silva.bacteria.zip".format(args.silva_102)
        get_db("https://www.mothur.org/w/images/9/98/Silva.bacteria.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0} -d {1}".format(download_path,
                                                args.silva_102))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
        download_path = "{0}/Silva.archaea.zip".format(args.silva_102)
        print "Downloading to {0}/Silva.archaea.zip".format(args.silva_102)
        get_db("https://www.mothur.org/w/images/3/3c/Silva.archaea.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0} -d {1}".format(download_path,
                                                args.silva_102))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
        download_path = "{0}/Silva.eukarya.zip".format(args.silva_102)
        print "Downloading to {0}/Silva.eukarya.zip".format(args.silva_102)
        get_db("https://www.mothur.org/w/images/1/1a/Silva.eukarya.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0} -d {1}".format(download_path,
                                                args.silva_102))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
        quit()
    else:
        pass
    if args.silva_119 is not None:
        download_path = "{0}/Silva.nr_v119.tgz".format(args.silva_119)
        print "Downloading to {0}/Silva.nr_v119.tgz".format(args.silva_119)
        get_db("http://www.mothur.org/w/images/2/27/Silva.nr_v119.tgz",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.mkdir("{0}/Silva.nr_v119".format(args.silva_119))
            os.system("tar -xf {0} --directory {1}".format(download_path,
                                                           "{0}/Silva.nr_v119".format(args.silva_119)))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
        quit()
    else:
        pass
    if args.silva_123 is not None:
        download_path = "{0}/Silva.nr_v123.tgz".format(args.silva_123)
        print "Downloading to {0}/Silva.nr_v123.tgz".format(args.silva_123)
        get_db("https://www.mothur.org/w/images/b/be/Silva.nr_v123.tgz",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.mkdir("{0}/Silva.nr_v119".format(args.silva_119))
            os.system("tar -xf {0} --directory {1}".format(download_path,
                                                           "{0}/Silva.nr_v119".format(args.silva_119)))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
        quit()
    else:
        pass


if __name__ == '__main__':
    main()
