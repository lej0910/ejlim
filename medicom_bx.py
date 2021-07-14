import pandas as pd

df = pd.read_csv('/Users/lunit/Documents/medicom_test/medicom_a.csv', encoding = 'utf-8-sig', low_memory= False)



def get_exam(df):
    report = df['reports'].lower()

    if report != '':
        try:
            exam = report.split('exam:')[1].split('accession')[0]
            return exam
        except:
            return 'na'



# def get_biopsy_result(df):
#     report = df['reports'].lower()

#     if report != '':
#         try:
#             biopsy_result = report.split('pathology outcome section:')[1].split('pathology result section')[0]
#             return biopsy_result
#         except:
#             return 'na'


# def get_biopsy_side(df):
#     exam = df['exam']


#     if 'bilateral' in exam :
#         return 'both'
#     elif 'left' in exam :
#         return 'lt'
#     elif 'right' in exam :
#         return 'rt'
#     else:
#         return 'unknown'
    



df['exam'] = df.apply(get_exam, axis=1)
# df['biopsy_result'] = df.apply(get_biopsy_result, axis=1)
# df['biopsy_side'] = df.apply(get_biopsy_side, axis=1)


df.to_csv('/Users/lunit/Documents/medicom_test/medicom_bx.csv')
