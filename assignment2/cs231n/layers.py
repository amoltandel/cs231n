import numpy as np


def affine_forward(x, w, b):
   """
   Computes the forward pass for an affine (fully-connected) layer.

   The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
   examples, where each example x[i] has shape (d_1, ..., d_k). We will
   reshape each input into a vector of dimension D = d_1 * ... * d_k, and
   then transform it to an output vector of dimension M.

   Inputs:
   - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
   - w: A numpy array of weights, of shape (D, M)
   - b: A numpy array of biases, of shape (M,)

   Returns a tuple of:
   - out: output, of shape (N, M)
   - cache: (x, w, b)
   """

   #############################################################################
   # TODO: Implement the affine forward pass. Store the result in out. You     #
   # will need to reshape the input into rows.                                 #
   #############################################################################
   N = x.shape[0]
   x_mod = x.reshape((N, -1))
   out = np.dot(x_mod, w) + b.T
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   cache = (x, w, b)
   return out, cache


def affine_backward(dout, cache):
   """
   Computes the backward pass for an affine layer.

   Inputs:
   - dout: Upstream derivative, of shape (N, M)
   - cache: Tuple of:
     - x: Input data, of shape (N, d_1, ... d_k)
     - w: Weights, of shape (D, M)
     - b: biases, of shape (D)

   Returns a tuple of:
   - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
   - dw: Gradient with respect to w, of shape (D, M)
   - db: Gradient with respect to b, of shape (M,)
   """
   x, w, b = cache

   #############################################################################
   # TODO: Implement the affine backward pass.                                 #
   #############################################################################
   dx = np.dot(dout, w.T).reshape(x.shape)
   dw = np.dot(x.reshape(x.shape[0], -1).T, dout)
   db = np.dot(np.ones(x.shape[0]).T, dout).T
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   return dx, dw, db


def relu_forward(x):
   """
   Computes the forward pass for a layer of rectified linear units (ReLUs).

   Input:
   - x: Inputs, of any shape

   Returns a tuple of:
   - out: Output, of the same shape as x
   - cache: x
   """
   out = np.maximum(np.zeros_like(x), x)
   #############################################################################
   # TODO: Implement the ReLU forward pass.                                    #
   #############################################################################
   # pass
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   cache = x
   return out, cache


def relu_backward(dout, cache):
   """
   Computes the backward pass for a layer of rectified linear units (ReLUs).

   Input:
   - dout: Upstream derivatives, of any shape
   - cache: Input x, of same shape as dout

   Returns:
   - dx: Gradient with respect to x
   """
   dx, x = None, cache

   #############################################################################
   # TODO: Implement the ReLU backward pass.                                   #
   #############################################################################
   temp = np.maximum(x, np.zeros_like(x))

   old_err_state = np.seterr(divide='raise')
   ignored_states = np.seterr(**old_err_state)
   dx = np.multiply(dout, np.where(temp > 0, 1, 0))
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   return dx


