from imblearn.over_sampling import SMOTE
from pandas import read_csv
import pandas
from matplotlib import pyplot
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler, RobustScaler
import pickle

claimscores = {}

def readCSV(filename):
    return read_csv(filename)


def model(dataframe):

    rob_scaler = RobustScaler()

    dataframe['Amount'] = rob_scaler.fit_transform(dataframe['Amount'].values.reshape(-1, 1))
    dataframe['Time'] = rob_scaler.fit_transform(dataframe['Time'].values.reshape(-1, 1))


    X =  dataframe.drop('Class', axis=1)
    y = dataframe['Class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = X_train.values
    X_test = X_test.values
    y_train = y_train.values
    y_test = y_test.values
    classifiers = {
        "LogisiticRegression": LogisticRegression(),


    }
    sm = SMOTE(sampling_strategy='auto', k_neighbors=1, random_state=42)
    x_res, y_res = sm.fit_resample(X_train, y_train)
    for key, classifier in classifiers.items():
        classifier.fit(x_res, y_res)
        training_score = cross_val_score(classifier, x_res, y_res, cv=5)
        print("Classifiers: ", classifier.__class__.__name__, "Has a training score of",
              round(training_score.mean(), 2) * 100, "% accuracy score")

        fraudset = readCSV('fraudset.csv')
        nonfraudset = readCSV('nonfraudset.csv')
        new_fraudset = fraudset.drop('Class', axis=1)
        new_nonfraudset = nonfraudset.drop('Class', axis=1)
        new_nonfraudset['Amount'] = rob_scaler.fit_transform(new_nonfraudset['Amount'].values.reshape(-1, 1))
        new_nonfraudset['Time'] = rob_scaler.fit_transform(new_nonfraudset['Time'].values.reshape(-1, 1))

        predictions = classifier.predict(new_fraudset)
        nonfraudpreds = classifier.predict(new_nonfraudset)
        correct=0
        for i in predictions:
            if i == 1:
                correct+=1
        print("correct: " + str(correct))
        nonfraudcorrect = 0
        for i in nonfraudpreds:
            if i == 0:
                nonfraudcorrect+=1

        print("nonfraudcorrect: " + str(nonfraudcorrect))
        y_preds = classifier.predict(X_test);
        print(accuracy_score(y_test, y_preds))
        pickle.dump(classifier, open(key+'.sav', 'wb'))




if __name__=='__main__':
    filename = input('filename: ')
    df = readCSV(filename)

    model(df)





