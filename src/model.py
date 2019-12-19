from pyforest import *
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import scipy.stats as stats

def features(df):

	'''Engineer features and impute missing values'''

	df['Coors'] = pd.get_dummies(df.Team,drop_first=True)['Rockies']
	df['Pull/OppoRatio'] = df.Pull/df.Oppo
	df['Shift%*GB'] = df['Shift%']*df['GB']
	df.fillna(df.mean(),inplace=True)
	return df

def train_and_predict(df):

	'''Split, train, and predict from model'''

	#grabbing features most important as determined by prior cross validation
	X = df[['ISO','LD','GB','IFFB','IFH','SweetSpot%','Above95MPH%','FBLDAvgEV','Age','Shift%','Coors','Pull/OppoRatio','Shift%*GB']]
	y = df.Babip

	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.2,random_state=42)

	lm = LinearRegression()
	lm.fit(X_train,y_train)

	pred = lm.predict(X_train)
	res = pred - y_train
	print(f'Train R^2 = {lm.score(X_train,y_train)}')
	print(f'Train MAE = {np.mean(np.abs(pred-y_train))}')
	print(f'Train RMSE = {np.sqrt(np.mean((y_train - pred)**2))}')

	pred = lm.predict(X_test)
	print(f'Test R^2 = {lm.score(X_test,y_test)}')
	print(f'Test MAE = {np.mean(np.abs(pred-y_test))}')
	print(f'Test RMSE = {np.sqrt(np.mean((y_test - pred)**2))}')

	return lm

def predictPlayer(playerX,playery,playername):
	'''Predict individual player-season's BABIP'''
    print(playername)
    print(f'Predicted BABIP: {lm.predict(np.array(playerX).reshape(1,-1))[0]}')
    print(f'Actual BABIP: {playery}')
    print(f'Difference: {abs(playery - lm.predict(np.array(playerX).reshape(1,-1)))[0]}')
    print(f'2 MAEs: {2*np.mean(np.abs(pred-y_test))}\n')
    playerdict = {'name': playername,'predbabip':lm.predict(np.array(playerX).reshape(1,-1))[0],
            'actbabip':playery}

if __name__ == '__main__':
	df = pd.read_csv('../data/trimmeddf.csv')
	df = features(df)
	model = train_and_predict(df)

