import re
import pandas as pd
from pathlib import Path


def feature_extraction(df):
    df = df.drop_duplicates()

    feature_list = []
    for url in df['domain']:
        url_length = len(url)
        feature_list.append({'url_length': url_length,
                             'alphabet_ratio': len(re.findall('[A-Za-z]',url))/ url_length,
                             'digit_ratio': len(re.findall('[\\d+]',url))/ url_length,
                             'non_alphanumeric_ratio': len(re.findall('[^a-zA-Z0-9]', url))/url_length,
                             'dot_count': len(re.findall('[.]', url)),
                             'dash_count': len(re.findall('[-]', url)),
                             'underscore_count':len(re.findall('[_]', url)),
                             'slash_count':len(re.findall('[/]', url)),
                             'q_mark_count': len(re.findall('[?]', url)),
                             'percentage_count':len(re.findall('[%]', url)),
                             'legit_http': 1 if re.match(r'^https?://', '123://') else 0, 
                             'fake_http': 1 if int('http' in url[8:]) else 0,
                             'php': int(len(re.findall('php', url)) > 0),
                             'html':int(len(re.findall('html', url)) > 0)
                              })
    
    final_df = pd.DataFrame(feature_list)

    return final_df
 


if __name__ == '__main__':
    cwd = Path.cwd()
    file_path = cwd.parent / 'data' / 'clean_02.csv'
    df = pd.read_csv(file_path)
    final_df = feature_extraction(df)
    print(final_df)

        
