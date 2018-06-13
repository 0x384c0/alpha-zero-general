import numpy as np

def data_array_to_one_hot(array,onehot_size):
	token_ids_one_hot = np.zeros((len(array), onehot_size))
	token_ids_one_hot[np.arange(len(array)), array] = 1
	return token_ids_one_hot

def one_hot_batch_to_array(one_hot_batch):
	array = []
	for one_hot in one_hot_batch:
		array.append(np.argmax(one_hot))
	return array