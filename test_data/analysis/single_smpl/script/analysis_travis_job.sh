#!/usr/bin/env bash


#SBATCH --job-name="analysis_travis_job"
#SBATCH --partition=long
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=6
#SBATCH --exclude=gpu[1-8]


###OTU approach analysis###

#Create directories and shorten shared file name

mkdir -p /home/travis/build/dizak/mothulity/test_data/analysis/single_smpl/shared_tax/analysis/OTU/alpha
cp /home/travis/build/dizak/mothulity/test_data/analysis/single_smpl/shared_tax/travis_job.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.agc.unique_list.0.03.pick.shared /home/travis/build/dizak/mothulity/test_data/analysis/single_smpl/shared_tax/analysis/OTU/analysis_travis_job.shared

cp /home/travis/build/dizak/mothulity/test_data/analysis/single_smpl/shared_tax/travis_job.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.agc.unique_list.0.03.pick.0.03.cons.tax.summary /home/travis/build/dizak/mothulity/test_data/analysis/single_smpl/shared_tax/analysis/OTU/alpha/analysis_travis_job.tax.summary


#Go to subdirectory, and subsample shared file

cd /home/travis/build/dizak/mothulity/test_data/analysis/single_smpl/shared_tax/analysis/OTU
mothur '#set.current(processors=1, shared=analysis_travis_job.shared); sub.sample(shared=current)'

#Copy non-subsampled shared file to alpha directory and subsampled shared file to beta directory

cp analysis_travis_job.shared ./alpha


#Go to alpha directory and create krona chart, rarefaction, summary table

cd ./alpha
mothulity_draw analysis_travis_job.tax.summary --output analysis_travis_job.krona.xml  --krona-xml
ktImportXML analysis_travis_job.krona.xml -o analysis_travis_job.krona.html
mothur '#set.current(processors=1, shared=analysis_travis_job.shared); rarefaction.single(shared=current, calc=sobs, freq=100); summary.single(shared=current, calc=nseqs-coverage-sobs-ace-chao-jack-simpson-invsimpson-shannon-npshannon, subsample=T)'
mothulity_draw analysis_travis_job.groups.rarefaction --output analysis_travis_job.raref.html --rarefaction
mothulity_draw analysis_travis_job.groups.summary --output analysis_travis_job.sum.html --summary-table

#Go to OTU directory

cd ../

#Render html output
mothulity /home/travis/build/dizak/mothulity/test_data/analysis/single_smpl/shared_tax/ --render-html --job-name analysis_travis_job

#Go to project's root directory

cd ../../

#Zip the results

zip -r analysis_travis_job.zip analysis/
