# FNN_part_1.py
# This code snippet is a part of learning of machine learning by maja-ja, a github noob.
# ----------- simple functin y=w*x+b ----------------
# this function is used to calculate the output of a simple linear model.
# w and b can change, but x is fixed.
# if we let theta = [w, b], then we can write the function as:
# f_theta(x) = w*x + b, forexample:
# f_theta(3) = 2*x + 1, theta = [2, 1]
# ----------- loss function ------------------------
# normally, the loss function is used to measure how well the model performs.
# L= sigma((y[i]-y_hat[i])^2)    
# where:
# (y[i]-y_hat[i]) = error between the actual output y[i] and the predicted output y_hat[i]
# this function is used to calculate the error for each input sample
# in python, this can be implemented as:
# L = sum((y[i] - y_hat[i])**2 for i in range(len(y)))
# L = sum((a - b)**2 for a, b in zip(y, y_hat)) #more pythonic way
# ----------- function of learning ------------------
# 3                                                       <--\  
# sigma(x[i]*w[i])+b[1]=w[1]*x[1] + w[2]*x[2] + w[3]*x[3] <---- activation function
# where:                                                  <--/
# x[i]=input values   # can't change = fixed inputs
# w[i]=input weights  # can change 
# b[1]=bias           # can change
# sigma=activation function
# w[i] and b[1] are the parameters of the model that we want to learn
# the goal of learning is to find the best values for w[i] and b[1] that minimize the loss function L
#------------ how to learning -------------------
# simple learning function y=w*x+b in python can be implemented as:
def linear_model(x, theta):
    w, b = theta
    return w * x + b

x_values = [1, 2, 3] # input values
y_true = [3, 5, 7]   # output values
theta = [2, 1]       # w=2, b=1, w=2, b=1, # if we want y = 2x + 1

y_hat = [linear_model(x, theta) for x in x_values]
loss = sum((y - y_pred)**2 for y, y_pred in zip(y_true, y_hat))
print(f"Loss: {loss}") # loss should be 0 if the model is perfect

x_values = [1, 3, 5] # input values, changed to test the model
y_true = [3, 5, 7]   # output values, changed to test the model
theta = [2, 1]      # w=2, b=1, # if we want y = 2x + 1

y_hat = [linear_model(x, theta) for x in x_values]
loss = sum((y - y_pred)**2 for y, y_pred in zip(y_true, y_hat))
print(f"Loss: {loss}") # los shonld'n be 0, because the model is not perfect for these inputs
