import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud

@st.dialog("데이터 확인하기", width='large')
def view_raw_data_dialog(data_df):
    num_data = st.number_input("확인할 데이터 수", value=10)
    st.write(data_df.head(num_data))

@st.cache_data
def set_korean_font_for_matplotlib(font_path):
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

@st.cache_data
def visualize_barhgraph(counter, num_words, title, xlabel, ylabel, font_path=None):
    fig, ax = plt.subplots()
    # 고빈도 단어를 num_words 만큼 추출
    wordcount_list = counter.most_common(num_words)

    # x데이터와 y데이터 분리
    x_list = [word for word, count in wordcount_list]
    y_list = [count for word, count in wordcount_list]

    if font_path: set_korean_font_for_matplotlib(font_path)
    # 수평막대그래프 객체 생성
    ax.barh(x_list[::-1], y_list[::-1])

    # 그래프 정보 추가(제목, x, y 레이블)
    if title: ax.set_title(title)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)

    # 화면에 출력
    st.pyplot(fig)

@st.cache_data
def visualize_wordcloud(counter, num_words, font_path=None):
    fig, ax = plt.subplots()
    # wordcloud 객체 생성 (option 지정)
    wc = WordCloud(
        font_path = font_path,
        width = 800,
        height = 600,
        max_words = num_words,
        background_color = 'ivory'
    )

    # 빈도 리스트를 반영한 wordcloud 생성
    wc = wc.generate_from_frequencies(counter)

    # wordcloud를 matplotlib으로 화면에 그리기
    ax.imshow(wc)
    ax.axis('off')
    st.pyplot(fig)