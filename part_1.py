# part_1.py
# This code snippet is a part of learning of machine learning by maja-ja, a github noob.
# ----------- simple function y = w * x + b ----------------
# this function is used to calculate the output of a simple linear model.
# w and b can change, but x is fixed.
# if we let theta = [w, b], then we can write the function as:
# f_theta(x) = w*x + b, for example:
# f_theta(3) = 2*3 + 1 = 7, theta = [2, 1]
# ----------- loss function ------------------------
# Normally, the loss function is used to measure how well the model performs.
# For regression tasks, one common loss is the Mean Squared Error (MSE):
# L = Σ((y[i] - y_hat[i])^2) / n
# where:
#   - y[i] is the actual value
#   - y_hat[i] is the predicted value
#   - (y[i] - y_hat[i])^2 is the squared error for each sample
# In Python, this can be implemented as:
loss = sum((y - y_hat)**2 for y, y_hat in zip(y_true, y_hat)) / len(y_true)
# or:
loss = sum((y - y_pred)**2 for y, y_pred in zip(y_true, y_pred)) / len(y_true) # Mean Squared Error
# ----------- function of learning ------------------
# For a simple neural unit (neuron), the output is calculated as:
# a = σ(w[1]*x[1] + w[2]*x[2] + w[3]*x[3] + b)
# or more generally:
# a = σ(Σ(w[i]*x[i]) + b)       # using summation
# or:
# a = σ(w · x + b)              # using vector dot product

# where:
#   - x[i]: input values (fixed during training)
#   - w[i]: weights (trainable parameters)
#   - b: bias term (trainable parameter)
#   - σ: activation function (e.g., sigmoid, ReLU)

# The goal of learning is to find the best values for w and b 
# that minimize the loss function L across training samples.
#------------ how makes machine learning -------------------
# simple learning function y=w*x+b in python can be implemented as:
def linear_model(x, theta):
    w, b = theta
    return w * x + b

x_values = [1, 2, 3] # input values
y_true = [3, 5, 7]   # output values
theta = [2, 1]       # w=2, b=1 if we want y = 2x + 1

y_hat = [linear_model(x, theta) for x in x_values]
loss = sum((y - y_hat)**2 for y, y_hat in zip(y_true, y_hat))
print(f"Loss: {loss}") # loss should be 0 if the model is perfect

x_values = [1, 3, 5] # input values, changed to test the model
y_true = [3, 5, 7]   # output values, changed to test the model
theta = [2, 1]      # w=2, b=1 if we want y = 2x + 1

y_hat = [linear_model(x, theta) for x in x_values]
loss = sum((y - y_hat)**2 for y, y_hat in zip(y_true, y_hat))
print(f"Loss: {loss}") # loss shouldn't be 0, because the model is not perfect for these inputs