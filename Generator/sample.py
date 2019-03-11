import uuid

import tensorflow as tf
from read_utils import TextConverter
from model import CharRNN
import os

FLAGS = tf.flags.FLAGS
tf.flags.DEFINE_string('file_type', 'js', 'File Type of Current Sampling.')
tf.flags.DEFINE_integer('lstm_size', 512, 'size of hidden state of lstm')
tf.flags.DEFINE_integer('num_layers', 2, 'number of lstm layers')
tf.flags.DEFINE_boolean('use_embedding', False, 'whether to use embedding')
tf.flags.DEFINE_integer('embedding_size', 128, 'size of embedding')
tf.flags.DEFINE_string('converter_path', 'model/' + FLAGS.file_type + '/converter.pkl', 'converter path')
tf.flags.DEFINE_string('checkpoint_path', 'model/' + FLAGS.file_type, 'checkpoint path')
tf.flags.DEFINE_string('seed_for_generating', 'jQuery', 'use this string to start generating')
tf.flags.DEFINE_integer('max_length_of_generated', 2000, 'max length to generate')
tf.flags.DEFINE_integer('num_to_generate', 14100, "Num of files to generate")


def main(_):
    converter = TextConverter(filename=FLAGS.converter_path)
    if os.path.isdir(FLAGS.checkpoint_path):
        FLAGS.checkpoint_path = tf.train.latest_checkpoint(FLAGS.checkpoint_path)

    model = CharRNN(converter.vocab_size, None, sampling=True,
                    lstm_size=FLAGS.lstm_size, num_layers=FLAGS.num_layers,
                    use_embedding=FLAGS.use_embedding,
                    embedding_size=FLAGS.embedding_size)

    model.load(FLAGS.checkpoint_path)

    # start = converter.text_to_arr(FLAGS.seed_for_generating)
    seeds = ['var a = fun', 'function a(', 'this.', 'document.', 'window.', 'var a = document.g', 'var a;', 'jQuery']
    for seed in seeds:
        start = converter.text_to_arr(seed)
        for i in range(0, FLAGS.num_to_generate):
            print('Generating: ' + seed + ' -> ' + str(i))
            file_name = str(uuid.uuid1())
            file_path = '../../BrowserFuzzingData/generated/' + FLAGS.file_type + '/' + file_name + '.' + FLAGS.file_type
            arr = model.sample(FLAGS.max_length_of_generated, start, converter.vocab_size, converter.word_to_int)
            f = open(file_path, "wb")
            f.write(converter.arr_to_text(arr).encode('utf-8'))
            f.close()


if __name__ == '__main__':
    tf.app.run()
