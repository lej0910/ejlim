"""
The module parses the dicommeta information.
`get` functions try to return the information by searching various dicom tags.
If it cannot find the requested feature, it returns an empty string('')

1. Change the DICOM meta table from view unit to study unit and combine file path with the corresponding table.
2. Merges left biopsy and right biopsy results from biopsy reports into a DICOM meta table.
3. Merges Birads and density from radiology reports into a DICOM meta table.
4. Get the biopsy time interval using the study date and biopsy date
5. Creates new columns and leaves only studies that meet the requirements.
6. Select an index study.(index_select is true, view_count is high, and study date is most recent study) 
7. classify Non-index studies as pre-index or post-index based on the index date.
"""
import pandas as pd
from datetime import datetime


dicom = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/medicom_dicom_parsed.csv', encoding='utf-8-sig', low_memory=False)
biopsy_lt = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/medicom_biopsy_parsed_lt.csv', encoding='utf-8-sig', low_memory=False)
biopsy_rt = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/medicom_biopsy_parsed_rt.csv', encoding='utf-8-sig', low_memory=False)
mg_report = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/medicom_report_parsed.csv', encoding='utf-8-sig', low_memory=False)


def change_group_c(dicom):
    """
    Change group D with birads of 2 or 3 to group C.

    Args:
        dicom_metas (list): dicom_metas

    Returns:
        str: a single letter group name
    """  
    group = dicom['group']
    birads = dicom['birads']

    if group == 'C':
        if birads == '2' or birads == '3':
            return 'D'
        else:
            return 'C'
    else:
        return group

def get_study_label(dicom):
    """
    Return the study label(e.g. malignant)

    Args:
        dicom_meta (dict): dicom meta

    Returns:
        str: study label
    """
    left_label = dicom['left_label']
    right_label = dicom['right_label']

    if 'malignant' in left_label or 'malignant' in right_label:
        return 'malignant'
    elif 'high risk' in left_label or 'high risk' in right_label:
        return 'high risk'
    elif 'benign' in left_label or 'benign' in right_label:
        return 'benign'
    else:
        return 'NA'

def devide_accept_reject(dicom):
    """
    Return Whether the conditions by group match

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: If true, accept, otherwise reject.
    """
    group = dicom['group']
    study_label = dicom['study_label']
    reports = str(dicom['reports']).lower()

    if 'mammo' in reports :
        if group == 'A' and study_label == 'malignant':
            return 'accept'
        elif group == 'B' and study_label == 'benign' :
            return 'accept'
        elif group == 'B' and study_label == 'high risk' :
            return 'accept'
        elif group == 'C' and study_label == 'NA' :
            return 'accept'
        elif group == 'D' and study_label != 'malignant' :
            return 'accept'
        else:
            return 'reject'
    else:
        return 'reject'

def get_bx_label_lt(dicom):
    """
    Returns left biopsy results that meet the time interval condition. only group a and b.

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: left biopsy result
    """
    group = str(dicom['group'])
    left_label = str(dicom['left_label'])
    interval_lt = dicom['interval_lt']

    if group == 'A' and 'malignant' in left_label :
        if interval_lt < 0 or interval_lt > 365 :
            return ''
        else:
            return 'malignant'

    elif group == 'B' and 'high risk' in left_label :
        if interval_lt < 0 or interval_lt > 365 :
            return ''
        else:
            return 'high risk'

    elif group == 'B' and 'benign' in left_label :
        if interval_lt < 0 or interval_lt > 365 :
            return ''
        else:
            return 'benign'

def get_bx_label_rt(dicom):
    """
    Returns right biopsy results that meet the time interval condition. only group a and b.

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: right biopsy result
    """
    group = str(dicom['group'])
    right_label = str(dicom['right_label'])
    interval_rt = dicom['interval_rt']

    if group == 'A' and 'malignant' in right_label :
        if interval_rt < 0 or interval_rt > 365 :
            return ''
        else:
            return 'malignant'

    elif group == 'B' and 'high risk' in right_label :
        if interval_rt < 0 or interval_rt > 365 :
            return ''
        else:
            return 'high risk'

    elif group == 'B' and 'benign' in right_label :
        if interval_rt < 0 or interval_rt > 365 :
            return ''
        else:
            return 'benign'

