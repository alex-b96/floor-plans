import tensorflow as tf
import numpy as np

target_shape = (None, None)

def upsample(filters, size, activation="True"):
    # initializer = tf.random_normal_initializer(0., 0.02)
    initializer = tf.keras.initializers.variance_scaling(scale=2)

    result = tf.keras.Sequential()
    result.add(
      tf.keras.layers.Conv2DTranspose(filters, size, strides=2,
                                      padding='same',
                                      kernel_initializer=initializer,
                                      use_bias=False))

    result.add(tf.keras.layers.BatchNormalization())
    if activation:
        result.add(tf.keras.layers.ReLU())

    return result

def attention_block(skip, x, filters,i):
    # https://towardsdatascience.com/a-detailed-explanation-of-the-attention-u-net-b371a5590831
    # https://arxiv.org/pdf/1804.03999.pdf
    
    initializer = tf.keras.initializers.variance_scaling(scale=2)
    

    theta = tf.keras.layers.Conv2D(filters, 1, strides=2, padding='same', kernel_initializer=initializer,name = 'theta_'+str(i))(skip) ## downsample skip connection
    phi = tf.keras.layers.Conv2D(filters, 1, strides=1, padding='same', kernel_initializer=initializer, name = 'phi_'+str(i))(x) # change channel number. 
 
#     result = tf.keras.layers.Concatenate(name='result_phi_theta'+str(i))([phi, theta])
    result = tf.keras.layers.Add(name='add_atention' + str(i))([phi, theta])
    
    result = tf.keras.layers.ReLU(name='relu_at_'+str(i))(result)
    result = tf.keras.layers.Conv2D(1,1,1,padding='same', kernel_initializer=initializer,name='flat_at_'+str(i))(result)
    result = tf.keras.layers.Activation('sigmoid',name='sig_at_'+str(i))(result)
    
    result = tf.keras.layers.Conv2DTranspose(filters, 3, strides=2, padding='same', kernel_initializer=initializer, name='trans_at_'+str(i))(result) # upsample size -> skip
    
    result = tf.keras.layers.Multiply(name='mul_at_'+str(i))([result, skip])
    
    return result 
    
def conv_block(inputs, filters, size=3, max_pooling=False, activation=True):
    
    initializer = tf.keras.initializers.variance_scaling(scale=2)

    result = tf.keras.layers.Conv2D(filters, size, strides=1,
                                      padding='same',
                                      kernel_initializer=initializer,
                                      use_bias=False)(inputs)

    result = tf.keras.layers.BatchNormalization()(result)

    result = tf.keras.layers.ReLU()(result)
    
    result = tf.keras.layers.Conv2D(filters, size, strides=1,
                                      padding='same',
                                      kernel_initializer=initializer,
                                      use_bias=False)(result)
    result = tf.keras.layers.BatchNormalization()(result)
    
    identity = tf.keras.layers.Conv2D(filters, 1, strides=1,
                                      padding='same',
                                      kernel_initializer=initializer,
                                      use_bias=False)(inputs)
    
    result = tf.keras.layers.Add()([identity, result])
    if activation:
        result = tf.keras.layers.ReLU()(result)
    
    if max_pooling:
        result = tf.keras.layers.MaxPooling2D(pool_size=(2,2))(result)
    
    return result

def unet_model(output_channels:int, down_stack, up_stack):
    inputs = tf.keras.layers.Input(shape=target_shape + (3,))

    filters = [32,64,128,256,512]
    
    # Downsampling through the model
    skips = down_stack(inputs)

    x = skips[-1]
    x = conv_block(x, filters[-1], max_pooling=False) 
    
    skips = reversed(skips[:-1])
    filters = filters[:-1]
    filters.reverse()
    
    i =0 
    for up, skip in zip(up_stack, skips):
        
        ## atention part
        skip = tf.keras.layers.Conv2D(filters[i], 3, 1, padding='same')(skip) 
        skip = tf.keras.layers.BatchNormalization()(skip)
        skip = tf.keras.layers.ReLU()(skip)

        skip = attention_block(skip, x, filters[i], i) 
      
        x = up(x)
        x = tf.keras.layers.Concatenate(name='concat_unet_'+str(i))([x, skip])
        
        ## extra conv block
        x = conv_block(x, filters[i], max_pooling=False)
        i += 1

    # This is the last layer of the model
    last = tf.keras.layers.Conv2DTranspose(
      filters=output_channels, kernel_size=3, strides=2,
      padding='same')  #64x64 -> 128x128

    x = last(x)
    x = conv_block(x, output_channels, max_pooling=False, activation=False)  ## extra conv block

    return tf.keras.Model(inputs=inputs, outputs=x)