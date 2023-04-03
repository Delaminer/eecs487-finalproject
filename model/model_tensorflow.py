import tensorflow as tf

# Define the neural network model
class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.fc1 = tf.keras.layers.Dense(50, input_shape=(768,))
        self.relu = tf.keras.layers.ReLU()
        self.fc2 = tf.keras.layers.Dense(1)

    def call(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Define the training loop
def train(model, optimizer, loss_fn, dataloader):
    for inputs, labels in dataloader:
        with tf.GradientTape() as tape:
            outputs = model(inputs)
            loss = loss_fn(labels, outputs)
        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

# Create a dataset and dataloader (dummy data for this example)
inputs = tf.random.normal((100, 10))  # 100 samples of input size 10
labels = tf.random.normal((100, 1))  # 100 samples of output size 1
dataset = tf.data.Dataset.from_tensor_slices((inputs, labels))
dataloader = dataset.batch(10)

# Create an instance of the model, an optimizer and a loss function
model = MyModel()
optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
loss_fn = tf.keras.losses.MeanSquaredError()

# Train the model
num_epochs = 10
for epoch in range(num_epochs):
    train(model, optimizer, loss_fn, dataloader)
    loss = loss_fn(labels, model(inputs)).numpy()
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss:.4f}")
