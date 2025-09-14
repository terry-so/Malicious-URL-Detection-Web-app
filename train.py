from src.feature_extract import feature_extraction
import pandas as pd
from pycaret.classification import ClassificationExperiment


def train(csv_file_path, model_filename):
    df = pd.read_csv(csv_file_path)
    df = feature_extraction(df)

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
    
    train('data/clean_data.csv', 'extra_tree_v1')