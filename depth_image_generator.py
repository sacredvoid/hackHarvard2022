import os
import glob
import numpy as np
from PIL import Image

from data import TEMP_FILES_PATH, DEPTH_IMAGE_FILE, IMAGE_DOWNLOAD_PATH

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from keras.models import load_model
from layers import BilinearUpSampling2D
from matplotlib import pyplot as plt

from skimage.transform import resize
from skimage.io import imsave, imread

import cv2


def to_multichannel(i):
    if i.shape[2] == 3: return i
    i = i[:, :, 0]
    return np.stack((i, i, i), axis=2)


def DepthNorm(x, maxDepth):
    return maxDepth / x


def display_images(outputs, inputs=None, gt=None, is_colormap=True, is_rescale=True):
    import matplotlib.pyplot as plt
    import skimage
    from skimage.transform import resize

    plasma = plt.get_cmap('plasma')

    shape = (outputs[0].shape[0], outputs[0].shape[1], 3)

    all_images = []

    for i in range(outputs.shape[0]):
        imgs = []

        if isinstance(inputs, (list, tuple, np.ndarray)):
            x = to_multichannel(inputs[i])
            x = resize(x, shape, preserve_range=True, mode='reflect', anti_aliasing=True)
            imgs.append(x)

        if isinstance(gt, (list, tuple, np.ndarray)):
            x = to_multichannel(gt[i])
            x = resize(x, shape, preserve_range=True, mode='reflect', anti_aliasing=True)
            imgs.append(x)

        if is_colormap:
            rescaled = outputs[i][:, :, 0]
            if is_rescale:
                rescaled = rescaled - np.min(rescaled)
                rescaled = rescaled / np.max(rescaled)
            imgs.append(plasma(rescaled)[:, :, :3])
        else:
            imgs.append(to_multichannel(outputs[i]))

        img_set = np.hstack(imgs)
        all_images.append(img_set)

    all_images = np.stack(all_images)

    return skimage.util.montage(all_images, multichannel=True, fill=(0, 0, 0))


def load_images(image_files):
    loaded_images = []
    for file in image_files:
        x = np.clip(np.asarray(Image.open(file), dtype=float) / 255, 0, 1)
        print(x.shape)
        loaded_images.append(x)
    return np.stack(loaded_images, axis=0)


def predict(model, images, minDepth=10, maxDepth=1000, batch_size=2):
    # Support multiple RGBs, one RGB image, even grayscale
    if len(images.shape) < 3: images = np.stack((images, images, images), axis=2)
    if len(images.shape) < 4: images = images.reshape((1, images.shape[0], images.shape[1], images.shape[2]))
    # Compute predictions
    predictions = model.predict(images, batch_size=batch_size)
    # Put in expected range
    return np.clip(DepthNorm(predictions, maxDepth=maxDepth), minDepth, maxDepth) / maxDepth


def resizeimage(path):
    img = imread(path)
    resized_img = cv2.resize(img, (640, 480))
    imsave(TEMP_FILES_PATH + "test.png", resized_img)

def generate_depth_image(path):
    # Argument Parser
    model = 'depthmodel.h5'
    resizeimage(path)
    inputimage = TEMP_FILES_PATH + "test.png"

    custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}
    model = load_model(model, custom_objects=custom_objects, compile=False)

    inputs = load_images(glob.glob(inputimage))
    outputs = predict(model, inputs)

    viz = display_images(outputs.copy(), inputs.copy())
    plt.imshow(viz)
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(viz)
    fig.savefig(IMAGE_DOWNLOAD_PATH + "inputdepthimage.jpg")

