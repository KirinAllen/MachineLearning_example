import tensorflow as tf
import matplotlib.pyplot as plt
print(tf.__version__)

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('loss')<0.4):
            print("\nReach 60% accuracy so cancelling training!")
            self.model.stop_training = True

callbacks = myCallback()#实例化myCallback类
mnist = tf.keras.datasets.fashion_mnist
(training_images, training_labels), (test_images, test_labels) = mnist.load_data()
plt.imshow(training_images[0])
print(training_labels[0])
print(training_images[0])
training_images = training_images / 255.0
test_images = test_images / 255.0
model = tf.keras.models.Sequential([tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu),
                                    tf.keras.layers.Dense(10, activation=tf.nn.softmax)])
model.compile(optimizer=tf.keras.optimizers.Adam(),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
model.fit(training_images, training_labels, epochs=5, callbacks=[callbacks])#这里的callbacks是怎么调用的
model.evaluate(test_images, test_labels)
