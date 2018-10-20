import tensorflow as tf
from convertor import TextConverter
from model import CharRNN
import os
from post_processor import *

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('file_type', 'js', 'name of the model')
tf.flags.DEFINE_integer('lstm_size', 128, 'size of hidden state of lstm')
tf.flags.DEFINE_integer('num_layers', 2, 'number of lstm layers')
tf.flags.DEFINE_boolean('use_embedding', False, 'whether to use embedding')
tf.flags.DEFINE_integer('embedding_size', 128, 'size of embedding')
tf.flags.DEFINE_string('converter_path', 'model/js/converter.pkl', 'model/name/converter.pkl')
tf.flags.DEFINE_string('checkpoint_path', 'model/js/', 'checkpoint path')
tf.flags.DEFINE_string('start_string', '《', 'use this string to start generating')
tf.flags.DEFINE_integer('max_length', 2000, 'max length to generate')
tf.flags.DEFINE_string('generated_folder', '../../BrowserFuzzingData/generated/', 'Path of Generated Folder')


def main(_):
    converter = TextConverter(filename=FLAGS.converter_path)
    if os.path.isdir(FLAGS.checkpoint_path):
        FLAGS.checkpoint_path = \
            tf.train.latest_checkpoint(FLAGS.checkpoint_path)

    model = CharRNN(converter.vocab_size, sampling=True,
                    lstm_size=FLAGS.lstm_size, num_layers=FLAGS.num_layers,
                    use_embedding=FLAGS.use_embedding,
                    embedding_size=FLAGS.embedding_size)

    model.load(FLAGS.checkpoint_path)

    start = converter.text_to_arr(FLAGS.start_string)

    # JS/Html/CSS
    for i in range(0, 10):
        print('Generating: ' + str(i))
        file_path = '../../BrowserFuzzingData/generated/' + FLAGS.file_type + '/' + str(i) + '.' + FLAGS.file_type
        f = open(file_path, "x")
        arr = model.sample(FLAGS.max_length, start, converter.vocab_size)
        content = converter.arr_to_text(arr)
        content = content.replace("\\t", "\t")
        content = content.replace("\\r", "\r")
        content = content.replace("\\n", "\n")

        if FLAGS.file_type.__eq__('js'):
            f.write(content)
            f.close()
        elif FLAGS.file_type.__eq__('html'):
            content = post_process(content)
            f.write(content)
            f.close()
        # TODO: 预留给CSS，暂不作任何处理
        else:
            pass
    execute_post_process()


if __name__ == '__main__':
    tf.app.run()
