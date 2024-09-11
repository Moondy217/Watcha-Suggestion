import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image


# 데이터 불러오기
watcha = pd.read_csv('./watcha.csv')
netflix = pd.read_csv('./netflix.csv')
wavve = pd.read_csv('./wavve.csv')

watcha_list = pd.DataFrame(watcha)
netflix_list = pd.DataFrame(netflix)
wavve_list = pd.DataFrame(wavve)


## 발표자 소개 및 주제 소개
st.markdown('2021204013 문다예')
st.subheader('주제: 유명 OTT 플랫폼들이 보유한 영화 분석 후, 왓챠에게 필요한 영화 탐색')
st.subheader('타깃: 왓챠', divider='rainbow')
st.title('')
st.title('')

st.title('0. 데이터 수집')
st.markdown('- 저스트와치(https://www.justwatch.com/kr/)')
st.markdown('- 왓챠, 웨이브, 넷플릭스가 보유한 영화')
st.markdown('- 개봉연도, 영화제목, 별점')
st.markdown('- 수집 기한은 11월 10일까지')
st.title('')
st.title('')
st.subheader('데이터 수집 과정')

code1 = '''
# watcha, netflix
ott_name = 'netflix'
start = '2019'
end = '2019'

url = f'https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/{ott_name}/%EC%98%81%ED%99%94%EC%82%B0%EC%97%85?release_year_from={start}&release_year_until={end}'

browser.get(url)
time.sleep(1)

# 스크롤 내리는 함수
scroll_to_bottom() 

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(browser.page_source, "html.parser")
movie_list = soup.select('div.title-list-grid > div >  a')'''
st.code(code1, language='python')


code2 = '''for movie in movie_list:
        movie_link = movie['href']
        movie_url = f'https://www.justwatch.com{movie_link}'
        browser.get(movie_url)

        # 랜덤하게 시간 할당
        time.sleep(random.uniform(1,4))

        soup = BeautifulSoup(browser.page_source, "html.parser")
        

        # 영화 이름 추출
        year = soup.select('div > span.text-muted')[0].text.strip()
        movie_name = soup.select('div > h1')[0].text.strip()
        
        # 영화 개봉연도 추출
        year = soup.select('div.jw-info-box.jw-info-box--no-card > div > div.jw-info-box__container-content > div:nth-child(2) > div.title-block__container > div.title-block > div > span')
        movie_year = year.replace('(', '').replace(')', '')
            
        #영화 별점 추출 (IMDB)
        star = soup.select('div.title-info.visible-xs.visible-sm > div:nth-child(1) > div > div > div:nth-child(2) > span')

        if star:
            first_star = star[0]
            star_text = first_star.text.strip()  # '9.2 (1m)' 형태의 문자열
            rating = star_text.split()[0]  # 공백을 기준으로 분리하여 '9.2'만 추출'''
st.code(code2, language='python')
st.title('')
st.title('')





st.title('1. 수집한 데이터')
st.title('')


# 1. 영화 전체 데이터 출력
columns = st.columns(3)

with st.expander("영화 데이터 보기"):

    with columns[0]:
        st.markdown('<p style="text-align:center;">왓챠</p>', unsafe_allow_html=True)
        st.dataframe(watcha_list)

    with columns[1]:
        st.markdown('<p style="text-align:center;">넷플릭스</p>', unsafe_allow_html=True)
        st.dataframe(netflix_list)

    with columns[2]:
        st.markdown('<p style="text-align:center;">웨이브</p>', unsafe_allow_html=True)
        st.dataframe(wavve_list)

# 1-2 영화 총 개수 데이터
with columns[0]:
    total_count = len(watcha_list)
    st.metric("왓챠", value = f'{total_count:,.0f}')

with columns[1]:
    total_count = len(netflix_list)
    st.metric("넷플릭스", value = f'{total_count:,.0f}')

with columns[2]:
    total_count = len(wavve_list)
    st.metric("웨이브", value = f'{total_count:,.0f}')
    

# 보유 영화 랭크
st.title('')
st.title('')
st.subheader('보유 영화 수', divider='rainbow')
st.title('왓챠 > 웨이브 >> 넷플릭스')
st.title('')
st.title('')
image = Image.open('ott.png')
st.image(image, caption='출처: 와이즈앱 ‘2023년 OTT 앱시장 동향 분석’')

# 사용율 랭크
st.title('')
st.title('')
st.subheader('OTT 사용률', divider='rainbow')
st.title('넷플릭스 >> 웨이브 > 왓챠')
st.title('')
st.title('')

# 2. 데이터 분석
st.title('2. 데이터 분석')
st.subheader('2-1. 개봉연도별 영화 개수')



# 2-1. 연도별 영화 그래프 출력
# 개봉년도를 주어진 구간으로 나누어 새로운 열 생성
bins = [1900, 1980, 1990, 2000, 2010, 2020, 2023]
labels = ['1900-1979', '1980-1989', '1990-1999', '2000-2009', '2010-2019', '2020-2023']
watcha['Decade'] = pd.cut(watcha['개봉연도'], bins=bins, labels=labels)
netflix['Decade'] = pd.cut(netflix['개봉연도'], bins=bins, labels=labels)
wavve['Decade'] = pd.cut(wavve['개봉연도'], bins=bins, labels=labels)

# 각 구간의 개수 계산
decade_watcha_counts = watcha['Decade'].value_counts().sort_index()
decade_netflix_counts = netflix['Decade'].value_counts().sort_index()
decade_wavve_counts = wavve['Decade'].value_counts().sort_index()

