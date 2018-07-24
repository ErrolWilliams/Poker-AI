import os
import h5py
import tensorflow as tf
import tensorflow.contrib.eager as tfe


def predict(model, class_names):

    # values model will use to predict output
    predict_dataset = tf.convert_to_tensor([
        [0.0, 0.7],
        [1.0, 0.5],
        [2.0, 0.3]
    ])

    predictions = model(predict_dataset)

    for i, logits in enumerate(predictions):
        class_idx = tf.argmax(logits).numpy()
        p = tf.nn.softmax(logits)[class_idx]
        name = class_names[class_idx]
        print("Example {} prediction: {} ({:4.1f}%)".format(i, name, 100 * p))

def grad(model, inputs, targets):
  with tf.GradientTape() as tape:
    loss_value = loss(model, inputs, targets)
  return loss_value, tape.gradient(loss_value, model.trainable_variables)


def loss(model, x, y):
  y_ = model(x)
  return tf.losses.sparse_softmax_cross_entropy(labels=y, logits=y_)


def pack_features_vector(features, labels):
  """Pack the features into a single array."""
  features = tf.stack(list(features.values()), axis=1)
  return features, labels


def train_model(model):
    train_loss_results = []
    train_accuracy_results = []

    # number of times to train the model
    num_epochs = 10

    for epoch in range(num_epochs):
        epoch_loss_avg = tfe.metrics.Mean()
        epoch_accuracy = tfe.metrics.Accuracy()

        # Training loop - using batches of 32
        for x, y in train_dataset:
            # Optimize the model
            loss_value, grads = grad(model, x, y)
            optimizer.apply_gradients(zip(grads, model.variables),
                                      global_step)

            # Track progress
            epoch_loss_avg(loss_value)  # add current batch loss
            # compare predicted label to actual label
            epoch_accuracy(tf.argmax(model(x), axis=1, output_type=tf.int32), y)

        # end epoch
        train_loss_results.append(epoch_loss_avg.result())
        train_accuracy_results.append(epoch_accuracy.result())

        if epoch % 2 == 0:
            print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,
                                                                        epoch_loss_avg.result(),
                                                                       epoch_accuracy.result()))

    test_dataset = tf.contrib.data.make_csv_dataset(
        data_set,
        batch_size,
        column_names=column_names,
        label_name=label_name,
        num_epochs=1,
        shuffle=False)

    test_dataset = test_dataset.map(pack_features_vector)

    test_accuracy = tfe.metrics.Accuracy()

    for (x, y) in test_dataset:
        logits = model(x)
        prediction = tf.argmax(logits, axis=1, output_type=tf.int32)
        test_accuracy(prediction, y)

    #print("Test set accuracy: {:.3%}".format(test_accuracy.result()))


if __name__ == "__main__":
    """
    Initialization
    """
    tf.enable_eager_execution()

    # name of csv file used to train network
    training_file_name = 'trainData.csv'
    data_set = open(training_file_name, 'r')
    data_set = data_set.name

    # column order in CSV file
    column_names = ['round', 'risk', 'response']

    feature_names = column_names[:-1]
    label_name = column_names[-1]

    # different values last column in csv file can represent
    class_names = ['bet', 'call', 'check', 'fold', 'raise']

    batch_size = 32

    train_dataset = tf.contrib.data.make_csv_dataset(
        data_set,
        batch_size,
        column_names=column_names,
        label_name=label_name,
        num_epochs=1)

    train_dataset = train_dataset.map(pack_features_vector)

    features, labels = next(iter(train_dataset))


    """
    Model creation/loading
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    response = input('Would you like to load in a network from a HDF5 file [Y/n]\n')
    if response.upper() == 'Y' or response.upper() == 'YES':
        response2 = input('Enter the relative directory to the HDF5 to load')
        model = tf.keras.models.load_model(os.path.join(script_dir, response2))
    else:
        # make keras neural net model
        print('Creating model')

        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(2,)),  # input shape required
            tf.keras.layers.Dense(10, activation=tf.nn.relu),
            tf.keras.layers.Dense(10, activation=tf.nn.relu),
            tf.keras.layers.Dense(10, activation=tf.nn.relu),
            tf.keras.layers.Dense(10, activation=tf.nn.relu),
            tf.keras.layers.Dense(5)
        ])

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)

    global_step = tf.train.get_or_create_global_step()

    loss_value, grads = grad(model, features, labels)

    optimizer.apply_gradients(zip(grads, model.variables), global_step)

    # update num epochs and when to print Loss
    train_model(model)

    # update tensor model will use to predict
    predict(model, class_names)

    response = input('Do you want to save to this model to [Y/n]\n')
    if response.upper() == 'Y' or response.upper() == 'YES':
        print('WARNING the model will be saved in a file from the current directory and will overwrite any files\n'
              'already saved under the name you will input next.')
        response2 = input('Enter name to save model as (exclude extension):')
        tf.keras.models.save_model(
            model,
            os.path.join(script_dir, response2),
            overwrite=True,
            include_optimizer=False
        )

    print('Done')



