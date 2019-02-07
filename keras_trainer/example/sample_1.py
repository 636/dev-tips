# -*- coding: utf-8 -*-

import logging
from keras_trainer.trainer import KerasTrainer

import numpy as np
from injector import inject
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

LOGGER = logging.getLogger(__name__)


def to_batch(train: np.ndarray, label: np.ndarray, batch_size: int):
    """
    :param l:           list
    :param group_size:  size of each group
    :return:            Yields successive group-sized lists from l.
    """
    while True:
        for i in range(0, train.shape[0], batch_size):
            yield train[i:i+batch_size], label[i:i+batch_size]


def get_dataloader(batch_size: int, num_classes):
    # input image dimensions
    img_rows, img_cols = 28, 28

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    LOGGER.info('x_train shape: %s', x_train.shape)
    LOGGER.info('%s %s', x_train.shape[0], 'train samples')
    LOGGER.info('%s %s', x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    train_step = x_train.shape[0] / batch_size
    val_step = x_test.shape[0] / batch_size

    return [lambda: (train_step, to_batch(x_train, y_train, batch_size)),
            lambda: (val_step, to_batch(x_test, y_test, batch_size)),
            input_shape]


@inject
def train(trainer: KerasTrainer,
          batch_size=128,
          num_classes=10,
          epoch=12):

    train_loader, val_loader, input_shape = get_dataloader(batch_size, num_classes)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    model, history = trainer.train(model, train_loader, train_loader, epoch)
    print('Test loss:', history)