# Streamlit 그래프 만들기
watcha_chart = alt.Chart(decade_watcha_counts.reset_index()).mark_bar().encode(
    x=alt.X('Decade', title='Decade'),
    y=alt.Y('count', axis=alt.Axis(title='Count', format=".0f", tickMinStep=1000)),
).properties(width=600, height=400, title='왓챠')

st.altair_chart(watcha_chart, use_container_width=True)

st.title('')
netflix_chart = alt.Chart(decade_netflix_counts.reset_index()).mark_bar().encode(
    x=alt.X('Decade', title='Decade'),
    y=alt.Y('count', axis=alt.Axis(title='Count', format=".0f", tickMinStep=1000)),
).properties(width=600, height=400, title='넷플릭스')

st.altair_chart(netflix_chart, use_container_width=True)

st.title('')
wavve_chart = alt.Chart(decade_wavve_counts.reset_index()).mark_bar().encode(
    x=alt.X('Decade', title='Decade'),
    y=alt.Y('count', axis=alt.Axis(title='Count', format=".0f", tickMinStep=1000)),
).properties(width=600, height=400, title='웨이브')

st.altair_chart(wavve_chart, use_container_width=True)



# 2-2 연도별 상세 영화 개수 데이터 프레임 출력
st.title('')
st.title('')
st.subheader('연도별 영화 개수 데이터')
columns = st.columns(3)

with st.expander("연도별 영화 개수 데이터 보기"):

    with columns[0]:
        st.markdown('왓챠', unsafe_allow_html=True)
        st.dataframe(decade_watcha_counts)

    with columns[1]:
        st.markdown('넷플릭스', unsafe_allow_html=True)
        st.dataframe(decade_netflix_counts)

    with columns[2]:
        st.markdown('웨이브', unsafe_allow_html=True)
        st.dataframe(decade_wavve_counts)



# 2-1. 별점 분포 계산
st.title('')
st.title('')
st.subheader('2-2. 별점 분포 - bar 차트')
watcha_rating_counts = watcha['별점'].value_counts().sort_index().reset_index()
netflix_rating_counts = netflix['별점'].value_counts().sort_index().reset_index()
wavve_rating_counts = wavve['별점'].value_counts().sort_index().reset_index()

watcha_rating_counts.columns = ['Rating', 'Count']
netflix_rating_counts.columns = ['Rating', 'Count']
wavve_rating_counts.columns = ['Rating', 'Count']


# Streamlit 앱 만들기
st.markdown('왓챠 별점 분포')

# Altair를 사용하여 별점 분포 그래프 그리기
watcha_rating_chart = alt.Chart(watcha_rating_counts).mark_bar().encode(
    x='Rating:O',
    y='Count:Q',
    tooltip=['Rating:O', 'Count:Q']
)
st.altair_chart(watcha_rating_chart, use_container_width=True)

st.markdown('넷플릭스 별점 분포')

# Altair를 사용하여 별점 분포 그래프 그리기
netflix_rating_chart = alt.Chart(netflix_rating_counts).mark_bar().encode(
    x='Rating:O',
    y='Count:Q',
    tooltip=['Rating:O', 'Count:Q']
)
st.altair_chart(netflix_rating_chart, use_container_width=True)

st.markdown('웨이브 별점 분포')

# Altair를 사용하여 별점 분포 그래프 그리기
wavve_rating_chart = alt.Chart(wavve_rating_counts).mark_bar().encode(
    x='Rating:O',
    y='Count:Q',
    tooltip=['Rating:O', 'Count:Q']
)
st.altair_chart(wavve_rating_chart, use_container_width=True)



st.title('')
st.title('')
st.subheader('2-3. 별점 분포 - boxplot 차트')

# Altair를 사용하여 연도별 별점 분포 그래프 그리기
watcha_chart = alt.Chart(watcha).mark_boxplot().encode(
    x='개봉연도:N',
    y='별점:Q',
    color='개봉연도:N'
).properties(width=600, height=400, title='왓챠')
st.altair_chart(watcha_chart, use_container_width=True)


# Altair를 사용하여 연도별 별점 분포 그래프 그리기
netflix_chart = alt.Chart(netflix).mark_boxplot().encode(
    x='개봉연도:N',
    y='별점:Q',
    color='개봉연도:N'
).properties(width=600, height=400, title='넷플릭스')
st.altair_chart(netflix_chart, use_container_width=True)


# Altair를 사용하여 연도별 별점 분포 그래프 그리기
wavve_chart = alt.Chart(wavve).mark_boxplot().encode(
    x='개봉연도:N',
    y='별점:Q',
    color='개봉연도:N'
).properties(width=600, height=400, title='웨이브')
st.altair_chart(wavve_chart, use_container_width=True)


st.title('')
st.title('')
st.title('3. 분석 결과')
st.subheader('')
st.markdown('넷플릭스: 최신 영화 독점')
st.markdown('웨이브: 왓챠와 영화 보유 수는 비슷하지만 드라마 및 예능으로 점유율 확보')
st.markdown('왓챠: 영화 보유 수는 많지만 타 OTT와 경쟁 속에서 어필하기에는 다소 부족')

st.title('')
st.title('')
st.subheader('왓챠: 1970년도 이전 고전 영화를 들여옴으로써 새로운 OTT 길 개척')
st.markdown('- 타 OTT는 고전 영화 수가 많지 않음')
st.markdown('- 고전 영화의 경우 별점 분포가 높음')
st.markdown('- 최신 영화보다 비용이 저렴')




