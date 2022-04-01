import neuralNetwork as nn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from os import listdir
from torch.nn.functional import mse_loss
import torch.optim.lr_scheduler
import torch.optim
import pickle
import torch
import torch.utils.data
import numpy as np

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)


PATH = "chessEngine.model"
pickles = listdir("data")
pickles = pickles[:]

if torch.cuda.is_available():  
  dev = "cuda:0" 
else:  
  dev = "cpu"  
device = torch.device(dev)  

try:
    checkpoint = torch.load(PATH)
except:
    checkpoint = None
    
#Building the network
learningRate = 3e-4
batchSize = 128
numEpochs = 50
testSize = 0.05
seed = 8008153

#network = nn.neuralNet()
network = nn.convNet()
network.to(device)

if checkpoint is not None:
    network.load_state_dict(checkpoint['model_state_dict'])

optim = torch.optim.Adam(network.parameters(), lr=learningRate)

if checkpoint is not None:
    optim.load_state_dict(checkpoint['optimizer_state_dict'])

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optim, patience=10, verbose=True, factor=0.5)

trainError = []
testError = []

trainErrorGraph = []
testErrorGraph = []
#Trainging the network
for epoch in range(1, numEpochs+1): 
    #Load the pickle
    index = 0
    for pic in pickles:
        index += 1
        printProgressBar(index, len(pickles), prefix="Epoch " + str(epoch))
        file = open("data/" + str(pic), "rb")
        xData, yData = pickle.load(file)
        file.close()
        X_train, X_test, y_train, y_test = train_test_split(xData, yData, test_size=testSize, random_state=seed)

        X_train = torch.tensor(X_train).float().to(device)
        X_test = torch.tensor(X_test).float().to(device)
        y_train = torch.tensor(y_train).float().to(device)
        y_test = torch.tensor(y_test).float().to(device)
        for X_batch,y_batch in nn.iterate_minibatches(X_train, y_train, batchsize=batchSize, shuffle=True):
            network.zero_grad()
            out = network(X_batch.view(-1, 12, 8, 8))
            loss = mse_loss(out, y_batch.tanh().view(-1, 1))
            loss.backward()
            optim.step()
        #Calculate Error
        network.eval()
        with torch.no_grad():
            error = []
            for X_batch,y_batch in nn.iterate_minibatches(X_train, y_train, batchsize=batchSize, shuffle=True):
                out = network(X_batch.view(-1, 12, 8, 8))
                loss = mse_loss(out, y_batch.tanh().view(-1, 1))
                error.append(loss.item())
            trainError.append(np.mean(error))
            trainErrorGraph.append(np.mean(trainError[-len(pickles):]))

            error = []
            for X_batch,y_batch in nn.iterate_minibatches(X_test, y_test, batchsize=batchSize, shuffle=True):
                out = network(X_batch.view(-1, 12, 8, 8))
                loss = mse_loss(out, y_batch.tanh().view(-1, 1))
                error.append(loss.item())
            testError.append(np.mean(error))
            testErrorGraph.append(np.mean(testError[-len(pickles):]))
        network.train()

    scheduler.step(np.mean(testError[-len(pickles):]))
    print("\nTraining error: " + str(np.mean(trainError[-len(pickles):])))
    print("Testing error: " + str(np.mean(testError[-len(pickles):])))
    torch.save({
            'epoch': epoch,
            'model_state_dict': network.state_dict(),
            'optimizer_state_dict': optim.state_dict(),
            }, PATH)

torch.save({
            'epoch': epoch,
            'model_state_dict': network.state_dict(),
            'optimizer_state_dict': optim.state_dict(),
            }, PATH)

plt.plot(testErrorGraph, label='Test Error')
plt.plot(trainErrorGraph, label='Train Error')
plt.legend(loc='best')
plt.grid()
plt.show()
                 
                    