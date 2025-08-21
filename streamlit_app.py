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
        hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3,
    )
    with col1:
        fig_pie.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=200
            )
        st.plotly_chart(fig_pie)
    
    detail = data['내용'].value_counts().reset_index()
    detail.columns = ['내용', '상담건수']
    fig_pie2 = px.pie(
        detail, names='내용', values='상담건수', title='내용별 상담 건수', 
        hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3,
    )
    with col2:
        fig_pie2.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=200
            )
        st.plotly_chart(fig_pie2)
    
    daily = data.groupby('일자').size().reset_index(name='상담건수')
    fig_bar = px.bar(daily, x='일자', y='상담건수', title='일자별 상담 건수',
                        color='일자', color_discrete_sequence=px.colors.qualitative.Pastel)
        
    fig_bar.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=300
            )
    fig_bar.update_xaxes(dtick='D1', tickformat='%Y-%m-%d')
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
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown(f'**🙍‍♀️ 상담사:** Julia')
    with col3:
        st.markdown(f'##### {now}')
    st.write(" ")
    st.sidebar.image('img/툭툭이.png', width=100)
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
        st.subheader('🎧 상담하기')
        
        col1, col2, col3 = st.columns([0.5, 1, 10])
        with col2:
            start = st.select_slider(
                        '상태',
                        options=['OFF', 'ON'],
                        value='OFF',
                        label_visibility='collapsed'
                    )
        
        col1, col2 = st.columns([2,1]) 
        if start == 'ON':
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
            done_rate = (done / total * 100) if total else 0.0

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("총 상담 건수", total, delta='+2')
            with col2:
                st.metric("고객 수", customer)
            with col3:
                st.metric("완료 건수", done, delta='+1')
            with col4:
                st.metric("완료율 (%)", done_rate)
            
            st.divider()
            
            data['일자_날짜'] = pd.to_datetime(data['일자']).dt.date
            daily = (
                data.groupby('일자_날짜').size()
                .reset_index(name='상담건수')
                .sort_values('일자_날짜')
            )
            if not daily.empty:
                fig_line = px.line(
                    daily, x='일자_날짜', y='상담건수',
                    markers=True, title='일자별 상담 건수 추이'
                )
                fig_line.update_layout(
                    margin=dict(l=10, r=10, t=50, b=10),
                    xaxis_title=None, yaxis_title=None
                )
                fig_line.update_xaxes(dtick='D1', tickformat='%Y-%m-%d')
                st.plotly_chart(fig_line)
            
            res = data['결과'].value_counts().reset_index()
            res.columns = ['결과', '상담건수']
            if not res.empty:
                fig_pie = px.pie(
                    res, names='결과', values='상담건수',
                    hole=0.35, title='결과별 비율',
                    color='결과', color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(margin=dict(l=10, r=10, t=50, b=10))
                st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown('###### 상위 이슈 TOP 3')
            top = (
                data['내용'].value_counts().head(3).rename_axis('내용').reset_index(name='상담건수')
            )
            top['순위'] = range(1, len(top) + 1)
            top = top.set_index('순위')
            st.table(top)
            
    elif choice == '검색하기':
        st.subheader('검색')
        
        col1, col2 = st.columns([1, 4])
        
        selected_word = None
                
        with col1:
            st.write('**많이 찾는 내용**')
            if st.button('자격여부'):
                selected_word = '자격여부'
            if st.button('필요서류'):
                selected_word = '필요서류'
        with col2:
            word = st.text_input('검색어를 입력하세요', placeholder='찾고 싶은 매뉴얼을 입력해주세요')
            if word:
                with st.expander(f'**검색어: {word}**', expanded=True):
                    st.write('검색된 내용 쭈루룩')
            elif selected_word:
                with st.expander(f'**검색어: {selected_word}**', expanded=True):
                    st.write(f'검색된 내용 쭈루룩')
    
    else:
        st.subheader('설정 Page')
        st.markdown('##### 상담사 정보')
        col1, col2 = st.columns(2)
        with col1: 
            st.write('**상담사 번호** : aaaa')
        with col2:
            st.write('**상담사 이름** : Julia')
        
        st.divider()
        
        st.markdown('##### 환경 설정')
        st.radio('테마', ['라이트', '다크'], index=0, horizontal=True)
        st.toggle('상담 저장 시 알림 표시', value=True)
        
        st.divider()
        
        st.markdown('##### 데이터 관리')
        st.button('상담 이력 다운로드')
        
    if st.sidebar.button('로그아웃', width=300, type='primary'):
        st.session_state["login"] = False
        st.rerun()       