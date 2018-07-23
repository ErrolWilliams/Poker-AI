import os
import h5py
import tensorflow as tf
import tensorflow.contrib.eager as tfe

MODEL = None
class_names = ['bet', 'call', 'check', 'fold', 'raise']

def load(model_name):
    global MODEL
    # different responses neural net can output

    script_dir = os.path.dirname(os.path.realpath(__file__))
    print(os.path.join(script_dir, model_name))
    MODEL = tf.keras.models.load_model(os.path.join(script_dir, model_name))
    print("MODEL BEFORE: " + str(MODEL))

def get_action(round_num, risk):
    global MODEL
    print("MODEL AFTER: " + str(MODEL))
    predict_data = tf.convert_to_tensor([[round_num, risk]])
    prediction = MODEL(predict_data)
    for i, logits in enumerate(prediction):
        class_idx = tf.argmax(logits).numpy()
        p = tf.nn.softmax(logits)[class_idx]
        name = class_names[class_idx]
    return name
