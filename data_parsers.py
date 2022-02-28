"""
This file contains data parser objects which will take as input text files and perform filtering operations
and processing. The output will be new CSV files.
"""

import re
import pandas as pd
from pathlib import Path

class DCSummaryParser:

    @staticmethod
    def parse_docs(docs, section='hosp_course'):
        #this does the regex parsing for docs, it returns a series of strings
        #it can parse hpi, dc_summary, or both
        regex_dict = {
            'hpi': docs.str.extract(re.compile(r'((history of present illness|history of the present illness):?([\s\S]*?)(past medical history:|physical exam:|physical examination:|exam:|hospital course:|social history:))', re.IGNORECASE)).iloc[:,2],
            'hosp_course': docs.str.extract(re.compile(r'hospital course(.{0,50}:)?([\s\S]*?)(condition at discharge|discharge diagnoses|discharge diagnosis|discharge medications|medications on discharge|addendum|NamePattern|past medical history:|allergies:|medications on admission:)', re.IGNORECASE)).iloc[:,1],
            }

        if section == 'both':        
            print(f"Parsed HPI successfully - {sum(regex_dict['hpi'].isna())}/{len(regex_dict['hpi'])} not matched")
            print(f"Parsed Hosp. Course successfully - {sum(regex_dict['hosp_course'].isna())}/{len(regex_dict['hosp_course'])} not matched")
            
            return regex_dict['hpi'] + '\n======================\n' + regex_dict['hosp_course']


        else:
            print(f"Parsed {section} successfully - {sum(regex_dict[section].isna())}/{len(regex_dict[section])} not matched")
            return regex_dict[section]

    @staticmethod
    def to_csv(df, out_path, section='hosp_course', with_code=True):
        """
        input: dc summary path - must be path to CSV with 'code' and 'dc_summary' columns
        output: csv of dataframe with columns 'hospital_course' and 'code'
        """

        df['parsed_hosp_course'] = DCSummaryParser.parse_docs(df.dc_summary, section=section)
        df = df[df.parsed_hosp_course.isnull() == False]
        if with_code:
            df[['parsed_hosp_course', 'code']].to_csv(out_path, header=False, index=False)
        else:
            df['parsed_hosp_course'].to_csv(out_path, header=False, index=False)

df = pd.read_csv('./data/balanced_dc_summaries.csv', index_col=False)
DCSummaryParser.to_csv(df, Path('./data/balanced_parsed.csv'), section='both')


