
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# 1. Data Preparation
train_dir = '/content/dataset/train'
val_dir = '/content/dataset/val'

train_datagen = ImageDataGenerator(rescale=1.0/255)
val_datagen = ImageDataGenerator(rescale=1.0/255)

train_data = train_datagen.flow_from_directory(
    train_dir, target_size=(100, 100), batch_size=32, class_mode='binary'
)
val_data = val_datagen.flow_from_directory(
    val_dir, target_size=(100, 100), batch_size=32, class_mode='binary'
)

# 2. Model Architecture
model = models.Sequential([
    layers.Conv2D(16, (3,3), activation='relu', input_shape=(100, 100, 3)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 3. Train the Model
history = model.fit(train_data, validation_data=val_data, epochs=5)

# 4. Save and Convert to TensorFlow Lite
model.save('recycler_model.h5')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open('recycler_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("TFLite model saved!")

# 5. Testing the TFLite Model
# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="recycler_model.tflite")
interpreter.allocate_tensors()

# Get input & output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test with a random image
sample_img, sample_label = next(train_data)
sample_img = sample_img[0]
input_data = np.expand_dims(sample_img, axis=0).astype(np.float32)

interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
prediction = interpreter.get_tensor(output_details[0]['index'])
print("Prediction:", "Recyclable" if prediction > 0.5 else "Not Recyclable")
