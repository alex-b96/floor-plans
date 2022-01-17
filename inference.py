from model import *

import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt

class Unet:
    def __init__(self, weights_path='checkpoints/unet-densenet-res-attention-512.ckpt', input_shape=(512,512)):
        
        OUTPUT_CLASSES = 2
        
        
        base_model = tf.keras.applications.DenseNet121(
                        include_top=False,
                        weights="imagenet",
                        input_tensor=None,
                        input_shape=target_shape + (3,),
                        pooling=None
                    )
        layer_names = ['conv1/relu', 'conv2_block6_concat', 'conv3_block12_concat','conv4_block24_concat', 'relu']
        base_model_outputs = [base_model.get_layer(name).output for name in layer_names]

        down_stack = tf.keras.Model(inputs=base_model.input, outputs=base_model_outputs)

        up_stack = [
            upsample(512, 3),  
            upsample(256, 3),  
            upsample(128, 3),  
            upsample(64, 3),  
        ]  
        
        self.model = unet_model(OUTPUT_CLASSES, down_stack, up_stack)
        self.model.load_weights(weights_path)
        
        self.input_shape = input_shape
    
    def inference(self, input_image):
        
        image = tf.convert_to_tensor(input_image)
        image = tf.image.resize(image, self.input_shape, method='bilinear')
        image = tf.keras.applications.densenet.preprocess_input(image)
        
        mask = self.model(image[tf.newaxis,...])
        mask = tf.math.argmax(mask, axis=-1)
        mask = mask.numpy()[0]
        
        return mask
        
if __name__ == '__main__':
    img_path = 'Anhelito (1).png'
    
    image = cv2.imread(img_path)
    model = Unet()
    mask = model.inference(image)
    
    image_show = cv2.resize(image, model.input_shape)
    fig, axarr = plt.subplots(1,2)
    axarr[0].imshow(image_show)
    axarr[1].imshow(mask, cmap='gray')
    plt.show()
    # print()
