import streamlit as st

st.title("Hello, Streamlit World")

name = "sungmin"
st.title(f'Hello, {name}. Welcome~~~')
# st.write(f'Hello, {name}. Welcome~~~')
# st.header(f'Hello, {name}. Welcome~~~')
# st.subheader(f'Hello, {name}. Welcome~~~')
# st.success(f'Hello, {name}. Welcome~~~')
# st.warning(f'Hello, {name}. Welcome~~~')
# st.info(f'Hello, {name}. Welcome~~~')
# st.error(f'Hello, {name}. Welcome~~~')

# '다음은 데이터프레임의 출력 예시입니다.'

'''
다음은 데이터프레임의 출력 예시입니다.
magic command를 확인할 수 있습니다.
'''

import pandas as pd
df = pd.DataFrame({
    'A' : [1, 2, 3, 4],
    'B' : [10, 20, 30, 40]
})

df

import time
text = st.info('텍스트가 변할겁니다.')
time.sleep(2)
text.success('2초가 지났습니다.')