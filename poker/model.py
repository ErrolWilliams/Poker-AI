import os
import h5py
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
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print(os.path.join(script_dir, model_name))
    MODEL = tf.keras.models.load_model(os.path.join(script_dir, model_name))
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
