from setuptools import find_packages
from distutils.core import setup
from glob import glob
from mothulity import __version__ as VERSION
from mothulity import __author__ as AUTHOR

j2_files = glob("templates/*j2")
js_files = glob("js/*js")
config_files = glob("config/*config")
blast_bin_files = glob("bin/mothur/blast/bin/*")
kronatools_img_files = glob("bin/kronatools/img/*")
kronatools_lib_files = glob("bin/kronatools/lib/*")
kronatools_src_files = glob("bin/kronatools/src/*")


setup(
    name="mothulity",
    version=VERSION,
    author=AUTHOR,
    packages=find_packages(exclude=["*test*"]),
    include_package_data=True,
    data_files=[
        ("templates", j2_files),
        ("js", js_files),
        ("config", config_files),
        ("bin/blast/bin", blast_bin_files),
        ("bin", [
            "bin/mothur/mothur",
            "bin/mothur/uchime",
            "bin/mothur/vsearch",
            "bin/kronatools/scripts/ktImportXML",
        ]),
        ("img", kronatools_img_files),
        ("lib", kronatools_lib_files),
        ("src", kronatools_src_files),
    ],
    python_requires='<3.7',
    install_requires=open("requirements.txt").readlines(),
    description="Easy-to-use tool facilitating work with Mothur.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author_email="dariusz.izak@ibb.waw.pl",
    url="https://github.com/dizak/mothulity",
    license="BSD",
    py_modules=["mothulity/utilities"],
    scripts=[
        "mothulity/mothulity",
        "mothulity/mothulity_draw",
        "mothulity/mothulity_dbaser",
        "mothulity/mothulity_fc",
     ],
    keywords=[
        "mothur",
        "diversity",
        "microbial-communities",
        "microbial-ecology",
        "16s",
        "16s-rrna",
        "its",
        "microbial",
        "fungal",
        "easy-to-use",
        ""
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