def batchnorm_forward(x, gamma, beta, bn_param):
   """
   Forward pass for batch normalization.

   During training the sample mean and (uncorrected) sample variance are
   computed from minibatch statistics and used to normalize the incoming data.
   During training we also keep an exponentially decaying running mean of the mean
   and variance of each feature, and these averages are used to normalize data
   at test-time.

   At each timestep we update the running averages for mean and variance using
   an exponential decay based on the momentum parameter:

   running_mean = momentum * running_mean + (1 - momentum) * sample_mean
   running_var = momentum * running_var + (1 - momentum) * sample_var

   Note that the batch normalization paper suggests a different test-time
   behavior: they compute sample mean and variance for each feature using a
   large number of training images rather than using a running average. For
   this implementation we have chosen to use running averages instead since
   they do not require an additional estimation step; the torch7 implementation
   of batch normalization also uses running averages.

   Input:
   - x: Data of shape (N, D)
   - gamma: Scale parameter of shape (D,)
   - beta: Shift paremeter of shape (D,)
   - bn_param: Dictionary with the following keys:
     - mode: 'train' or 'test'; required
     - eps: Constant for numeric stability
     - momentum: Constant for running mean / variance.
     - running_mean: Array of shape (D,) giving running mean of features
     - running_var Array of shape (D,) giving running variance of features

   Returns a tuple of:
   - out: of shape (N, D)
   - cache: A tuple of values needed in the backward pass
   """
   mode = bn_param['mode']
   eps = bn_param.get('eps', 1e-5)
   momentum = bn_param.get('momentum', 0.9)

   N, D = x.shape
   running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
   running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

   out, cache = None, None
   if mode == 'train':
      #############################################################################
      # TODO: Implement the training-time forward pass for batch normalization.   #
      # Use minibatch statistics to compute the mean and variance, use these      #
      # statistics to normalize the incoming data, and scale and shift the        #
      # normalized data using gamma and beta.                                     #
      #                                                                           #
      # You should store the output in the variable out. Any intermediates that   #
      # you need for the backward pass should be stored in the cache variable.    #
      #                                                                           #
      # You should also use your computed sample mean and variance together with  #
      # the momentum variable to update the running mean and running variance,    #
      # storing your result in the running_mean and running_var variables.        #
      #############################################################################
      running_mean = momentum * running_mean + (1.0 - momentum) * np.mean(x, axis=0)
      running_var = momentum * running_var + (1.0 - momentum) * np.var(x, axis=0)
      a = {}
      a[1] = np.mean(x, axis=0)
      a[2] = x - a[1]
      a[3] = a[2] ** 2
      a[4] = np.sum(a[3], axis=0) / float(N)
      a[5] = np.sqrt(a[4] + eps)
      a[6] = 1 / (a[5])
      a[7] = a[6] * a[2]
      a[8] = a[7] * gamma
      out = a[8] + beta

      cache = (x, a, gamma, beta, eps)
      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################
   elif mode == 'test':
      #############################################################################
      # TODO: Implement the test-time forward pass for batch normalization. Use   #
      # the running mean and variance to normalize the incoming data, then scale  #
      # and shift the normalized data using gamma and beta. Store the result in   #
      # the out variable.                                                         #
      #############################################################################
      x = (x - running_mean) / (np.sqrt(running_var) + eps)
      out = gamma * x + beta
      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################
   else:
      raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

   # Store the updated running means back into bn_param
   bn_param['running_mean'] = running_mean
   bn_param['running_var'] = running_var

   return out, cache


def batchnorm_backward(dout, cache):
   """
   Backward pass for batch normalization.

   For this implementation, you should write out a computation graph for
   batch normalization on paper and propagate gradients backward through
   intermediate nodes.

   Inputs:
   - dout: Upstream derivatives, of shape (N, D)
   - cache: Variable of intermediates from batchnorm_forward.

   Returns a tuple of:
   - dx: Gradient with respect to inputs x, of shape (N, D)
   - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
   - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
   """

   dx, dgamma, dbeta = None, None, None
   x, a, gamma, beta, eps = cache
   N, D = x.shape
   #############################################################################
   # TODO: Implement the backward pass for batch normalization. Store the      #
   # results in the dx, dgamma, and dbeta variables.                           #
   #############################################################################
   dldout = dout
   dldbeta = np.sum(dldout, axis=0)
   dldgamma = np.sum(dldout * a[7], axis=0)

   dlda7 = dldout * gamma
   dlda6 = np.sum(dlda7 * a[2], axis=0)
   dlda5 = dlda6 * (-1.0 / (a[5] ** 2))
   dlda4 = dlda5 * (1.0 / (2 * np.sqrt(a[4] + eps)))
   dlda3 = dlda4 / float(N) * np.ones((N, D))
   dlda22 = dlda3 * (2 * a[2])
   dlda21 = dlda7 * a[6]
   dlda2 = dlda21 + dlda22
   dlda1 = -1.0 * np.sum(dlda2, axis=0)
   dldx = (dlda1 / float(N) * np.ones((N, D))) + dlda2

   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   dx = dldx
   dgamma = dldgamma
   dbeta = dldbeta
   return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
   """
   Performs the forward pass for (inverted) dropout.

   Inputs:
   - x: Input data, of any shape
   - dropout_param: A dictionary with the following keys:
     - p: Dropout parameter. We drop each neuron output with probability p.
     - mode: 'test' or 'train'. If the mode is train, then perform dropout;
       if the mode is test, then just return the input.
     - seed: Seed for the random number generator. Passing seed makes this
       function deterministic, which is needed for gradient checking but not in
       real networks.

   Outputs:
   - out: Array of the same shape as x.
   - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
     mask that was used to multiply the input; in test mode, mask is None.
   """
   p, mode = dropout_param['p'], dropout_param['mode']
   if 'seed' in dropout_param:
      np.random.seed(dropout_param['seed'])

   mask = None
   out = None

   if mode == 'train':
      ###########################################################################
      # TODO: Implement the training phase forward pass for inverted dropout.   #
      # Store the dropout mask in the mask variable.                            #
      ###########################################################################
      mask = (np.random.rand(*x.shape) < p) / p
      out = x * mask
      ###########################################################################
      #                            END OF YOUR CODE                             #
      ###########################################################################
   elif mode == 'test':
      ###########################################################################
      # TODO: Implement the test phase forward pass for inverted dropout.       #
      ###########################################################################
      out = x
      ###########################################################################
      #                            END OF YOUR CODE                             #
      ###########################################################################

   cache = (dropout_param, mask)
   out = out.astype(x.dtype, copy=False)

   return out, cache


