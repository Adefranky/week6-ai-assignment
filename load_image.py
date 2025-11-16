from tflite_runtime.interpreter import Interpreter
import numpy as np
from PIL import Image

interpreter = Interpreter(model_path="recycler_model.tflite")
interpreter.allocate_tensors()

img = Image.open("test_image.jpg").resize((100, 100))
input_data = np.array(img, dtype=np.float32).reshape(1, 100, 100, 3) / 255.0

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Prediction:", "Recyclable" if output_data > 0.5 else "Not Recyclable")
