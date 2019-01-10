# iGWOS
**i**ntegrated **G**enome-**W**ide **O**ff-target cleavage **S**earch

## Introduction
iGWOS is designed specifically for an integrate analysis of the high-throughput sequencing data generated from various mainstream CRISPR/SpCas9 off-target detection techniques, as well as for optimal OTS prediction by aggregating the available OTS prediction tools in a complementary way.   
* Current data processing supports three OTS detection techniques (GUIDE-seq, CIRCLE-seq, and SITE-seq).  
* Current integrate method iGWOS, by aggregating CFD and DeepCRISPR, supports conventional NGG-PAM OTS prediction with mismatches up to 6.

# the NGS data processing on OTS Detection

## Requirement

* HTSeq == 0.6.1    
* PyYAML == 3.11    
* swalign == 0.3.1  
* pyfaidx == 0.2.7  
* svgwrite == 1.1.6     
* regex == 2016.07.21   
* numpy == 1.11.1   
* nwalign == 0.3.1  
* statsmodels == 0.6.1  
* pysam == 0.9.1.4 

## Usage
	python [option0] {GUIDE-seq,CIRCLE-seq,SITE-seq} [option1]
	
#### option0:    
    -h --help :
        show the help message
    -UID:
        user id, necessary is -U is True, for the determination of data source
    -D:
        description of sgRNA
    -U:
        if you are willing to upload part of your data and share them to all the researchers of CRIPSR
    -O:
        output folder
    -L:
        the name of CRISPR/Cas which you use in the experiment
    -r1:
        treated sequencing data 1, it need to be noticed that different methods require different types of input data
    -r2:
        treated sequencing data 2, if sequencing data is single-end, read1 is only necessary
        
#### option1:
   option1 is different when chosing different experiment method
    
>when chosing GUIDE-seq   

    -m:
        DO NOT FILL ANY VALUE FOR THIS PARAMETER
    -F:
        /path/to/reference_genome.fa
    -R:
        target sequence including PAM
    -bar1:
        barcode 1, 
        necessary
    -bar2:
        barcode 2,
        necessary
    -cbar1:
        control barcode 1, 
        necessary
    -cbar2:
        control barcode 2, 
        necessary
    -ind1:
        index 1, 
        necessary
    -ind2:
        index 2, 
        necessary
    --d-minreads:
        demultiplex_min_reads, 
        necessary with default 1000
			
>when chosing CIRCLE-seq   

    -m:
        DO NOT FILL ANY VALUE FOR THIS PARAMETER
    -F:
        /path/to/reference_genome.fa
    -R:
        target sequence including PAM
    -cr1:
        control sequencing data 1
        necessary
    -cr2:
        control sequencing data 2
        necessary
    -rt:
        The minimum number of reads at a location for that location to be called as a site, 
        necessary and with default 4
    -ws:
        size of the sliding window, 
        necessary and with default 3
    -mqt:
        Minimum read mapping quality score, 
        necessary and with default 50
    -st:
        Tolerance for breakpoint location, 
        necessary and with default 1
    -gt:
        Number of tolerated gaps in the fuzzy target search step, 
        necessary and with default 3
    -mt:
        Number of tolerated gaps in the fuzzy target search setp, 
        necessary and with default 6
    -ma:
        Whether or not the paired read merging step should takingTrue, 
        necessary and with default True
		
>when chosing SITE-seq  

    -m:
        DO NOT FILL ANY VALUE FOR THIS PARAMETER
    -F:
        /path/to/reference_genome.fa
    -R:
        target sequence including PAM
					
>Example  

    python Plt_main.py 
        -UID test_OTS
        -D EMX_site1
        -U false
        -O test_ouput/
        -L test_0 
        -r1 guideseq/test/data/undemultiplexed/undemux.r1.fastq 
        -r2 guideseq/test/data/undemultiplexed/undemux.r2.fastq
        GUIDE-seq 
        -F guideseq/test/test_genome.fa 
        -R GAGTCCGAGCAGAAGAAGAANGG
        -bar1 TAGGCATG
        -bar2 TAGATCGC
        -cbar1 CTCTCTAC
        -cbar2 CTCTCTAT
        -ind1 guideseq/test/data/undemultiplexed/undemux.i1.fastq
        -ind2guideseq/test/data/undemultiplexed/undemux.i2.fastq

# OTS Prediction
Predict CRISPR/Cas9 off-target sites by integrating CFD and DeepCRISPR.
The genome encode can be referred to DeepCRISPR (https://github.com/bm2-lab/DeepCRISPR)


## Requirement
* python == 3.6   
* pandas == 0.20.1  
* numpy == 1.14.5   
* pyfaidx == 0.4.8.4    
* tensorflow == 1.8.0  
* sonnet == 1.9

## Usage
    python main.py [-h] [--version] [-g GENOME] [-m {0,1,2,3,4,5}] [-gpu GPU]
             [-e ENCODE] [-o OUTPUT]
             gRNA cell cid

    Prediction of CRISPR-Cas9 off-target sites with iGWOS.
    
    positional arguments:
      gRNA              input your gRNA file, formed like data/gRNA.tab
      cell              the cell-type of performed gRNAs
      cid               the cell-id encode file, formed like data/encode_hg19.tab
    
    optional arguments:
      -h, --help        show this help message and exit
      --version         show program's version number and exit
      -g GENOME         the genome folder for candidate off-target searching,
                        default=genome/hg19
      -m {0,1,2,3,4,5}  the maximum mismatch allowed in off-target prediction,
                        default=5
      -gpu GPU          select a gpu device to perform cas-offinder and
                        deepcrispr, default=0
      -e ENCODE         the encode folder, default=/home/data/encode
      -o OUTPUT         the output folder, default=data
      
>Example  
    
    python main.py -g genome/hg19 -m 5 -gpu 0 -e /home/data/encode -o data data/gRNA.tab K562 data/encode_hg19.tab

>gRNA file format     

    sgID	gRNA	Chr	Strand	Start
    HBB	CTTGCCCCACAGGGCAGTAACGG	chr11	+	5248198
    FANCF	GGAATCCCTTCTGCAGCACCTGG	chr11	-	22647332
>cell encode file format    

    h1	MCF-7
    h2	GM12878
    h3	HepG2
    h4	LNCaP clone FGC
    h5	HCT116
    h6	HeLa-S3
    h7	K562