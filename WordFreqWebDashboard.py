import streamlit as st

from mylib import myTextAnalyzer as ta
from mylib import myStreamlitVisualizer as sv

import pandas as pd
from konlpy.tag import Okt

font_path = "c:/Windows/Fonts/malgun.ttf"

st.set_page_config(
    page_title="단어 빈도수 분석 웹 대시보드",
)

tag_dic = {
    "명사" : "Noun",
    "대명사" : "Pronoun",
    "동사" : "Verb",
    "형용사" : "Adjective",
    "부사" : "Adverb",
    "전치사" : "Preposition",
    "접속사" : "Conjunction",
    "감탄사" : "Interjection"
}

with st.sidebar:
    data_file = st.file_uploader("파일 선택", type=['csv'])
    column_name = st.text_input('데이터가 있는 컬럼명', value='review')
    if st.button("데이터 파일 확인"): 
        if data_file:
            data_df = pd.read_csv(data_file)
            sv.view_raw_data_dialog(data_df)
        else:
            st.sidebar.warning("데이터 파일을 업로드 후 데이터를 확인하세요.")
    tag_multiselect = st.multiselect("분석할 품사를 선택하세요", options=list(tag_dic.keys()))
    ta.init_state()
    if st.button("불용어 설정"):
        ta.stop_word_input()
    st.write("## 설정")
    with st.form('my_form'):
        freq = st.checkbox('빈도수 그래프', value=True)
        num_words = st.slider('단어 수', 10, 50, 10, 1)
        title = st.text_input('제목')
        xlabel = st.text_input('X축')
        ylabel = st.text_input('Y축')
        wc = st.checkbox('워드클라우드')
        num_wc_words = st.slider('단어 수', 20, 500, 20, 10)
        submitted = st.form_submit_button('분석 시작')

st.title('단어 빈도수 시각화')
status = st.info('분석할 파일을 업로드하고, 시각화 수단을 선택한 후 "분석 시작" 버튼을 클릭하세요.')

if submitted:
    if not data_file:
        st.error('분석할 데이터 파일을 업로드 한 후 분석 시작하세요.')
        exit()

    status.info('데이터를 분석 중입니다.')

    corpus = ta.load_corpus_from_csv(data_file, column_name)
    if not corpus:
        st.error(f"분석할 컬럼명 '{column_name}'을 확인하고 다시 입력해주세요.")
        exit()

    my_tags = [tag_dic[tag] for tag in tag_multiselect]
    my_stopwords = st.session_state.word_list

    tokenizer = Okt().pos
    pos_list = ta.tokenize_korean_corpus(corpus, tokenizer, my_tags, my_stopwords)
    
    counter = ta.analyze_word_freq(pos_list)

    status.info(f'분석이 완료되었습니다 ({len(corpus):,}개의 리뷰, {counter.total():,}개의 단어)')

    if freq: sv.visualize_barhgraph(counter, num_words, title, xlabel, ylabel, font_path)
    if wc: sv.visualize_wordcloud(counter, num_wc_words, font_path)
    if not freq and not wc:
        st.warning('빈도수 그래프 또는 워드클라우드 중 하나 이상을 선택하세요.')
        
    