from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, SimpleRNN
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
import re

# Максимальное количество слов
num_words = 15000
# Максимальная длина новости
max_news_len = 100


def make_set(path):
    return pd.read_csv(path,
                       header=None,
                       names=['class', 'title'],
                       encoding='latin-1')


def make_y_class(arr):
    arr_class = []
    positive = 0
    negative = 0
    for i in arr:
        if i == "positive":
            arr_class.append(1)
            positive += 1
        if i == "negative":
            arr_class.append(0)
            negative += 1
    return arr_class


def preprocess_text(text):
    text = text.lower().replace("ё", "е")
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'USER', text)
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
    text = re.sub('([A-Za-z]{3}\-\d{2}-\d{2}\s)?\d{2}\:\d{2}[A|P][M]', ' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip()


def make_network():
    dataset = make_set('C:\\Users\\Illia\\PycharmProjects\\diplom_2\\utils\\new_dataset.csv')
    news = [preprocess_text(t) for t in dataset['title']]
    label = make_y_class(dataset['class'])
    news_2, x_test, y_train, y_test = train_test_split(news, label, test_size=0.1, random_state=38)
    tokenizer = Tokenizer(num_words=num_words)
    tokenizer.fit_on_texts(news_2)
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    sequences = tokenizer.texts_to_sequences(news_2)
    x_train = pad_sequences(sequences, maxlen=max_news_len)
    model = Sequential()
    model.add(Embedding(num_words, 2, input_length=max_news_len))
    model.add(SimpleRNN(8))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model_save_path = 'best_model.h5'
    checkpoint_callback = ModelCheckpoint(model_save_path,
                                          monitor='val_accuracy',
                                          save_best_only=True,
                                          verbose=1)
    history = model.fit(np.array(x_train),
                        np.array(y_train),
                        epochs=10,
                        batch_size=128,
                        validation_split=0.2,
                        callbacks=[checkpoint_callback])
    plt.plot(history.history['accuracy'],
             label='Доля верных ответов на обучающем наборе')
    plt.plot(history.history['val_accuracy'],
             label='Доля верных ответов на проверочном наборе')
    plt.xlabel('Эпоха обучения')
    plt.ylabel('Доля верных ответов')
    plt.legend()
    plt.show()

    test_sequences = tokenizer.texts_to_sequences(x_test)
    x_test = pad_sequences(test_sequences, maxlen=max_news_len)
    model.load_weights(model_save_path)
    model.evaluate(np.array(x_test), np.array(y_test), verbose=1)