import numpy as np

def process_data(data):
    summary = {}
    
    # Get basic statistics for numeric columns
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    summary['numeric_stats'] = data[numeric_columns].describe().to_dict()
    
    # Get value counts for categorical columns
    categorical_columns = data.select_dtypes(include=['object']).columns
    summary['categorical_stats'] = {col: data[col].value_counts().to_dict() for col in categorical_columns}
    
    return {
        'summary': summary,
        'data': data
    }