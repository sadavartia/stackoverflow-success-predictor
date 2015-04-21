from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.naive_bayes import *
from sklearn.neighbors import KNeighborsRegressor
from sklearn import metrics
from feature_extract import *
from data_parser import *
from data_sampling import *
from utils import *
import numpy as np
def main():
    '''
    baseline = Pipeline([('extract', ColumnSelector(['Body'])),
                          ('vect', CountVectorizer(min_df=30,stop_words='english')),
                          #('tfidf', TfidfTransformer()),
                          ('clf', MultinomialNB())])
    '''
    pipeline = Pipeline([
        ('features', FeatureUnion([
            ('bag_of_words',Pipeline([
                ('extract', ColumnSelector(['Body'])),
                ('vect', CountVectorizer(min_df=30,stop_words='english'))
            ])),
            ('field_intersections',Pipeline([
                ('extract', ColumnSelector(['Body','Title','Tags'])),
                ('tokenize_stem', TokenizeStemTransformer()),
                ('transform', ColumnIntersectionTransformer())
            ]))
        ])),
	('estimators', Pipeline([
        ('clf', MultinomialNB()),
	('knn', KNeighborsRegressor())
	]))
    ])
    

    X,y = parse_xml_and_separate_labels('../data/Posts.xml')
    print len(X),len(y)
    split_index=int(0.75*len(X))
    X_train, y_train = X[0:split_index],y[0:split_index]
    X_test, y_test = X[split_index:],y[split_index:]
    _ = pipeline.fit(X_train, y_train)
    predicted = pipeline.predict(X_test)
    print str(np.mean(predicted == y_test))
    Utils.write_to_file("report.txt", metrics.classification_report(y_test, predicted))

    maj,min = getClassCount(X,y)
    d = getd(X,y,maj,min)
    G = getG(X,y,maj,min,1)
    rlist = getRis(X,y,0,5)
    newX,newy = generateSamples(rlist,X,y,G,0,5)
    print len(newX),len(newy)
    split_index=int(0.75*len(newX))
    newX_train, newy_train = newX[0:split_index],newy[0:split_index]
    newX_test, newy_test = newX[split_index:],newy[split_index:]
    _ = pipeline.fit(newX_train, newy_train)
    newPredicted = pipeline.predict(newX_test)
    print str(np.mean(newPredicted == newy_test))



if __name__ == "__main__":
    main()
