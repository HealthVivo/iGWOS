# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 20:34:57 2017

@author: xuedy
"""

import subprocess
import os
from P1_genyaml import genyaml_G, yaml_structure, genyaml_C
from P3_file_upload import get_time
from S2 import site_data_analysis,SITE_ot_2_visl
from S3 import SITE_visualizeOfftargets
from Plt_trans import circle_standard,guide_standard
from circos import circos


def GUIDE_process(args):
    print ('[{0}][INFO][guideseq] reading the input information'.format(get_time()))
    input_infg,parag,parasg,input_labelg = yaml_structure('G')
    input_infg['forward'] = args.read1
    input_infg['reverse'] = args.read2
    input_infg['index1'] = args.index1
    input_infg['index2'] = args.index2
    parag['barcode1'] = args.barcode1
    parag['barcode2'] = args.barcode2 
    parag['c_barcode1'] = args.cbarcode1
    parag['c_barcode2'] = args.cbarcode2
    parag['description'] = args.label
    parag['demultiplex_min_reads']= args.demultiplex_min_reads
    parag['target'] = args.target
    genyaml_G(
            ref = args.reference,
            output_add = args.output,
            label = args.label,
            para = parag,
            input_label = input_labelg,
            input_inf = input_infg,
            )
    print ('[{0}][INFO][guideseq] done'.format(get_time()))
    print ('[{0}][INFO][guideseq] start the process'.format(get_time()))
    cmd = 'python software/guideseq/guideseq/guideseq.py all --manifest run/run.yaml'
    subprocess.call(cmd, executable='/bin/bash', shell=True)
    guide_outcome_f = '{0}/identified/{1}_identifiedOfftargets.txt'.format(args.output, args.label)
    if os.path.exists(guide_outcome_f) == False:
        print('there is something wrong with guideseq program')
        return 0
    else:
        guide_standard(guide_outcome_f, args.output+'/outcome.txt', args.target)
        circos(args.output+'/outcome.txt', args.output)
        return 1

def CIRCLE_process(args):
    print ('[{0}][INFO][circleseq] reading the input information'.format(get_time()))
    input_infg,parag,parasg,input_labelg = yaml_structure('C')
    input_infg['read1'] = args.read1
    input_infg['read2'] = args.read2
    input_infg['controlread1'] = args.cread1
    input_infg['controlread2'] = args.cread2
    input_infg['description'] = args.label
    input_infg['target'] = args.target
    parag['gap_threshold'] = args.gap_threshold
    parag['mapq_threshold'] = args.mapq_threshold
    parag['merged_analysis'] = args.merged_analysis
    parag['mismatch_threshold'] = args.mismatch_threshold
    parag['read_threshold'] = args.read_threshold
    parag['start_threshold'] = args.start_threshold
    parag['window_size'] = args.window_size
    genyaml_C(
            ref = args.reference,
            output_add = args.output,
            label = args.label,
            para = parag,
            paras = parasg,
            input_label = input_labelg,
            input_inf = input_infg,
            )
    print ('[{0}][INFO][circleseq] done'.format(get_time()))
    print ('[{0}][INFO][circleseq] start the process'.format(get_time()))
    cmd = 'python software/circleseq/circleseq/circleseq.py all --manifest run/run.yaml'
    subprocess.call(cmd, executable='/bin/bash', shell=True)
    circle_outcome_f = '{0}/identified/{1}_identified_matched.txt'.format(args.output, args.label)
    if os.path.exists(circle_outcome_f) == False:
        print('there is something wrong with circleseq program')
        return 0
    else:
        circle_standard(circle_outcome_f, args.output+'/outcome.txt', args.target)
        circos(args.output+'/outcome.txt', args.output)
        return 1

    
def SITE_process(args):
    ref_seq = args.target
    offtargets = site_data_analysis(args.read1, args.read2, args.output, args.target, args.reference, args.label)
    visual_data = SITE_ot_2_visl(offtargets,args.target)
    #print(visual_data)
    if not os.path.exists(args.output+'/visualization'):
        os.mkdir(args.output+'/visualization')
    f_n = args.output+'/visualization/'+args.label+'_offtargets'
    SITE_visualizeOfftargets(visual_data, ref_seq, f_n, title=args.label)
    circos(args.output+'/outcome.txt', args.output)
    return 1


    
def process_pack(method):
    pcpk = {'GUIDE-seq':GUIDE_process,
            'CIRCLE-seq':CIRCLE_process,
            'SITE-seq':SITE_process}
    return pcpk[method]
