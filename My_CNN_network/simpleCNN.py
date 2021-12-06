import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.python.keras.models import Sequential
from Test_network.test import num_words, max_news_len, preprocess_text


def call_network(text):
    model = Sequential()
    model.add(Embedding(num_words, 2, input_length=max_news_len))
    model.add(SimpleRNN(8))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model_save_path = 'C:\\Users\\Illia\\Documents\\Diploma_2021\\diplom_final\\utils\\best_mode_77.h5'
    model.load_weights(model_save_path)
    with open('C:\\Users\\Illia\\Documents\\Diploma_2021\\diplom_final\\utils\\tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    new_text = [preprocess_text(t) for t in text]
    sequence = tokenizer.texts_to_sequences(new_text)
    data = pad_sequences(sequence, maxlen=max_news_len)
    result = model.predict(data)
    return result
