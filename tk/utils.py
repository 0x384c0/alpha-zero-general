import numpy as np
import os

def data_array_to_one_hot_with_shape(array,shape):
	if not is_debug_mode():
		for i,item in enumerate(array):
			if item >=  shape[1]:
				array[i] = shape[1] - 1

	token_ids_one_hot = np.zeros((shape[0], shape[1]))
	token_ids_one_hot[np.arange(len(array)), array] = 1
	return token_ids_one_hot

def data_array_to_one_hot(array,onehot_size): #TODO: remove
	token_ids_one_hot = np.zeros((len(array), onehot_size))
	try:
		token_ids_one_hot[np.arange(len(array)), array] = 1
	except:
		print("Warning: data_array_to_one_hot out of bounds")
		print("array " + str(array))
	return token_ids_one_hot.tolist()

def one_hot_batch_to_array(one_hot_batch):
	array = []
	for one_hot in one_hot_batch:
		array.append(np.argmax(one_hot))
	return array


def number_to_onehot(number,onehot_size):
	one_hot = np.zeros(onehot_size)

	try:
		if number is not None:
			one_hot[number] = 1
	except:
		print("Warning: number_to_onehot out of bounds")
		print("number " + str(number))
		
	return one_hot.tolist()

def onehot_to_number(onehot):
	return np.argmax(onehot) if sum(onehot) == 1 else None


def number_to_bits_array(number,array_size):
	a =	np.array(np.uint8(number), dtype=np.uint8)
	b = np.unpackbits(a)
	return np.concatenate((np.zeros(array_size - len(b)) ,b)).tolist()

def bits_array_to_number(array):
	array = list(map(lambda x: int(x),array[-8:]))
	return np.packbits(array)[0]

# env vraiables
is_debug_mode_result = None
def is_debug_mode():
	global is_debug_mode_result
	if is_debug_mode_result == None:
		is_debug_mode_result = os.getenv('DEBUG_MODE', "False")
	return is_debug_mode_result == "True"

def is_gpu_mode():
	return os.getenv('GPU_MODE', "False") == "True"

def number_of_train_iterations():
	stringNum = os.getenv('NUMBER_OF_TRAIN_ITERATIONS', "3")
	return int(stringNum)


# string coloring
def red(obj):
	return "\033[31m"+ str(obj) + "\033[0m"

def green(obj):
	return "\033[32m"+ str(obj) + "\033[0m"

def bpurple(obj):
	return "\033[1;35m"+ str(obj) + "\033[0m"