def get_bx_study(dicom):
    """
    Returns study result that meet the time interval condition. only group a and b.

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: study result
    """
    left_bx = dicom['left_bx']
    right_bx = dicom['right_bx']

    if left_bx == 'malignant' or right_bx == 'malignant':
        return 'malignant'
    elif left_bx == 'high risk' or right_bx == 'high risk':
        return 'high risk'
    elif left_bx == 'benign' or right_bx == 'benign':
        return 'benign'
    else:
        return ''

def get_index_study(dicom):
    """
    Returns whether the study meets the requirements for each group.

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: If true, 'available', otherwise 'unavailable'.
    """
    select = dicom['select']
    group = dicom['group']
    study_bx = dicom['study_bx']
    study_label = dicom['study_label']
    
    if select == 'accept':
        if group == 'A' and study_bx == 'malignant':
            return 'available'
        elif group == 'B' and study_bx == 'high risk':
            return 'available'
        elif group == 'B' and study_bx == 'benign':
            return 'available'
        elif group == 'C' and study_label == 'NA':
            return 'available'
        elif group == 'D' and study_label != 'malignant':
            return 'available'
        else:
            return 'unavailable'

def get_index_type(dicom):
    """
    Returns the index type

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: index type
    """
    study_date = dicom['Study_Date']
    index_date = dicom['index_date']
    group = dicom['group']
    lt_bx_date = dicom['lt_bx_date']
    rt_bx_date = dicom['rt_bx_date']
    left_label = dicom['left_label']
    right_label = dicom['right_label']
    study_date = dicom['Study_Date']


    if study_date == index_date :
        return '1-index'
    elif study_date < index_date :
        return '2-pre_index'
    elif study_date > index_date : 
        return '3-post_index'
    else:
        if group == 'A':
            if 'malignant' in left_label and 'malignant' in right_label:
                if lt_bx_date >= rt_bx_date:
                    if lt_bx_date > study_date:
                        return '4-pre_bx'
                    else:
                        return '5-post_bx'
                elif lt_bx_date < rt_bx_date:
                    if rt_bx_date > study_date:
                        return '4-pre_bx'
                    else:
                        return '5-post_bx'
            elif 'malignant' in left_label and 'malignant' not in right_label:
                if lt_bx_date > study_date:
                    return '4-pre_bx'
                else:
                    return '5-post_bx'
            elif 'malignant' in right_label and 'malignant' not in left_label:
                if rt_bx_date > study_date:
                    return '4-pre_bx'
                else:
                    return '5-post_bx'

        if group == 'B':
            benigns = ['benign', 'high risk']
            for benign in benigns:
                if benign in left_label and benign in right_label : 
                    if lt_bx_date >= rt_bx_date:
                        if lt_bx_date > study_date:
                            return '4-pre_bx'
                        else:
                            return '5-post_bx'
                    elif lt_bx_date < rt_bx_date:
                        if rt_bx_date > study_date:
                            return '4-pre_bx'
                        else:
                            return '5-post_bx'
                elif benign in left_label and benign not in right_label :
                    if lt_bx_date > study_date:
                        return '4-pre_bx'
                    else:
                        return '5-post_bx'
                elif benign in right_label and benign not in left_label :
                    if rt_bx_date > study_date:
                        return '4-pre_bx'
                    else:
                        return '5-post_bx'

