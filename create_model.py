# example of loading the mnist dataset
#import tensorflow as tf
#from tensorflow import tensorflow as tf
#import tensorflow as tf
from numpy import mean
from numpy import std
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import BatchNormalization
from sklearn.model_selection import KFold
from matplotlib import pyplot


# load train and test dataset
def load_dataset():
	# load dataset from home/xavier/.keras/datasets/mnist.npz
	path = 'mnist.npz'
	(trainX, trainY), (testX, testY) = mnist.load_data(path)
	# reshape dataset to have a single channel, skip color
	#trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
	#testX = testX.reshape((testX.shape[0], 28, 28, 1))
	# one hot encode target values
	#trainY = to_categorical(trainY)
	#testY = to_categorical(testY)
	return trainX, trainY, testX, testY

# reshape model
def Reshape(trainX, trainY, testX, testY):
	# reshape dataset to have a single channel, skip color
	trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
	testX = testX.reshape((testX.shape[0], 28, 28, 1))
	# Normalize
    #X_train /= 255
    # X_test /= 255
	# one hot encode target values
	# number of classes
	number_of_classes = 10
	trainY = to_categorical(trainY, number_of_classes)
	testY = to_categorical(testY, number_of_classes)
	return trainX, trainY, testX, testY

# just to show pictures in the model
def show_data(trainX, trainY, testX, testY):
	# plot first few images
	for i in range(9):
		# define subplot
		pyplot.subplot(330 + 1 + i)
		# plot raw pixel data
		pyplot.imshow(trainX[i], cmap=pyplot.get_cmap('gray'))
	# show the figure
	pyplot.show()

# scale pixels
def prep_pixels(train, test):
	# convert from integers to floats
	train_norm = train.astype('float32')
	test_norm = test.astype('float32')
	# normalize to range 0-1
	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0
	# return normalized images
	return train_norm, test_norm

# define cnn model
def define_model():
	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
	model.add(BatchNormalization())
	model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(BatchNormalization())
	model.add(Dense(10, activation='softmax'))
	# compile model
	opt = SGD(lr=0.01, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model
#
# evaluate a model using k-fold cross-validation
def evaluate_model(model, dataX, dataY, n_folds=5):
	scores, histories = list(), list()
	# prepare cross validation
	kfold = KFold(n_folds, shuffle=True, random_state=1)
	# enumerate splits
	for train_ix, test_ix in kfold.split(dataX):
		# select rows for train and test
		trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
		# fit model
		history = model.fit(trainX, trainY, epochs=10, batch_size=32, validation_data=(testX, testY), verbose=0)
		# evaluate model
		_, acc = model.evaluate(testX, testY, verbose=0)
		print('> %.3f' % (acc * 100.0))
		# stores scores
		scores.append(acc)
		histories.append(history)
	return scores, histories
#
# plot diagnostic learning curves
def summarize_diagnostics(histories):
	for i in range(len(histories)):
		# plot loss
		pyplot.subplot(211)
		pyplot.title('Cross Entropy Loss')
		pyplot.plot(histories[i].history['loss'], color='blue', label='train')
		pyplot.plot(histories[i].history['val_loss'], color='orange', label='test')
		# plot accuracy
		pyplot.subplot(212)
		pyplot.title('Classification Accuracy')
		pyplot.plot(histories[i].history['accuracy'], color='blue', label='train')
		pyplot.plot(histories[i].history['val_accuracy'], color='orange', label='test')
	pyplot.show()
 
# summarize model performance
def summarize_performance(scores):
	# print summary
	print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(scores)*100, std(scores)*100, len(scores)))
	# box and whisker plots of results
	pyplot.boxplot(scores)
	pyplot.show()

# tun_test_harness
def run_test_harness():

	#print("Tensorflow version: ", tf.__version__)
	# eager execution
	tf.executing_eagerly()
	# load dataset
	trainX, trainY, testX, testY = load_dataset()
	# show data
	#show_data(trainX, trainY, testX, testY)
	# reshape
	trainX, trainY, testX, testY = Reshape(trainX, trainY, testX, testY)
	# prepare pixel data
	trainX, testX = prep_pixels(trainX, testX)
	# define model
	model = define_model()
	# only needed when we should show digrams on screnn
	# evaluate model
	scores, histories = evaluate_model(model, trainX, trainY)
	# learning curves
	summarize_diagnostics(histories)
	# summarize estimated performance
	summarize_performance(scores)
	# fit model
	model.fit(trainX, trainY, epochs=25, batch_size=32, validation_data=(testX, testY))
	#
	metrics = model.evaluate(testX, testY, verbose=0)
	print("Metrics - (test loss and test accuracy)")
	print(metrics)
	# save model
	model.save('models/final_model2.h5')
 
#
#############################	
# entry point
#############################
run_test_harness()