def dropout_backward(dout, cache):
   """
   Perform the backward pass for (inverted) dropout.

   Inputs:
   - dout: Upstream derivatives, of any shape
   - cache: (dropout_param, mask) from dropout_forward.
   """
   dropout_param, mask = cache
   mode = dropout_param['mode']

   dx = None
   if mode == 'train':
      ###########################################################################
      # TODO: Implement the training phase backward pass for inverted dropout.  #
      ###########################################################################
      dx = dout * mask
      ###########################################################################
      #                            END OF YOUR CODE                             #
      ###########################################################################
   elif mode == 'test':
      dx = dout
   return dx


def conv_forward_naive(x, w, b, conv_param):
   """
   A naive implementation of the forward pass for a convolutional layer.

   The input consists of N data points, each with C channels, height H and width
   W. We convolve each input with F different filters, where each filter spans
   all C channels and has height HH and width HH.

   Input:
   - x: Input data of shape (N, C, H, W)
   - w: Filter weights of shape (F, C, HH, WW)
   - b: Biases, of shape (F,)
   - conv_param: A dictionary with the following keys:
     - 'stride': The number of pixels between adjacent receptive fields in the
       horizontal and vertical directions.
     - 'pad': The number of pixels that will be used to zero-pad the input.

   Returns a tuple of:
   - out: Output data, of shape (N, F, H', W') where H' and W' are given by
     H' = 1 + (H + 2 * pad - HH) / stride
     W' = 1 + (W + 2 * pad - WW) / stride
   - cache: (x, w, b, conv_param)
   """
   N, C, H, W = x.shape
   F, C, HH, WW = w.shape
   out = None
   H_prime = 1 + (H + 2 * conv_param['pad'] - HH) / conv_param['stride']
   W_prime = 1 + (W + 2 * conv_param['pad'] - WW) / conv_param['stride']
   out = np.zeros((N, F, H_prime, W_prime))
   #############################################################################
   # TODO: Implement the convolutional forward pass.                           #
   # Hint: you can use the function np.pad for padding.                        #
   #############################################################################
   x_mod = np.swapaxes(x, axis1=1, axis2=2)
   x_mod = np.swapaxes(x_mod, axis1=2, axis2=3)
   w_mod = np.swapaxes(w, axis1=1, axis2=2)
   w_mod = np.swapaxes(w_mod, axis1=2, axis2=3)
   for each_example in range(N):
      temp = np.zeros((H + 2 * conv_param['pad'], W + 2 * conv_param['pad'], C))
      for channel in range(C):
         temp[:, :, channel] = np.pad(x_mod[each_example, :, :, channel], conv_param['pad'], mode='constant')
      for each_filter in range(F):
         for i in range(H_prime):
            for j in range(W_prime):
               start_h = i * conv_param['stride']
               start_w = j * conv_param['stride']
               stop_h = start_h + HH
               stop_w = start_w + WW
               out[each_example, each_filter, i, j] = np.sum(temp[start_h:stop_h, start_w:stop_w, :]
                                                             * w_mod[each_filter, :, :, :]) + b[each_filter]
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   cache = (x, w, b, conv_param)
   return out, cache


