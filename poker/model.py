import os
import h5py
import tensorflow as tf
import tensorflow.contrib.eager as tfe

MODEL = None
def load(model_name)
    tf.enable_eager_execution()

    # different responses neural net can output
    class_names = ['bet', 'call', 'check', 'fold', 'raise']

    script_dir = os.path.dirname(os.path.realpath(__file__))
    model = tf.keras.models.load_model(os.path.join(script_dir, model_name))

 def action(round_num, risk) 
    predict_data = tf.convert_to_tensor([[round_num, risk]])
    prediction = model(predict_data)
    for i, logits in enumerate(prediction)
        class_idx = tf.argmax(logits).numpy()
        p = tf.nn.softmax(logits)[class_idx]
        name = class_names[class_idx]
     return name
