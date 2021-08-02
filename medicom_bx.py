"""
The module joins 5 biopsy files and parses the biopsy report to get the biopsy result of both breasts.

1. Rename columns to join 5 files
2. Join 5 biopsy files
3. Parse biopsy reports to get the biopsy label (biopsy side, left breast label, right breast label)
4. Sort biopsy results of the left and right breasts in severe order and select the most severe biopsy results as the final label of each breast
"""
import pandas as pd

df_a = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/raw_file/medicom_bx_a.csv', encoding='utf-8-sig', low_memory=False)
df_a2 = pd.read_csv("/Users/lunit/Documents/medicom_script_202107/raw_file/medicom_bx_a2.csv", encoding='utf-8-sig', low_memory=False)
df_b = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/raw_file/medicom_bx_b.csv', encoding='utf-8-sig', low_memory=False)
df_b2 = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/raw_file/medicom_bx_b2.csv', encoding='utf-8-sig', low_memory=False)
df_ge = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/raw_file/medicom_bx_ge.csv', encoding='utf-8-sig', low_memory=False)


def get_biopsy_side(biopsy):
    """
    Return the biopsy side (e.g. both, lt, rt, unknown or ge_unknown)

    Args:
        biopsy reports (str): biopsy report

    Returns:
        str: a single biopsy side or ''
    """
    exam = str(biopsy['exam']).lower()
    biopsy_result = str(biopsy['biopsy_result'])
    ge_biopsy = biopsy['Biopsy Finding (Negative, Benign, Malignant)']

    if 'bilateral' in exam :
        return 'both'
    elif 'left' in exam and 'right' in exam:
        return 'both'
    elif 'left' in exam:
        return 'lt'
    elif 'right' in exam:
        return 'rt'
    elif 'lt' in exam:
        return 'lt'
    elif 'rt' in exam:
        return 'rt'
    elif 'benign' in biopsy_result or 'malignant' in biopsy_result or 'high risk' in biopsy_result:  ##some biopsies don't have the biopsy side information
        return 'unknown'
    elif ge_biopsy != '':
        return 'ge_unknown'  #all of ge biopsies don't have the biopsy side information
    else:
        return ''

def get_left_label(biopsy):
    """
    Return the left breast result (e.g. malignant, high risk or benign)

    Args:
        biopsy reports (str): pathology outcome section:
        biopsy finding (str): biopsy finding (Negative, Benign, Malignant)  #df_ge only

    Returns:
        str: a single left biopsy result or ''
    """
    biopsy_side = biopsy['biopsy_side']
    biopsy_result = biopsy['biopsy_result']
    ge_biopsy = str(biopsy['Biopsy Finding (Negative, Benign, Malignant)']).lower()

    if biopsy_side == 'lt' or biopsy_side == 'both':
        return biopsy_result
    elif biopsy_side == '' and biopsy_result != '':
        return  biopsy_result
    elif biopsy_side == 'unknown':
        return biopsy_result
    elif biopsy_side == 'ge_unknown':
        return ge_biopsy
    else:
        return ''

def get_right_label(biopsy):
    biopsy_side = biopsy['biopsy_side']
    biopsy_result = biopsy['biopsy_result']
    ge_biopsy = str(biopsy['Biopsy Finding (Negative, Benign, Malignant)']).lower()
    """
    Return the right breast result (e.g. malignant, high risk or benign)

    Args:
        biopsy reports (str): pathology outcome section:
        biopsy finding (str): biopsy finding (Negative, Benign, Malignant)  #df_ge only

    Returns:
        str: a single right biopsy result or ''
    """
    if biopsy_side == 'rt' or biopsy_side == 'both':
        return biopsy_result
    elif biopsy_side == '' and biopsy_result != '':
        return  biopsy_result
    elif biopsy_side == 'unknown':
        return biopsy_result
    elif biopsy_side == 'ge_unknown':
        return ge_biopsy
    else:
        return ''

#1. Rename Renaming columns to join 5 Biopsy files into 1 file
df_a2 = df_a2.rename(columns={'bx_report':'reports','Patient_ID':'patientId', 'Representative_Study_Instance_UID':'studyUID'})
df_b2 = df_b2.rename(columns={'bx_report':'reports','Patient_ID':'patientId', 'Representative_Study_Instance_UID':'studyUID'})
df_ge = df_ge.rename(columns={'Patient ID':'patientId','Index Exam Study UID': 'studyUID'})

#2. Join 5 biopsy files
biopsy = pd.concat([df_a, df_a2, df_b, df_b2, df_ge])
biopsy = biopsy.fillna('')

#3. Parse biopsy reports to get the biopsy label (biopsy side, left breast label, right breast label)
biopsy['exam'] = biopsy.reports.str.lower().str.split('exam:').str[1].str.split('accession').str[0].str.strip()
biopsy['biopsy_result'] = biopsy.reports.str.lower().str.split('outcome section:').str[1].str.split('pathology').str[0].str.strip()
biopsy['biopsy_side'] = biopsy.apply(get_biopsy_side, axis=1)
biopsy['left_label'] = biopsy.apply(get_left_label, axis=1)
biopsy['right_label'] = biopsy.apply(get_right_label, axis=1)
biopsy = biopsy[['patientId', 'studyUID', 'completedDate', 'reports','Biopsy Finding (Negative, Benign, Malignant)', 'biopsy_result', 'biopsy_side','left_label', 'right_label']]

#4. Sort biopsy results of the left and right breasts in severe order and select the most severe biopsy results as the final label of each breast
biopsy_lt = biopsy.sort_values(by=['patientId','left_label','completedDate'], ascending=False).fillna('')
biopsy_lt = biopsy_lt[biopsy_lt['left_label'].str.contains('malignant|high risk|benign')].drop_duplicates(subset=['patientId'], keep='first')
biopsy_lt = biopsy_lt.rename(columns={'completedDate' : 'lt_bx_date'})
biopsy_lt = biopsy_lt[['patientId', 'lt_bx_date', 'biopsy_side','left_label']]

biopsy_rt = biopsy.sort_values(by=['patientId','right_label','completedDate'], ascending=False).fillna('')
biopsy_rt = biopsy_rt[biopsy_rt['right_label'].str.contains('malignant|high risk|benign')].drop_duplicates(subset=['patientId'], keep='first')
biopsy_rt = biopsy_rt.rename(columns={'completedDate' : 'rt_bx_date'})
biopsy_rt = biopsy_rt[['patientId', 'rt_bx_date', 'biopsy_side','right_label']]

biopsy_lt.to_csv('/Users/lunit/Documents/medicom_script_202107/medicom_biopsy_parsed_lt.csv')
biopsy_rt.to_csv('/Users/lunit/Documents/medicom_script_202107/medicom_biopsy_parsed_rt.csv')