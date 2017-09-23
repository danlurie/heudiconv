import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    
    allowed template fields - follow python string module: 
    
    item: index within category 
    subject: participant id 
    seqitem: run number during scanning
    subindex: sub index within group
    """
    t1w = create_key('anat/sub-{subject}_T1w')
    rest = create_key('func/sub-{subject}_task-rest_bold')
    task = create_key('func/sub-{subject}_task-DistractWM_run-{item:02d}_bold')

    info = {t1w: [], task: [], rest: []}

    for idx, seq in enumerate(seqinfo):
        x,y,z,n_vol,protocol,dcm_dir = (seq[6], seq[7], seq[8], seq[9], seq[12], seq[3])
        # t1_mprage --> T1w
        if (x == 256) and (n_vol == 1) and ('T1 MPRAGE' in protocol):
            info[t1w] = [seq[2]]
        # ep2d_neuro_PA_Task_3mm --> task-DistractWM
        if (x == 70) and (z == 35) and (n_vol == 164) and ('Task' in protocol):
            info[task].append({'item': seq[2]})
        # ep2d_neuro_PA_Rest_3mm --> task-rest
        if (x == 70) and (z == 35) and (n_vol == 300) and ('Rest' in protocol):
            info[rest].append({'item': seq[2]})
        
    return info
