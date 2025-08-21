import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import plotly.express as px

data = pd.DataFrame({
        '일자': ['2025-08-20','2025-08-21', '2025-08-20', '2025-08-20', '2025-08-21'],
        '고객명': ['김철수','이영희', '김철수', '홍길동', '김영희'],
        '내용': ['대출문의','서류보완', '단순민원', '대출문의', '대출문의'],
        '결과':['완료', '진행중', '완료', '진행중', '진행중']
        })

def show_category_charts(data):
    col1, col2 = st.columns([1, 1])    
    result = data['결과'].value_counts().reset_index()
    result.columns = ['결과', '상담건수']
    fig_pie = px.pie(
        result, names='결과', values='상담건수', title='결과별 상담 건수', 
        hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3
    )
    with col1:
        st.plotly_chart(fig_pie)
    
    detail = data['내용'].value_counts().reset_index()
    detail.columns = ['내용', '상담건수']
    fig_pie2 = px.pie(
        detail, names='내용', values='상담건수', title='내용별 상담 건수', 
        hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3
    )
    with col2:
        st.plotly_chart(fig_pie2)
    
    daily = data.groupby('일자').size().reset_index(name='상담건수')
    fig_bar = px.bar(daily, x='일자', y='상담건수', title='일자별 상담 건수',
                        color='일자', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_bar)
    

if 'login' not in st.session_state:
    st.session_state['login'] = False
    
if not st.session_state['login']:
    with st.expander(('**툭툭 상담 지원 시스템**'), expanded=True):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.image('img/툭툭이2.png', width=100)
                st.write('상담사 로그인')

            agent_num = st.text_input('상담사 번호', placeholder='상담사 번호를 입력하세요', label_visibility='hidden')

            if st.button('상담 시작', width=400):
                st.session_state['login'] = True
                st.session_state['agent_num'] = agent_num
                st.rerun()
            
else:
    KST = ZoneInfo('Asia/Seoul')
    now = datetime.now(KST).strftime('%Y-%m-%d (%a) %H:%M')
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown(f'**🙍‍♀️ 상담사:** Julia')
    with col3:
        st.markdown(f'##### {now}')
    st.divider()
    
    st.sidebar.header('상담사 메뉴')
    choice = st.sidebar.radio(
                '메뉴 선택',
                ['--- 선택하세요 ---', '상담 시작하기', '나의 상담 이력', '검색하기', '설정'],
                
            )
    
    if choice == '--- 선택하세요 ---':
        col1, col2 = st.columns([1, 8])
        with col1:
            st.image('img/툭툭이2.png', width=60)
        with col2:
            st.info('왼쪽 메뉴에서 기능을 선택해주세요. 😊')
        show_category_charts(data)
          
    elif choice == '상담 시작하기':
        st.subheader('🟢상담하기🟢')
        start = st.toggle('start!')
        
        col1, col2 = st.columns([2,1]) 
        if start:
            with col2:    
                st.text_area('툭툭의 추천 응답', placeholder='자동 생성')
            with col1:
                st.text_input('고객명', placeholder='고객명을 입력해주세요')
                st.text_area('대화 내용', placeholder='자동 출력 창')
                
        
        memo = st.text_area('상담 메모')
        st.button('저장')

    elif choice == '나의 상담 이력':
        st.subheader('나의 상담 이력')
        
        tab1, tab2, tab3 = st.tabs(["전체 이력", "카테고리별", "요약 통계"])
        
        with tab1:
            st.dataframe(data)
        with tab2:
            show_category_charts(data)
        with tab3:
            total = len(data)
            customer = data['고객명'].nunique()
            done = (data['결과'] == '완료').sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("총 상담 건수", total)
            col2.metric("고객 수", customer)
            col3.metric("완료 건수", done)
            
    elif choice == '검색하기':
        st.subheader('상담 이력 검색')
        st.text_input('검색어를 입력하세요')
        
    else:
        st.subheader('설정')
    
    
    
    
    if st.sidebar.button('로그아웃', width=300):
        st.session_state["login"] = False
        st.rerun()       