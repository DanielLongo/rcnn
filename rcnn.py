import keras
from keras.layers import (Activation, Conv3D, Dense, Dropout, Flatten, MaxPooling3D, LSTM, Reshape)
from keras.models import Sequential
from keras.optimizers import Adam
import numpy as np
np.random.seed(17)
# (num examples, num trades in t, num currencey pairs, num of time periods, num currencey pairs, num features per trade)
x = np.random.randn(100,70,87,20,4)
y = np.random.randn(100,1)
def build_model():
	model = keras.Sequential()
	num_trades_in_t = x.shape[1] #differs among examples and pairs
	num_features = x.shape[4]
	num_time_periods = x.shape[3]
	num_currencey_pairs = x.shape[2]
	input_shape = (num_trades_in_t, num_currencey_pairs, num_time_periods, num_features)
	model.add(Conv3D(32, kernel_size=(3,3,3), input_shape=input_shape))
	model.add(Activation('relu'))
	model.add(Conv3D(64, kernel_size=(3,3,3)))
	model.add(Activation('relu'))
	model.add(MaxPooling3D(pool_size=(3, 3, 3)))
	model.add(Conv3D(128, kernel_size=(3, 3, 3)))
	model.add(Activation('softmax'))
	# model.add(Conv3D(32, kernel_size=(3, 3, 3)))
	# model.add(Activation('softmax'))
	# model.add(Dropout(0.25))

	#Makes a 2D so that it is LSTM compatible
	model.add(Flatten())
	model.add(Dense(num_currencey_pairs * num_time_periods * num_features, activation="softmax"))
	model.add(Reshape((num_time_periods, num_currencey_pairs * num_features)))

	#RNN
	model.add(LSTM(1))
	
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

model = build_model()
model.summary()
# model.fit(x,y, epochs=100)
print("Finished")