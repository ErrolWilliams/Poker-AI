import os
import h5py
import sys
import tensorflow as tf
import tensorflow.contrib.eager as tfe

MODEL = None
class_names = ['bet', 'call', 'check', 'fold', 'raise']


def load(model_name):
    global MODEL
    global class_names
    # different responses neural net can output
    if 'marvel' in model_name:
	    class_names = ['all','bet', 'call', 'check', 'fold', 'raise']
    model_path = os.path.join(os.path.dirname(sys.argv[0]), "models", model_name)
    print(model_path)
    MODEL = tf.keras.models.load_model(model_path)
    print("MODEL BEFORE: " + str(MODEL))

def get_action(inputs):
    global MODEL
    global class_names
    print("MODEL AFTER: " + str(MODEL))
    predict_data = inputs
    prediction = MODEL(predict_data)
    for i, logits in enumerate(prediction):
        class_idx = tf.argmax(logits).numpy()
        print(f"CLASS IDX: {class_idx}")

        p = tf.nn.softmax(logits)[class_idx]
        name = class_names[class_idx]
    return name
