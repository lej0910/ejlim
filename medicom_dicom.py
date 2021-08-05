"""
The module parses the dicommeta information.
`get` functions try to return the information by searching various dicom tags.
If it cannot find the requested feature, it returns an empty string('')

1. Remove the outliers
2. Parse dicom tags and create new columns
3. Select the best 4-view file per study and count the number of views corresponding to 4 views per study
"""
import pandas as pd
import ast

df = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/raw_file/medicom_dm_1_6.csv', encoding='utf-8-sig', low_memory=False)
df = df.fillna('')

def get_scan_type(df):
    """
    Return the dicom's scan type(e.g. 3D, S2D or 2D)

    Args:
        dicom_metas (list): a list of dicom meta dict

    Returns:
        str: scan type
    """    
    try:
        num_frame = int(df['Number of Frames'])
    except ValueError:
        num_frame = 0
    series_description = df['Series_Description']
    if num_frame > 1:
        return "3D"
    elif 'tomosynthesis' in series_description.lower() or 'ROUTINE3D_VOL' in series_description:
        return "3D"
    elif 'preview' in series_description.lower() or \
            'c-view' in series_description.lower():
        return "S2D"
    else:
        if df['Window Center'] == '' or df['Window Width'] == '':
            return "unused"
        else:
            return "2D"

def get_view_type(df):
    """
    Find out the view type(e.g. RCC) from GE 2D case. Unlike others,
    view type cannot be parsed from the series description, so it utilizes
    the laterality and view position information and plane_orientation in dicom meta.

    Args:
        dicom_meta (dict): dicom meta

    Returns:
        str: view type(e.g. LMLO)
    """   
    sereis_description = df['Series_Description']
    laterality = df['Image Laterality']
    view_position = df['View Position']
    plane_orientation = df['Plane Orientation'].replace("'","")
    views = ['XCCL','XCCM','CC','MLO','LMO','ML','LM']
    for view in views:
        if '_R2' in sereis_description:  # There is no dicom 
            return ''
        elif view in sereis_description:
            return laterality + view
    if '2D_PROC' in sereis_description:
        return laterality + view_position
    elif 'V-Preview' in sereis_description :
        if plane_orientation:
            plane_orientation = ast.literal_eval(plane_orientation)
        else:
            return ''
        laterality = 'R' if int(plane_orientation[1]) == 1 else 'L'
        if abs(plane_orientation[3]) > 1.0:
            return ''
        elif abs(plane_orientation[3]) >= 0.9:
            view_position = 'CC'
        elif abs(plane_orientation[3]) < 0.9:
            view_position = 'MLO'
        return laterality + view_position
    else:
        return ''

def sum_rows_columns(df):
    """
    Return Sum of the Rows and Columns values.
    If one study has multiple duplicate view files, 
    the sum of rows and columns will be used as an element to select one file

    Args:
        dicom_meta (list): dicom meta

    Returns:
        int: sum of Rows and Columns (e.g. 4016)
    """   
    if df['Rows'] != '' and df['Columns'] != '' :
        return int(df['Rows']) + int(df['Columns']) 

def inter_view_type(df):
    """
    Return the 4-view type

    Args:
        dicom_meta (dict): dicom meta

    Returns:
        str: the 4-view type
    """   
    view_type = df['view_type']
    LCC = 'LCC|LXCCL|LXCCM'
    RCC = 'RCC|RXCCL|RXCCM'
    LMLO = 'LMLO|LLM|LML|LLMO'
    RMLO = 'RMLO|RLM|RML|RLMO'

    if view_type != '':
        if view_type in LCC :
            return 'LCC'
        elif view_type in RCC :
            return 'RCC'
        elif view_type in LMLO :
            return 'LMLO'
        elif view_type in RMLO :
            return 'RMLO'
        else:
            return ''

def get_view_priority(df):
    """
    Returns the view priority.
    Standard 4-view and additional view take precedence over standard 4-view.

    Args:
        dicom_meta (dict): dicom meta

    Returns:
        int: 1 or 2
    """   
    view_type = df['view_type']
    first = 'LCC|RCC|LMLO|RMLO'

    if view_type != '' :
        if view_type in first :
            return int(2)  # To select standard 4-view by applying Ascending = "False"
        else:
            return int(1)

def get_group(df):
    """
    Return group information

    Args:
        dicom_meta (list): dicom meta

    Returns:
        str: a single letter group name or ''
    """   
    path = df['Path']

    if 'Group A' in path:
        return 'A'
    elif 'Group B' in path:
        return 'B'
    elif 'Group C' in path:
        return 'C'
    elif 'Group D' in path:
        return 'D'
    else :
        return ''


#1. Remove the outliers
df = df.loc[(df['View Modifier Code Sequence Meaning'] == '') &
                (df['Patient_Sex'] != 'M') &
                (df['Presentation Intent Type'] != 'FOR PROCESSING')&
                (df['Estimated Radiographic Magnification Factor'].replace('', 0) < 1.5)&
                (df['Breast Implant Present'] != 'YES')&
                (df['Study_Description'].str.contains('STEREOTACTIC|SPECIMEN')!= True)]

#2. Parse dicom tags and create new columns
df['group'] = df.apply(get_group, axis=1)
df["scan_type"] = df.apply(get_scan_type, axis=1)
df["view_type"] = df.apply(get_view_type, axis=1)
df["4view_type"] = df.apply(inter_view_type, axis=1)
df["view_priority"] = df.apply(get_view_priority, axis=1)
df["resolution"] = df.apply(sum_rows_columns, axis=1)

#3. Select the best 4-view file per study and count the number of views corresponding to 4 views per study
df['duplication'] = df['Study_Instance_UID'] + "_" + df['scan_type'] + "_" + df['4view_type'] + '_' + df['Manufacturer_Model_Name']
df = df.loc[(df['view_type'] != '') & (df['4view_type'] != '')].sort_values(by=['duplication', 'view_priority','Number of Frames']).drop_duplicates(subset=['duplication'], keep = 'last')
df['unique_id'] = df['Study_Instance_UID'] + '_' + df['scan_type'] + '_' + df['Manufacturer_Model_Name']
df['view_count'] = df.groupby(['unique_id'])['unique_id'].transform('count')

df = df[['Patient_ID',	
    'Study_Instance_UID',
    'Manufacturer',
    'Manufacturer_Model_Name', 
    'Study_Date', 
    'Patient_Sex', 
    'Patient_Birth_Date', 
    'SOP Instance UID', 
    'Frame of Reference UID', 
    'Path', 
    'group', 
    'scan_type',
    '4view_type',
    'unique_id',
    'view_count']]

df.to_csv('/Users/lunit/Documents/medicom_script_202107/medicom_dicom_parsed.csv')

