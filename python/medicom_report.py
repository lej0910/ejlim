"""
The module parses the radiology report to get density and birads category.

1. Create new columns 'density' and 'birads'
2. Drop duplicated reports and remove unused columns
"""
import pandas as pd

report = pd.read_csv('/Users/lunit/Documents/medicom_script_202107/raw_file/medicom_reports.csv', encoding='utf-8-sig')


def get_density(report):

    reports = report['reports'].lower()
    
    if 'mammo' in reports :
        if 'extremely dense' in reports :
            return 'D'
        elif 'heterogeneously dense' in reports:
            return 'C'
        elif 'scattered fibroglandular' in reports :
            return 'B'
        elif 'entirely fatty' in reports or 'predominantly fatty' in reports :
            return 'A'
        else:
            return ''
    else:
        return ''

def get_birads(report):

    reports = report['reports'].lower()

    if 'birads: 6' in reports or 'category: 6' in reports or 'category 6' in reports:
        return '6'
    elif 'birads: 5' in reports or 'category: 5' in reports or 'category 5' in reports :
        return '5'
    elif 'birads: 4c' in reports or 'category: 4c' in reports or 'category 4c' in reports :
        return '4c'
    elif 'birads: 4b' in reports or 'category: 4b' in reports or 'category 4b' in reports :
        return '4b'
    elif 'birads: 4a' in reports or 'category: 4a' in reports or 'category 4a' in reports :
        return '4a'
    elif 'birads: 4' in reports or 'category: 4' in reports or 'category 4' in reports :
        return '4'
    elif 'birads: 3' in reports or 'category: 3' in reports or 'category 3' in reports :
        return '3'
    elif 'birads: 2' in reports or 'category: 2' in reports or 'category 2' in reports :
        return '2'
    elif 'birads: 1' in reports or 'category: 1' in reports or 'category 1' in reports :
        return '1'
    elif 'birads: 0' in reports or 'category: 0' in reports or 'category 0' in reports :
        return '0'
    elif ': - benign' in reports:
        return '2'
    elif ': - probably benign' in reports:
        return '2'
    elif ': - negative' in reports:
        return '1'   
    else:
        return ''

def select(report):
    density = report['density']
    birads = report['birads']

    if density != '' and birads != '':
        return 'accept'
    else:
        return 'reject'

#1. Create new columns 'density' and 'birads'
report['density'] = report.apply(get_density, axis=1)
report['birads'] = report.apply(get_birads, axis=1)
report['select'] = report.apply(select, axis=1)

#2. Drop duplicated reports and remove unused columns
report = report.loc[report['select'] == 'accept']
report = report.sort_values(by=['Study_Instance_UID','birads', 'density'], ascending=False)
report = report.drop_duplicates(subset=['Study_Instance_UID'], keep='first')
report = report[['Study_Instance_UID', 'reports', 'birads', 'density']]

report.to_csv('/Users/lunit/Documents/medicom_script_202107/medicom_report_parsed.csv')
