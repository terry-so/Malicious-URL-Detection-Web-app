from src.feature_extract import feature_extraction
import pandas as pd
from pycaret.classification import ClassificationExperiment
import argparse

def train(csv_file_path, model_filename):
    raw_df = pd.read_csv(csv_file_path)
    label = raw_df.iloc[:,-1]
    df = feature_extraction(raw_df)
    df['label'] = label
    print(df)
    exp = ClassificationExperiment()
    exp.setup(data = df, target = 'label', numeric_features=['url_length','alphabet_ratio','digit_ratio','non_alphanumeric_ratio',
                                                       'dot_count','dash_count','underscore_count','underscore_count','q_mark_count','percentage_count'],
                                                       transformation= True, normalize= True, normalize_method= 'zscore', train_size = 0.75, 
                                                       data_split_stratify = True, fold_strategy = 'stratifiedkfold', fold = 5, session_id= 123
                                                       )
    model = exp.create_model('et')
    tuned_model = exp.tune_model(model)
    final_model = exp.finalize_model(tuned_model)
    exp.save_model(final_model, f'models/{model_filename}')


















if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='train model, input csv path and model name')
    parser.add_argument('path', type=str, help='csv file path')
    parser.add_argument('model_name', type=str, help='desired model name')
    args = parser.parse_args()
    train(args.path, args.model_name)