def get_index_interval_day(dicom):
    """
    Returns the time interval between index study and study date

    Args:
        dicom_meta (list): dicom meta

    Returns:
        day: time interval 
    """
    index_interval_day = dicom['index_interval_day']
    group = dicom['group']
    study_date = dicom['Study_Date']
    lt_bx_date = dicom['lt_bx_date']
    rt_bx_date = dicom['rt_bx_date']
    left_label = dicom['left_label']
    right_label = dicom['right_label']
    study_date = dicom['Study_Date']


    if index_interval_day != '' :
        return index_interval_day
    else:
        if group == 'A':
            if 'malignant' in left_label and 'malignant' in right_label:
                if lt_bx_date >= rt_bx_date:
                    return (study_date - lt_bx_date).days
                else:
                    return (study_date - rt_bx_date).days
            elif 'malignant' in left_label and 'malignant' not in right_label:
                return (study_date - lt_bx_date).days
            elif 'malignant' in right_label and 'malignant' not in left_label:
                return (study_date - rt_bx_date).days

        if group == 'B':
            benigns = ['benign', 'high risk']
            for benign in benigns:
                if benign in left_label and benign in right_label : 
                    if lt_bx_date >= rt_bx_date:
                        return (study_date - lt_bx_date).days
                    else:
                        return (study_date - rt_bx_date).days
                elif benign in left_label and benign not in right_label :
                    return (study_date - lt_bx_date).days
                elif benign in right_label and benign not in left_label :
                    return (study_date - rt_bx_date).days

def get_index_interval_category(dicom):
    """
    Returns the time interval category from 1 to 5_over

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: time interval category
    """
    index_interval_day = abs(dicom['index_interval_day'])

    if index_interval_day == 0:
        return 0
    elif index_interval_day > 0 and index_interval_day <= 365 :
        return 1
    elif index_interval_day > 365 and index_interval_day <= 730 :
        return 2
    elif index_interval_day > 730 and index_interval_day <= 1095 :
        return 3
    elif index_interval_day > 1095 and index_interval_day <= 1460 :
        return 4
    elif index_interval_day > 1460 and index_interval_day <= 1825 :
        return 5
    else:
        return '5_over'

def change_lt_label(dicom):
    """
    Returns the left breast label (e.g. malignant, high risk, benign)

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: the left breast label
    """
    biopsy_side_lt = dicom['biopsy_side_lt']
    left_label = dicom['left_label']

    if 'unknown' in biopsy_side_lt:
        return ''
    elif 'malignant' in left_label:
        return 'malignant'
    elif 'high risk' in left_label:
        return 'high risk'
    elif 'benign' in left_label:
        return 'benign'
    else:
        return ''

def change_rt_label(dicom):
    """
    Returns the right breast label (e.g. malignant, high risk, benign)

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: the right breast label
    """
    biopsy_side_rt = dicom['biopsy_side_rt']
    right_label = dicom['right_label']

    if 'unknown' in biopsy_side_rt:
        return ''
    elif 'malignant' in right_label:
        return 'malignant'
    elif 'high risk' in right_label:
        return 'high risk'
    elif 'benign' in right_label:
        return 'benign'
    else:
        return ''

#1. Change the DICOM meta table from view unit to study unit and combine file path with the corresponding table.
dicom_path = pd.pivot_table(dicom, index ='unique_id', columns='4view_type', values='Path', aggfunc='first')
dicom = dicom.drop_duplicates(subset=['unique_id'], keep = 'first')
dicom = pd.merge(dicom, dicom_path, on='unique_id', how='left')

#2. Merges left biopsy and right biopsy results from biopsy reports into a DICOM meta table.
dicom.rename(columns={'Patient_ID':'patientId'}, inplace=True)
dicom = pd.merge(dicom, biopsy_lt, on='patientId', how='left')
dicom = pd.merge(dicom, biopsy_rt, on='patientId', how='left').fillna('')

#3. Merges Birads and density from radiology reports into a DICOM meta table.
dicom = pd.merge(dicom, mg_report, on='Study_Instance_UID', how='left')

#4. Get the biopsy time interval using the study date and biopsy date
dicom = dicom.astype({'Study_Date': 'str', 'Patient_Birth_Date': 'str'})
dicom['Patient_Birth_Date'] = pd.to_datetime(dicom['Patient_Birth_Date'].str[:4] + '/' + dicom['Patient_Birth_Date'].str[4:6] + '/'+ dicom['Patient_Birth_Date'].str[6:8], format='%Y-%m-%d', errors='coerce')
dicom['Study_Date'] = pd.to_datetime(dicom['Study_Date'].str[:4] + '/' + dicom['Study_Date'].str[4:6] + '/'+ dicom['Study_Date'].str[6:8], format='%Y-%m-%d', errors='coerce')
dicom['lt_bx_date'] = pd.to_datetime(dicom['lt_bx_date'], format='%Y-%m-%d', errors='ignore')
dicom['rt_bx_date'] = pd.to_datetime(dicom['rt_bx_date'], format='%Y-%m-%d', errors='ignore')
dicom['Patient_Age'] = round((dicom['Study_Date'] - dicom['Patient_Birth_Date']).dt.days/365)
dicom['interval_lt'] = (dicom['lt_bx_date']-dicom['Study_Date']).dt.days
dicom['interval_rt'] = (dicom['rt_bx_date']-dicom['Study_Date']).dt.days

