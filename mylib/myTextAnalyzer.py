import pandas as pd
import streamlit as st
from collections import Counter

@st.cache_data
def load_corpus_from_csv(data_filename, column):
    data_df = pd.read_csv(data_filename)
    corpus = list(data_df[column])
    if data_df[column].isnull().sum():
        data_df.dropna(subset=[column], inplace=True)
    return corpus

def init_state():
    if "word_list" not in st.session_state:
        st.session_state.word_list = []

@st.dialog("불용어 추가하기")
def stop_word_input():
    st.write("단어를 입력하고 Enter를 누르면 입력됩니다.")

    st.text_input("단어 입력", key="word_input", on_change=add_word)

    if st.session_state.word_list:
        st.write("추가된 단어 : ")
        words_str = ", ".join(st.session_state.word_list)
        st.info(words_str)
        
        if st.button("초기화"):
            st.session_state.word_list = []

    if st.button("닫기"):
        st.rerun()

def add_word():
    new_word = st.session_state.word_input.strip()
    
    if new_word and new_word not in st.session_state.word_list:
        st.session_state.word_list.append(new_word)
    
    st.session_state.word_input = ""

@st.cache_data
def tokenize_korean_corpus(corpus, _tokenizer, my_tags=None, my_stopwords=None):
    all_tokens = []
    if my_tags and my_stopwords:
        for text in corpus:
            tokens = [word for word, tag in _tokenizer(text) if tag in my_tags and word not in my_stopwords]
            all_tokens += tokens
    elif my_tags:
        for text in corpus:
            tokens = [word for word, tag in _tokenizer(text) if tag in my_tags]
            all_tokens += tokens
    elif my_stopwords:
        for text in corpus:
            tokens = [word for word, tag in _tokenizer(text) if word not in my_stopwords]
            all_tokens += tokens
    else:
        for text in corpus:
            tokens = [word for word, tag in _tokenizer(text)]
            all_tokens += tokens
    return all_tokens

def analyze_word_freq(tokens):
    return Counter(tokens)

from matplotlib import font_manager, rc
def set_korean_font_for_matplotlib(font_path):
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)