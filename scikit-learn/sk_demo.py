from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from clockdeco import clock

# load iris datasets
iris = datasets.load_iris()
X = iris.data[:,[2,3]]
y = iris.target
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)

# preprocessing
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)


def modelDemo(model,x_train,y_train,test):
	model.fit(x_train,y_train)
	y_pred = model.predict(test)
	return round(accuracy_score(y_test,y_pred),2)


# Perceptron
from sklearn.linear_model import Perceptron
@clock
def PerceptronDemo():
	ppn = Perceptron(max_iter=40,eta0=0.1,random_state=0,shuffle=True)
	result = modelDemo(model=ppn,x_train=X_train_std,y_train=y_train,test=X_test_std)
	return result

# LogisticRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
@clock
def LogisticRegressionDemo():
	#lr = LogisticRegression(C=1000.0,random_state=0)
	lr = SGDClassifier(loss="log")
	result = modelDemo(model=lr,x_train=X_train_std,y_train=y_train,test=X_test_std)
	return result

# SuportVectorMachine
from sklearn.svm import SVC
@clock
def SVMDemo():
	svm = SVC(kernel="linear", C=1.0, random_state=0)
	result = modelDemo(model=svm,x_train=X_train_std,y_train=y_train,test=X_test_std)
	return result


# DecisionTree
from sklearn.tree import DecisionTreeClassifier
@clock
def DecisionTreeDemo():
	tree = DecisionTreeClassifier(criterion="entropy",max_depth=3,random_state=0)
	result = modelDemo(model=tree,x_train=X_train,y_train=y_train,test=X_test)
	return result

# RandomForest
from sklearn.ensemble import RandomForestClassifier
@clock
def RandomForestDemo():
	forest = RandomForestClassifier(criterion="entropy",n_estimators=10,random_state=1,n_jobs=2)
	result = modelDemo(model=forest,x_train=X_train,y_train=y_train,test=X_test)
	return result

# KNN
from sklearn.neighbors import KNeighborsClassifier
@clock
def KNNDemo():
	knn = KNeighborsClassifier(n_neighbors=5,p=2,metric="minkowski")
	result = modelDemo(model=knn,x_train=X_train,y_train=y_train,test=X_test)
	return result

# wbdc dataset
# pipeline test
from skutils import load_wdbc_dataset
df = load_wdbc_dataset()
X = df.loc[:,2:].values
y = df.loc[:,1].values

# クラスを0,1にする
from skutils import label_encode
le,y = label_encode(y)
X_train_w,X_test_w,y_train_w,y_test_w = train_test_split(X,y,test_size=0.20,random_state=1)

from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
@clock
def wdbc_piplineDemo():
	procs = [("scl",StandardScaler()),
			("pca",PCA(n_components=2)),("clf",LogisticRegression(random_state=1,solver='lbfgs'))]
	pipe_lr = Pipeline(procs)
	pipe_lr.fit(X_train_w,y_train_w)
	return round(pipe_lr.score(X_test_w,y_test_w),2)



demos = [globals()[name] for name in globals()
			if name.endswith("Demo")
			and name != "modelDemo"]


if __name__ == "__main__":
	for demo in demos :
		demo()