def conv_backward_naive(dout, cache):
   """
   A naive implementation of the backward pass for a convolutional layer.

   Inputs:
   - dout: Upstream derivatives.
   - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

   Returns a tuple of:
   - dx: Gradient with respect to x
   - dw: Gradient with respect to w
   - db: Gradient with respect to b
   """
   dx, dw, db = None, None, None
   #############################################################################
   # TODO: Implement the convolutional backward pass.                          #
   #############################################################################
   x, w, b, conv_param = cache
   N, C, H, W = x.shape
   F, C, HH, WW = w.shape
   _, _, H_prime, W_prime = dout.shape
   dldout = dout
   dldb = np.zeros(b.shape)

   dldx = np.zeros((N, C, H + 2 * conv_param['pad'], W + 2 * conv_param['pad']))
   dldw = np.zeros(w.shape)

   for each_example in range(N):
      temp = np.zeros((C, H + 2 * conv_param['pad'], W + 2 * conv_param['pad']))
      for each_channel in range(C):
         temp[each_channel, :, :] = np.pad(x[each_example, each_channel, :, :], pad_width=conv_param['pad'],
                                           mode='constant')
      for each_filter in range(F):
         for i in range(H_prime):
            for j in range(W_prime):
               dldb[each_filter] += dldout[each_example, each_filter, i, j]
               start_h = i * conv_param['stride']
               start_w = j * conv_param['stride']
               stop_h = start_h + HH
               stop_w = start_w + WW
               dldx[each_example, :, start_h:stop_h, start_w:stop_w] += dldout[each_example, each_filter, i, j] \
                                                                        * w[each_filter, :, :, :]
               dldw[each_filter, :, :, :] += dldout[each_example, each_filter, i, j] * temp[:, start_h:stop_h,
                                                                                       start_w:stop_w]
   db = dldb
   dx = dldx[:, :, conv_param['pad']:-conv_param['pad'], conv_param['pad']:-conv_param['pad']]
   dw = dldw
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   return dx, dw, db


def max_pool_forward_naive(x, pool_param):
   """
   A naive implementation of the forward pass for a max pooling layer.

   Inputs:
   - x: Input data, of shape (N, C, H, W)
   - pool_param: dictionary with the following keys:
     - 'pool_height': The height of each pooling region
     - 'pool_width': The width of each pooling region
     - 'stride': The distance between adjacent pooling regions

   Returns a tuple of:
   - out: Output data
   - cache: (x, pool_param)
   """
   out = None
   #############################################################################
   # TODO: Implement the max pooling forward pass                              #
   #############################################################################
   N, C, H, W = x.shape
   H_prime = (H - pool_param['pool_height'])/pool_param['stride'] + 1
   W_prime = (W - pool_param['pool_width'])/pool_param['stride'] + 1
   out = np.zeros((N, C, H_prime, W_prime))

   for each_example in range(N):
      for each_channel in range(C):
         for i in range(H_prime):
            for j in range(W_prime):
               start_h = i * pool_param['stride']
               start_w = j * pool_param['stride']
               stop_h = start_h + pool_param['pool_height']
               stop_w = start_w + pool_param['pool_width']
               out[each_example, each_channel, i, j] = np.max(x[each_example, each_channel, start_h:stop_h, start_w:stop_w])
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   cache = (x, pool_param)
   return out, cache


