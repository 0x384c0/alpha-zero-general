import numpy as np

def data_array_to_one_hot_with_shape(array,shape):
	token_ids_one_hot = np.zeros((shape[0], shape[1]))
	token_ids_one_hot[np.arange(len(array)), array] = 1
	return token_ids_one_hot

def data_array_to_one_hot(array,onehot_size): #TODO: remove
	token_ids_one_hot = np.zeros((len(array), onehot_size))
	token_ids_one_hot[np.arange(len(array)), array] = 1
	return token_ids_one_hot.tolist()

def one_hot_batch_to_array(one_hot_batch):
	array = []
	for one_hot in one_hot_batch:
		array.append(np.argmax(one_hot))
	return array


def number_to_onehot(number,onehot_size):
	one_hot = np.zeros(onehot_size)
	if number is not None:
		one_hot[number] = 1
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