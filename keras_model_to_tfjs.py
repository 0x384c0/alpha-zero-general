import tensorflowjs as tfjs
from tk.TKGame import TKGame
from tk.keras.NNet import NNetWrapper as NNet



g = TKGame()
n1 = NNet(g)
n1.load_checkpoint('temp/','best.pth.tar')
n1.nnet.model._make_predict_function() # workaround from https://github.com/keras-team/keras/issues/6462
n1.save_for_web('temp/',"best.h5")
# tfjs.converters.save_keras_model(n1.nnet.model, "temp/tfjs")