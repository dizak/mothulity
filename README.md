# mothur_files_creator

Simple script for creating \*files file that [mothur](https://www.mothur.org/) uses.

### Usage examples

```
usage: mothur_files_creator [directory] [OPTION]

creates mothur-suitable <.files> file just upon the input file names. Removes
<-> from file names

positional arguments:
  path/to/files         input directory path.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o , --output         output file name. Default <mothur.files>
  -s , --split-sign     first group of characters before this sign is
                        recognized as sample name. Default <_>
  -e , --files-extension
                        reads files are recognized by this. Default <fastq>
  -l , --left-reads-sign
                        left reads files are recognized by this. Default <R1>
  -r , --right-reads-sign
                        right reads files are recognized by this. Default <R2>
  --original-names      use if you do not want to modify file names
```

#### Let's assume you have a directory containing 4 files:

1. group001_S1_R1.fastq
2. group001_S1_R2.fastq
3. group002_S1_R1.fastq
4. group004_S1_R2.fastq

Running ```mothur_files_creator.py /path/to/files -o my_output.files``` will create a file with following content:

```
group001  group001_S1_R1.fastq  group001_S1_R2.fastq
group002  group002_S1_R1.fastq  group004_S1_R2.fastq
```

#### Unusual names, extensions, etc.

If using _ sign is not the best idea in your case, use ```--split-sign```. Running ```mothur_files_creator --split-sign _L``` on this set:

```
F3D0_S188_L001_R1_001.fastq    F3D147_S213_L001_R1_001.fastq  F3D5_S193_L001_R1_001.fastq
F3D0_S188_L001_R2_001.fastq    F3D147_S213_L001_R2_001.fastq  F3D5_S193_L001_R2_001.fastq
F3D141_S207_L001_R1_001.fastq  F3D148_S214_L001_R1_001.fastq  F3D6_S194_L001_R1_001.fastq
F3D141_S207_L001_R2_001.fastq  F3D148_S214_L001_R2_001.fastq  F3D6_S194_L001_R2_001.fastq
F3D142_S208_L001_R1_001.fastq  F3D149_S215_L001_R1_001.fastq  F3D7_S195_L001_R1_001.fastq
F3D142_S208_L001_R2_001.fastq  F3D149_S215_L001_R2_001.fastq  F3D7_S195_L001_R2_001.fastq
F3D143_S209_L001_R1_001.fastq  F3D150_S216_L001_R1_001.fastq  F3D8_S196_L001_R1_001.fastq
F3D143_S209_L001_R2_001.fastq  F3D150_S216_L001_R2_001.fastq  F3D8_S196_L001_R2_001.fastq
F3D144_S210_L001_R1_001.fastq  F3D1_S189_L001_R1_001.fastq    F3D9_S197_L001_R1_001.fastq
F3D144_S210_L001_R2_001.fastq  F3D1_S189_L001_R2_001.fastq    F3D9_S197_L001_R2_001.fastq
F3D145_S211_L001_R1_001.fastq  F3D2_S190_L001_R1_001.fastq    Mock_S280_L001_R1_001.fastq
F3D145_S211_L001_R2_001.fastq  F3D2_S190_L001_R2_001.fastq    Mock_S280_L001_R2_001.fastq
F3D146_S212_L001_R1_001.fastq  F3D3_S191_L001_R1_001.fastq
F3D146_S212_L001_R2_001.fastq  F3D3_S191_L001_R2_001.fastq
```

will produce a file with following content:

```
F3D6_S194	F3D6_S194_L001_R1_001.fastq	F3D6_S194_L001_R2_001.fastq
F3D0_S188	F3D0_S188_L001_R1_001.fastq	F3D0_S188_L001_R2_001.fastq
F3D5_S193	F3D5_S193_L001_R1_001.fastq	F3D5_S193_L001_R2_001.fastq
F3D143_S209	F3D143_S209_L001_R1_001.fastq	F3D143_S209_L001_R2_001.fastq
F3D148_S214	F3D148_S214_L001_R1_001.fastq	F3D148_S214_L001_R2_001.fastq
F3D150_S216	F3D150_S216_L001_R1_001.fastq	F3D150_S216_L001_R2_001.fastq
F3D142_S208	F3D142_S208_L001_R1_001.fastq	F3D142_S208_L001_R2_001.fastq
F3D2_S190	F3D2_S190_L001_R1_001.fastq	F3D2_S190_L001_R2_001.fastq
F3D9_S197	F3D9_S197_L001_R1_001.fastq	F3D9_S197_L001_R2_001.fastq
F3D3_S191	F3D3_S191_L001_R1_001.fastq	F3D3_S191_L001_R2_001.fastq
F3D144_S210	F3D144_S210_L001_R1_001.fastq	F3D144_S210_L001_R2_001.fastq
F3D145_S211	F3D145_S211_L001_R1_001.fastq	F3D145_S211_L001_R2_001.fastq
F3D1_S189	F3D1_S189_L001_R1_001.fastq	F3D1_S189_L001_R2_001.fastq
F3D146_S212	F3D146_S212_L001_R1_001.fastq	F3D146_S212_L001_R2_001.fastq
Mock_S280	Mock_S280_L001_R1_001.fastq	Mock_S280_L001_R2_001.fastq
F3D8_S196	F3D8_S196_L001_R1_001.fastq	F3D8_S196_L001_R2_001.fastq
F3D147_S213	F3D147_S213_L001_R1_001.fastq	F3D147_S213_L001_R2_001.fastq
F3D141_S207	F3D141_S207_L001_R1_001.fastq	F3D141_S207_L001_R2_001.fastq
F3D7_S195	F3D7_S195_L001_R1_001.fastq	F3D7_S195_L001_R2_001.fastq
F3D149_S215	F3D149_S215_L001_R1_001.fastq	F3D149_S215_L001_R2_001.fastq
```

You can specify left and right read sign by using ```--left-reads-sign``` and ```--right-reads-sign```.

mothur_files_creator recognizes the files containing reads by extension. It allows running it in the directory with other files, like metadata. The extension used by default is fastq. You can change it by using ```--files-extension myext```

Since [mothur](https://www.mothur.org/) does not really like hyphens ```-```, these are removed from the file names by default. If you do not like it, use ```--original-names```
