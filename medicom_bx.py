import pandas as pd


'''
df_a
'''
df_a = pd.read_csv('/Users/lunit/Documents/medicom_test/medicom_bx_file/medicom_a.csv', encoding='utf-8-sig', low_memory=False)

def get_biopsy_side(df_a):
    exam = str(df_a['exam']).lower()

    if exam != '' :
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
        else:
            return ''


def get_left_label(df_a):
    biopsy_result = df_a['biopsy_result']
    side = df_a['biopsy_side']

    if side == 'both':
        return biopsy_result
    elif side == 'lt':
        return biopsy_result 
    else:
        return ''


def get_right_label(df_a):
    biopsy_result = df_a['biopsy_result']
    side = df_a['biopsy_side']

    if side == 'both':
        return biopsy_result
    elif side == 'rt':
        return biopsy_result
    else:
        return ''


df_a = df_a.dropna(subset=['reports'])
df_a['exam'] = df_a.reports.str.lower().str.split('exam:').str[1].str.split('accession').str[0].str.strip()
df_a['biopsy_result'] = df_a.reports.str.lower().str.split('outcome section:').str[1].str.split('pathology').str[0].str.strip()
df_a['biopsy_side'] = df_a.apply(get_biopsy_side, axis=1)
df_a['left_label'] = df_a.apply(get_left_label, axis=1)
df_a['right_label'] = df_a.apply(get_right_label, axis=1)

df_a.to_csv('/Users/lunit/Documents/medicom_test/medicom_bx_file/medicom_bx_a.csv')



'''
df_a2
'''
df_a2 = pd.read_csv("/Users/lunit/Documents/medicom_test/medicom_bx_file/medicom_a2.csv", encoding='utf-8-sig', low_memory=False)


def get_biopsy_side2(df_a2):
    exam = str(df_a2['exam']).lower()

    if exam != '' :
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
        else:
            return ''



def get_left_label2(df_a2):
    biopsy_result = df_a2['biopsy_result']
    side = df_a2['biopsy_side']

    if side == 'both':
        return biopsy_result
    elif side == 'lt':
        return biopsy_result 
    else:
        return ''



def get_right_label2(df_a2):
    biopsy_result = df_a2['biopsy_result']
    side = df_a2['biopsy_side']

    if side == 'both':
        return biopsy_result
    elif side == 'rt':
        return biopsy_result
    else:
        return ''


df_a2 = df_a2.rename(columns={'bx_report':'reports','Patient_ID':'patientId', 'Representative_Study_Instance_UID':'studyUID'}).dropna(subset=['reports'])
df_a2['exam'] = df_a2.reports.str.lower().str.split('exam:').str[1].str.split('accession').str[0].str.strip()
df_a2['biopsy_result'] = df_a2.reports.str.lower().str.split('outcome section:').str[1].str.split('pathology').str[0].str.strip()
df_a2['biopsy_side'] = df_a2.apply(get_biopsy_side2, axis=1)
df_a2['left_label'] = df_a2.apply(get_left_label2, axis=1)
df_a2['right_label'] = df_a2.apply(get_right_label2, axis=1)



'''
df_b
'''
df_b = pd.read_csv('/Users/lunit/Documents/medicom_test/medicom_bx_file/medicom_b.csv', encoding='utf-8-sig', low_memory=False)


def get_biopsy_side3(df_b):
    exam = str(df_b['exam']).lower()

    if exam != '' :
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
        else:
            return ''



def get_left_label3(df_b):
    biopsy_result = df_b['biopsy_result']
    side = df_b['biopsy_side']

    if side == 'both':
        return biopsy_result
    elif side == 'lt':
        return biopsy_result 
    else:
        return ''



def get_right_label3(df_b):
    biopsy_result = df_b['biopsy_result']
    side = df_b['biopsy_side']

    if side == 'both':
        return biopsy_result
    elif side == 'rt':
        return biopsy_result
    else:
        return ''


df_b = df_b.rename(columns={'examDescription':'exam'}).dropna(subset=['reports'])
df_b['biopsy_result'] = df_b.reports.str.lower().str.split('outcome section:').str[1].str.split('pathology').str[0].str.strip()
df_b['biopsy_side'] = df_b.apply(get_biopsy_side3, axis=1)
df_b['left_label'] = df_b.apply(get_left_label3, axis=1)
df_b['right_label'] = df_b.apply(get_right_label3, axis=1)



'''
df_b2
'''
df_b2 = pd.read_csv('/Users/lunit/Documents/medicom_test/medicom_bx_file/medicom_b2.csv', encoding='utf-8-sig', low_memory=False)

def get_biopsy_side4(df_b2):
    exam = str(df_b2['exam']).lower()

    if exam != '' :
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
        else:
            return ''


def get_left_label4(df_b2):
    biopsy_result = df_b2['biopsy_result']
    side = df_b2['biopsy_side']

    if side == 'both':
        return biopsy_result
    elif side == 'lt':
        return biopsy_result 
    else:
        return ''


def get_right_label4(df_b2):
    biopsy_result = df_b2['biopsy_result']
    side = df_b2['biopsy_side']

    if side == 'both':
        return biopsy_result
    elif side == 'rt':
        return biopsy_result
    else:
        return ''


df_b2 = df_b2.rename(columns={'bx_report':'reports','Patient_ID':'patientId', 'Representative_Study_Instance_UID':'studyUID'}).dropna(subset=['reports'])
df_b2['exam'] = df_b2.reports.str.lower().str.split('exam:').str[1].str.split('accession').str[0].str.strip()
df_b2['biopsy_result'] = df_b2.reports.str.lower().str.split('outcome section:').str[1].str.split('pathology').str[0].str.strip()
df_b2['biopsy_side'] = df_b2.apply(get_biopsy_side4, axis=1)
df_b2['left_label'] = df_b2.apply(get_left_label4, axis=1)
df_b2['right_label'] = df_b2.apply(get_right_label4, axis=1)



'''
df_ge
'''
df_ge = pd.read_csv('/Users/lunit/Documents/medicom_test/medicom_bx_file/GE Case Reference Spreadsheet (CSV).csv', encoding='utf-8-sig', low_memory=False)

df_ge['patientId'] = df_ge['Patient ID']
df_ge['studyUID'] = df_ge['Index Exam Study UID']
df_ge['biopsy_result'] = df_ge['Biopsy Finding (Negative, Benign, Malignant)']
df_ge['biopsy_side'] = 'unknown'
df_ge['left_label'] = df_ge['Biopsy Finding (Negative, Benign, Malignant)']
df_ge['right_label'] = df_ge['Biopsy Finding (Negative, Benign, Malignant)']




'''
merge_biopsy
'''
biopsy = pd.concat([df_a, df_a2, df_b, df_b2, df_ge])
biopsy = biopsy.sort_values(by=['patientId','biopsy_result','completedDate'], ascending=False)

biopsy.to_csv('/Users/lunit/Documents/medicom_test/medicom_bx_file/medicom_bx_concat.csv')