#5. Creates new columns and leaves only studies that meet the requirements.
dicom['group'] = dicom.apply(change_group_c, axis=1)
dicom['study_label'] = dicom.apply(get_study_label, axis=1)
dicom['select'] = dicom.apply(devide_accept_reject, axis=1)
dicom['left_bx'] = dicom.apply(get_bx_label_lt, axis=1)
dicom['right_bx'] = dicom.apply(get_bx_label_rt, axis=1)
dicom['study_bx'] = dicom.apply(get_bx_study, axis=1)
dicom['index_select'] = dicom.apply(get_index_study, axis=1)
dicom = dicom.loc[dicom['select']=='accept']

#6. Select an index study.(index_select is true, view_count is high, and study date is most recent study) 
dicom['pid+scan_type'] = dicom['patientId'] + "_" + dicom['scan_type']
dicom = dicom.sort_values(by=['group', 'pid+scan_type', 'index_select', 'view_count', 'Study_Date'], ascending=[True, True, True, False, False])
dicom_index = dicom.loc[dicom['index_select']=='available'].drop_duplicates(subset=['pid+scan_type'], keep = 'first')
dicom_index = dicom_index[['pid+scan_type', 'Study_Date']]
dicom_index.rename(columns={'Study_Date':'index_date'}, inplace=True)

#7. classify Non-index studies as pre-index or post-index based on the index date.
dicom = pd.merge(dicom, dicom_index, on='pid+scan_type', how='left')
dicom['index'] = dicom.apply(get_index_type, axis=1)
dicom['index_date'] = pd.to_datetime(dicom['index_date'], format='%Y-%m-%d', errors='ignore')
dicom['index_interval_day'] = (dicom['Study_Date']-dicom['index_date']).dt.days
dicom = dicom.fillna('')
dicom['index_interval_day'] = dicom.apply(get_index_interval_day, axis=1)
dicom['index_interval_category'] = dicom.apply(get_index_interval_category, axis=1)
dicom['left_label'] = dicom.apply(change_lt_label, axis=1)
dicom['right_label'] = dicom.apply(change_rt_label, axis=1)



dicom = dicom.rename(columns=
{'group' : 'Group',
'patientId' : 'Patient_ID',
'Study_Instance_UID' : 'Study_Instance_UID',
'Manufacturer' : 'Manufacturer',
'Manufacturer_Model_Name' : 'Manufacturer_Model_Name',
'Study_Date' : 'Study_Date',
'scan_type' : 'Scan_Type',
'index' : 'Exam_type',
'birads' : 'BIRADS',
'density' : 'Density',
'LCC' : 'LCC_Path',
'LMLO' : 'LMLO_Path',
'RCC' : 'RCC_Path',
'RMLO' : 'RMLO_Path',
'view_count' : 'View_Count',
'lt_bx_date' : 'Left_Bx_Date',
'rt_bx_date' : 'Right_Bx_Date',
'left_bx' : 'Biopsy_Left',
'right_bx' : 'Biopsy_Right',
'study_bx' : 'Study_Label'})

dicom = dicom[[
'Group',
'Patient_ID',
'Patient_Age',
'Study_Instance_UID',
'Manufacturer',
'Manufacturer_Model_Name',
'Study_Date',
'Scan_Type',
'Exam_type',
'index_interval_day',
'index_interval_category',
'BIRADS',
'Density',
'LCC_Path',	
'LMLO_Path',	
'RCC_Path',
'RMLO_Path',
'View_Count',
'left_label',
'right_label',
'study_label',]]

dicom.to_csv('/Users/lunit/Documents/medicom_script_202107/medicom_merged.csv')