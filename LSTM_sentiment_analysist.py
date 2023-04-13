import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import re
import urllib.request
import mecab
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import keras
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


class emotionAM:
    def __init__(self) -> None:
        urllib.request.urlretrieve("https://raw.githubusercontent.com/ukairia777/finance_sentiment_corpus/main/finance_data.csv", filename="finance_data.csv")
        data = pd.read_csv('finance_data.csv')
        data['labels'] = data['labels'].replace(['neutral', 'positive', 'negative'],[0, 1, 2])
        del data['sentence']
        data.drop_duplicates(subset=['kor_sentence'], inplace=True)

        meca = mecab.MeCab()
        data['tokenized'] = data['kor_sentence'].apply(meca.morphs)

        X_data = data['tokenized']
        y_data = data['labels']
        X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0, stratify=y_data)

        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(X_train)
        self.loaded_model = load_model("news_NLP/finance_sentiment_corpus/LSTM_sentiment_analusis")

    def predict(self,x):
        X_encoded = self.tokenizer.texts_to_sequences(x)
        max_len = max(len(sent) for sent in x)
        X_encoded = pad_sequences(X_encoded, maxlen=max_len)
        pred = self.loaded_model.predict(X_encoded)

        return pred