def max_pool_backward_naive(dout, cache):
   """
   A naive implementation of the backward pass for a max pooling layer.

   Inputs:
   - dout: Upstream derivatives
   - cache: A tuple of (x, pool_param) as in the forward pass.

   Returns:
   - dx: Gradient with respect to x
   """
   dx = None
   #############################################################################
   # TODO: Implement the max pooling backward pass                             #
   #############################################################################
   x, pool_param = cache
   dldx = np.zeros_like(x)
   N, C, H_prime, W_prime= dout.shape
   _, _, H, W = x.shape

   for each_example in range(N):
      for each_channel in range(C):
         for i in range(H_prime):
            for j in range(W_prime):
               start_h = i * pool_param['stride']
               start_w = j * pool_param['stride']
               stop_h = start_h + pool_param['pool_height']
               stop_w = start_w + pool_param['pool_width']
               max_val = np.max(x[each_example, each_channel, start_h:stop_h, start_w:stop_w])
               window = x[each_example, each_channel, start_h:stop_h, start_w:stop_w]
               temp = np.where(window == max_val, 1, 0)
               dldx[each_example, each_channel, start_h:stop_h, start_w:stop_w] += temp * dout[each_example, each_channel, i, j]


   dx = dldx
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################
   return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
   """
   Computes the forward pass for spatial batch normalization.

   Inputs:
   - x: Input data of shape (N, C, H, W)
   - gamma: Scale parameter, of shape (C,)
   - beta: Shift parameter, of shape (C,)
   - bn_param: Dictionary with the following keys:
     - mode: 'train' or 'test'; required
     - eps: Constant for numeric stability
     - momentum: Constant for running mean / variance. momentum=0 means that
       old information is discarded completely at every time step, while
       momentum=1 means that new information is never incorporated. The
       default of momentum=0.9 should work well in most situations.
     - running_mean: Array of shape (D,) giving running mean of features
     - running_var Array of shape (D,) giving running variance of features

   Returns a tuple of:
   - out: Output data, of shape (N, C, H, W)
   - cache: Values needed for the backward pass
   """
   out, cache = None, None

   #############################################################################
   # TODO: Implement the forward pass for spatial batch normalization.         #
   #                                                                           #
   # HINT: You can implement spatial batch normalization using the vanilla     #
   # version of batch normalization defined above. Your implementation should  #
   # be very short; ours is less than five lines.                              #
   #############################################################################
   N, C, H, W = x.shape
   x_mod = x.reshape(-1, C)
   out, cache = batchnorm_forward(x_mod, gamma, beta, bn_param)
   out = out.reshape(x.shape)
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################

   return out, cache


def spatial_batchnorm_backward(dout, cache):
   """
   Computes the backward pass for spatial batch normalization.

   Inputs:
   - dout: Upstream derivatives, of shape (N, C, H, W)
   - cache: Values from the forward pass

   Returns a tuple of:
   - dx: Gradient with respect to inputs, of shape (N, C, H, W)
   - dgamma: Gradient with respect to scale parameter, of shape (C,)
   - dbeta: Gradient with respect to shift parameter, of shape (C,)
   """
   dx, dgamma, dbeta = None, None, None

   #############################################################################
   # TODO: Implement the backward pass for spatial batch normalization.        #
   #                                                                           #
   # HINT: You can implement spatial batch normalization using the vanilla     #
   # version of batch normalization defined above. Your implementation should  #
   # be very short; ours is less than five lines.                              #
   #############################################################################
   N, C, H, W = dout.shape
   dout_mod = dout.reshape((-1, C))
   dx, dgamma, dbeta = batchnorm_backward(dout_mod, cache)
   dx = dx.reshape(dout.shape)
   #############################################################################
   #                             END OF YOUR CODE                              #
   #############################################################################

   return dx, dgamma, dbeta


def svm_loss(x, y):
   """
   Computes the loss and gradient using for multiclass SVM classification.

   Inputs:
   - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
     for the ith input.
   - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
     0 <= y[i] < C

   Returns a tuple of:
   - loss: Scalar giving the loss
   - dx: Gradient of the loss with respect to x
   """
   N = x.shape[0]
   correct_class_scores = x[np.arange(N), y]
   margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
   margins[np.arange(N), y] = 0
   loss = np.sum(margins) / N
   num_pos = np.sum(margins > 0, axis=1)
   dx = np.zeros_like(x)
   dx[margins > 0] = 1
   dx[np.arange(N), y] -= num_pos
   dx /= N
   return loss, dx


def softmax_loss(x, y):
   """
   Computes the loss and gradient for softmax classification.

   Inputs:
   - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
     for the ith input.
   - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
     0 <= y[i] < C

   Returns a tuple of:
   - loss: Scalar giving the loss
   - dx: Gradient of the loss with respect to x
   """
   probs = np.exp(x - np.max(x, axis=1, keepdims=True))
   probs /= np.sum(probs, axis=1, keepdims=True)
   N = x.shape[0]
   loss = -np.sum(np.log(probs[np.arange(N), y])) / N
   dx = probs.copy()
   dx[np.arange(N), y] -= 1
   dx /= N
   return loss, dx
