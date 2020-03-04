def plot_train_valid_error(model_name, X_train, y_train, X_valid, y_valid, param_name, param_vec):
    import pandas as pd
    import altair as alt
    import numpy as np

    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.linear_model import LogisticRegression


    
    """
    Takes in a model name, train/validation data sets, 
    a parameter name and a vector of parameter values 
    to try and then plots train/validation errors vs.
    parameter values.

    Parameters:
    ------------
    model_name : str 
        the machine learning model name. Only 'knn', 'decision tree', 'svc', 
        'logistic regression', and 'random forests' are allowed.

    X_train : pd.DataFrame/np.ndarray
        Training dataset without labels. Must be numeric.

    y_train : np.ndarray
        Training labels. Must be numeric.

    X_valid : pd.DataFrame/np.ndarray
        Validation dataset without labels. Must be numeric.

    y_valid : np.ndarray
        Validation labels. Must be numeric.
        
    param_name : str
        the parameter name. Please choose this parameter based on the following information:
        'knn': 'n_neighbors',
        'decision tree': 'max_depth',
        'svc': 'c' or 'gamma',
        'logistic regression': 'c',
        'random forests': 'max_depth' or 'n_estimators'.

    param_vec : list
        the parameter values. Must be numeric.

    Returns:
    ------------
        alt.vegalite.v3.api.Chart
    """
    
    if not isinstance(X_train, pd.DataFrame) and not isinstance(X_train, np.ndarray):
        raise Exception("Sorry, X_train should be a pd.DataFrame or np.ndarray.")
        
    if not isinstance(y_train, np.ndarray):
        raise Exception("Sorry, y_train should be a np.ndarray.")
        
    if not isinstance(X_valid, pd.DataFrame) and not isinstance(X_valid, np.ndarray):
        raise Exception("Sorry, X_valid should be a pd.DataFrame or np.ndarray.")
        
    if not isinstance(y_valid, np.ndarray):
        raise Exception("Sorry, y_valid should be a np.ndarray.")
        
    if (isinstance(X_train, pd.DataFrame) and not np.issubdtype(X_train.to_numpy().dtype, np.number)) or \
    (isinstance(X_train, np.ndarray) and  not np.issubdtype(X_train.dtype, np.number)):
        raise Exception("Sorry, all elements in X_train should be numeric.")
    
    if not np.issubdtype(y_train.dtype, np.number):
        raise Exception("Sorry, all elements in y_train should be numeric.")
    
    if (isinstance(X_valid, pd.DataFrame) and not np.issubdtype(X_valid.to_numpy().dtype, np.number)) or \
    (isinstance(X_valid, np.ndarray) and  not np.issubdtype(X_valid.dtype, np.number)):
        raise Exception("Sorry, all elements in X_valid should be numeric.")
    
    
    if not np.issubdtype(y_valid.dtype, np.number):
        raise Exception("Sorry, all elements in y_valid should be numeric.")

    if not np.issubdtype(np.array(param_vec).dtype, np.number):
        raise Exception("Sorry, all elements in para_vec should be numeric.")

    if np.any(np.array(param_vec) < 0):
        raise Exception("Sorry, all elements in para_vec should be non-negative.")

    if y_train.shape[0] != X_train.shape[0]:
        raise Exception("Sorry, X_train and y_train should have the same number of rows.")
        
    if y_valid.shape[0] != X_valid.shape[0]:
        raise Exception("Sorry, X_valid and y_valid should have the same number of rows.")
        
    if len(X_train.shape) != len(X_valid.shape) or (len(X_train.shape) != 1 and X_train.shape[1] != X_valid.shape[1]):
        raise Exception("Sorry, X_train and X_valid should have the same number of columns.")
        
    results = {'para' : param_vec,
               'train' : [],
               'valid' : []}

    model_name = model_name.lower()
    param_name = param_name.lower()
    
    for n in param_vec:

        if model_name == 'knn':
            if param_name != 'n_neighbors':
                raise Exception("Sorry, only the hyperparameter 'n_neighbors' is allowed for a 'KNN' model.")
                
            model = KNeighborsClassifier(n_neighbors=n).fit(X_train, y_train)

        elif model_name == 'decision tree':
            if param_name != 'max_depth':
                raise Exception("Sorry, only the hyperparameter 'max_depth' is allowed for a 'decision tree' model.")
                
            model = DecisionTreeClassifier(max_depth=n).fit(X_train, y_train)

        elif model_name == 'svc':
            if param_name == 'c':
                model = SVC(C=n).fit(X_train, y_train)
                
            elif param_name == 'gamma':
                model = SVC(gamma=n).fit(X_train, y_train)
                
            else:
                raise Exception("Sorry, only the hyperparameters, 'c' and 'gamma', are allowed for a 'svc' model.")
                
        elif model_name == 'logistic regression':
            if param_name != 'c':
                raise Exception("Sorry, only the hyperparameter 'c' is allowed for a 'logistic regression' model.")
                
            model = LogisticRegression(C=n, max_iter=1000).fit(X_train, y_train)
         
        elif model_name == 'random forests':
            if param_name == 'max_depth':
                model = RandomForestClassifier(max_depth=n).fit(X_train, y_train)
                
            elif param_name == 'n_estimators':
                model = RandomForestClassifier(n_estimators=n).fit(X_train, y_train)
                
            else:
                raise Exception("Sorry, only the hyperparameters, 'max_depth' and 'n_estimators', are allowed for a 'random forests' model.")
        else:
            
            raise Exception("Sorry, the model_name should be chosen from 'knn', 'decision tree', 'svc', 'logistic regression', and 'random forests'.")
            
        results['train'].append(1- model.score(X_train, y_train))
        results['valid'].append(1- model.score(X_valid, y_valid))

    df = pd.DataFrame(results)
    df = df.melt(id_vars = 'para',
                      value_name = 'error',
                      var_name = 'data')
    
    return alt.Chart(df).encode(
        alt.X('para:Q', title = param_name),
        alt.Y('error:Q', title = 'Error'),
        alt.Color('data:N', title = 'Dataset')
    ).mark_line().properties(
        height = 300,
        width = 300
    ).properties(
        title = model_name + " train and valid errors vs. " + param_name
    ).configure_axis(
        labelFontSize = 14,
        titleFontSize = 14
    ).configure_title(
        fontSize = 18
    ).configure_legend(
        labelFontSize = 14,
        titleFontSize = 14
    ).configure_header(
        labelFontSize = 14,
        titleFontSize = 14
    )
