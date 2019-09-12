# Copyright 2019 The FastEstimator Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import layers

from fastestimator import Estimator, Network, Pipeline
from fastestimator.network.loss import MeanSquaredError
from fastestimator.network.model import FEModel, ModelOp


def create_dnn():
    model = tf.keras.Sequential()
    model.add(layers.Dense(10, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(10, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(10, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation="linear"))
    return model


def get_estimator(epochs=50, batch_size=32):
    (x_train, y_train), (x_eval, y_eval) = tf.keras.datasets.boston_housing.load_data()
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_eval = scaler.transform(x_eval)
    data = {"train": {"x": x_train, "y": y_train}, "eval": {"x": x_eval, "y": y_eval}}
    pipeline = Pipeline(batch_size=batch_size, data=data)

    #prepare model
    model = FEModel(model_def=create_dnn, model_name="dnn", optimizer="adam")
    network = Network(
        ops=[ModelOp(inputs="x", model=model, outputs="y_pred"), MeanSquaredError(y_true="y", y_pred="y_pred")])

    #create estimator
    estimator = Estimator(network=network, pipeline=pipeline, epochs=epochs, log_steps=10)
    return estimator


if __name__ == "__main__":
    est = get_estimator()
    est.fit()
