import time

import tensorflow as tf
from read_utils import TextConverter, batch_generator
from model import CharRNN
import os
import codecs
from db_operation import *

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('name', 'js', 'name of the model')
tf.flags.DEFINE_integer('num_seqs', 64, 'number of seqs in one batch')
tf.flags.DEFINE_integer('num_steps', 64, 'length of one seq')
tf.flags.DEFINE_integer('lstm_size', 256, 'size of hidden state of lstm')
tf.flags.DEFINE_integer('num_layers', 2, 'number of lstm layers')
tf.flags.DEFINE_boolean('use_embedding', False, 'whether to use embedding')
tf.flags.DEFINE_integer('embedding_size', 128, 'size of embedding')
tf.flags.DEFINE_float('learning_rate', 0.01, 'learning_rate')
tf.flags.DEFINE_float('train_keep_prob', 0.5, 'dropout rate during training')
tf.flags.DEFINE_string('input_file', '', 'utf8 encoded text file')
tf.flags.DEFINE_integer('max_steps', 200000, 'max steps to train')
tf.flags.DEFINE_integer('validate_every_n_steps', 1000, 'save the model every n steps')
tf.flags.DEFINE_integer('log_every_n', 10, 'log to the screen every n steps')
tf.flags.DEFINE_integer('max_vocab', 5000, 'max char number')


def main(_):
    model_path = os.path.join('model', FLAGS.name)
    if os.path.exists(model_path) is False:
        os.makedirs(model_path)
    print("---------------------------- Reading Corpus ----------------------------")
    start_time = time.time()
    read_corpus()
    print("Read Corpus Finished in " + str(time.time() - start_time) + ' Seconds.')

    converter = TextConverter(training_corpus, FLAGS.max_vocab)
    converter.save_to_file(os.path.join(model_path, 'converter.pkl'))

    training_vector_array = converter.text_to_arr(training_corpus)
    validating_vector_array = converter.text_to_arr(validating_corpus)

    training_batch_generator = batch_generator(training_vector_array, FLAGS.num_seqs, FLAGS.num_steps)
    validating_batch_generator = batch_generator(validating_vector_array, FLAGS.num_seqs, FLAGS.num_steps)

    model = CharRNN(converter.vocab_size,
                    validating_batch_generator,
                    num_seqs=FLAGS.num_seqs,
                    num_steps=FLAGS.num_steps,
                    lstm_size=FLAGS.lstm_size,
                    num_layers=FLAGS.num_layers,
                    learning_rate=FLAGS.learning_rate,
                    train_keep_prob=FLAGS.train_keep_prob,
                    use_embedding=FLAGS.use_embedding,
                    embedding_size=FLAGS.embedding_size
                    )
    model.train(training_batch_generator,
                FLAGS.max_steps,
                model_path,
                FLAGS.validate_every_n_steps,
                FLAGS.log_every_n,
                )


def read_corpus():
    global training_corpus, validating_corpus
    training_corpus = ''
    validating_corpus = ''
    source_list = query_all()
    training_corpus_percentage = 0.9
    training_corpus_length = int(len(source_list) * training_corpus_percentage) + 1
    for i in range(0, training_corpus_length):
        try:
            training_corpus += (source_list[i][1] + '\n')
        except RuntimeError:
            pass

    for i in range(training_corpus_length, len(source_list)):
        try:
            validating_corpus += (source_list[i][1] + '\n')
        except RuntimeError:
            pass


if __name__ == '__main__':
    tf.app.run()
