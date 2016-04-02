# Copyright 2015 Google Inc. All Rights Reserved.
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


"""Simple image classification with Inception.

Run image classification with Inception trained on ImageNet 2012 Challenge data
set.

This program creates a graph from a saved GraphDef protocol buffer,
and runs inference on an input JPEG image. It outputs human readable
strings of the top 5 predictions along with their probabilities.

Change the --image_file argument to any jpg image to compute a
classification of that image.

Please see the tutorial and website for a detailed description of how
to use this script to perform image recognition.

https://tensorflow.org/tutorials/image_recognition/
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

import subprocess
import time


node_to_class = {}
node_to_class[0] = "beer bottle"
node_to_class[1] = "bar"
node_to_class[2] = "plastic bottle"
node_to_class[3] = "odwalla"
node_to_class[4] = "bag"
node_to_class[5] = "other"
node_to_class[6] = "can"
node_to_class[7] = "empty"
node_to_class[8] = "coffee lid"
node_to_class[9] = "wine bottle"


# classify_image_graph_def.pb:
#   Binary representation of the GraphDef protocol buffer.
# imagenet_synset_to_human_label_map.txt:
#   Map from synset ID to a human readable string.
# imagenet_2012_challenge_label_map_proto.pbtxt:
#   Text representation of a protocol buffer mapping a label to synset ID.

# tf.app.flags.DEFINE_string(
#     'model_dir', '/tmp/imagenet',
#     """Path to classify_image_graph_def.pb, """
#     """imagenet_synset_to_human_label_map.txt, and """
#     """imagenet_2012_challenge_label_map_proto.pbtxt.""")

tf.app.flags.DEFINE_string('image_file', '',
                           """Absolute path to image file.""")
tf.app.flags.DEFINE_integer('num_top_predictions', 5,
                            """Display this many predictions.""")

def create_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  # with tf.gfile.FastGFile(os.path.join(
  #     FLAGS.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
  with tf.gfile.FastGFile("retrained_graph1.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
create_graph()

def log_recyclable():
    proc=subprocess.Popen('echo "recyclable" > log.txt', shell=True, stdout=subprocess.PIPE, )
    proc.communicate()

def log_trash():
    proc=subprocess.Popen('echo "trash" > log.txt', shell=True, stdout=subprocess.PIPE, )
    proc.communicate()


def run_inference_on_image(image):
  """Runs inference on an image.

  Args:
    image: Image file name.

  Returns:
    Nothing
  """
  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = tf.gfile.FastGFile(image, 'rb').read()

  # Creates graph from saved GraphDef.
  with tf.Session() as sess:
    # Some useful tensors:
    # 'softmax:0': A tensor containing the normalized prediction across
    #   1000 labels.
    # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
    #   float description of the image.
    # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
    #   encoding of the image.
    # Runs the softmax tensor by feeding the image_data as input to the graph.
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    print("predicting!")
    predictions = sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)

    # Creates node ID --> English string lookup.
    # node_lookup = NodeLookup()

    top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
    for node_id in top_k:
      # human_string = node_lookup.id_to_string(node_id)
      human_string = node_to_class[node_id]
      score = predictions[node_id]
      print('%s (score = %.5f)' % (human_string, score))
    maxNum = 0
    max_index = 100
    # threshold = max([x for x in predictions if x != 5])
    for i in range(len(predictions)):
      if predictions[i] > maxNum and i not in [1, 4, 5, 7]:
        maxNum = predictions[i]
        max_index = i
    print(maxNum)
    #beer bottle
    if max_index == 0 and maxNum >= 0.65:
      log_recyclable()
    #plastic bottle
    elif max_index == 2 and maxNum >=0.5:
      log_recyclable()
    #odwalla
    elif max_index == 3 and maxNum >=0.4:
      log_recyclable()
    #can
    elif max_index == 6 and maxNum >=0.9:
      log_recyclable()
    elif maxNum >= 0.90:
      log_recyclable()
    else:
      log_trash()


def get_image_files():
  proc=subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, )
  working_directory_files=proc.communicate()[0]
  image_files = [f for f in working_directory_files.split('\n') if f.endswith("jpg") or f.endswith("jpeg")]
  return set(image_files)

# image = (FLAGS.image_file if FLAGS.image_file else
#          os.path.join(FLAGS.model_dir, 'cropped_panda.jpg'))

image_files = get_image_files()
print("ready to categorize")
while True:
  new_image_files = get_image_files()
  if len(new_image_files) > len(image_files):
    image = list(new_image_files.difference(image_files))[0]
    print("running recognition on {0}".format(image))
    time.sleep(1)
    run_inference_on_image(image)
    image_files = new_image_files
  else:
    time.sleep(1)





# def main(_):
#   # maybe_download_and_extract()
#   image = (FLAGS.image_file if FLAGS.image_file else
#            os.path.join(FLAGS.model_dir, 'cropped_panda.jpg'))
#   run_inference_on_image(image)
#   run_inference_on_image(image)

# if __name__ == '__main__':
#   tf.app.run()
