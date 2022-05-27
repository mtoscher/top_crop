import streamlit as st
import pandas as pd
import random
import numpy as np

all = pd.read_csv('all_production_quiz_small.csv')

#st.markdown(page_bg_img, unsafe_allow_html=True)

#st.markdown('<style>body{background-color: Blue;}</style>',unsafe_allow_html=True)

st.title("TOP CROP")
 
st.write("""Let's play this quiz to see how much you know about where our food grows.""")

countries = all.Area.unique()
years = all.Year.unique()
years.sort()

st.session_state['country'] = st.selectbox('Select a country:', countries)
st.session_state['year'] = st.selectbox('Select a year:', years)

selection = all[all.Area == st.session_state['country']][all.Year == st.session_state['year']]
selection = selection[['Item', 'Value']][selection.Value > 0.0].sort_values(by='Value').set_index('Item')

if not selection.empty: 

    if 'quiz' not in st.session_state:
      max = selection[selection.Value == selection.Value.max()]
      selection_min = selection.drop(index=max.index)
      if len(selection_min) > 2:
          st.session_state['sample'] = selection_min.sample(n=4-len(max))
          shuffler = [0, 1, 2, 3]
      else:
          st.session_state['sample'] = selection_min
      shuffler = []
      for i in range(len(st.session_state['sample'])+1):
          shuffler.append(i)
      random.shuffle(shuffler)
      quiz = st.session_state['sample'].append(max)
      quiz['order'] = shuffler
      quiz = quiz.reset_index()
      default = [{'Item': 'default' ,'Value': 0, 'order': -1}]
      st.session_state['quiz'] = quiz.append(default).sort_values('order').set_index('Item')

    st.markdown(
        """ <style>
                div[role="radiogroup"] >  :first-child{
                    display: none !important;
                }
            </style>
            """,
        unsafe_allow_html=True
    )

    st.write(f'Which one was the top crop of {st.session_state.country} in {st.session_state.year}?')
    st.session_state['choice'] = st.radio(label='Unit is in tonnes. Except for eggs, where it is in 1000.', options=st.session_state['quiz'].index)

    #st.session_state

    if st.session_state['quiz'][st.session_state['quiz'].index == st.session_state['choice']]['Value'][0] == st.session_state['quiz'].Value.sort_values(ascending=False)[0]:
        st.title(f'HOORAY! :rocket: {st.session_state.choice} is correct! You nailed it!')
        st.balloons()
        for key in st.session_state.keys():
            del st.session_state[key]
    elif st.session_state['choice'] == 'default':
        st.write('You need to select one of the crops.')
    else:
        st.error(f'Congratulations on trying. Unfortunately, {st.session_state.choice} is awfully wrong, really. :see_no_evil:')

else:
    st.write("Oh no! It's the dreaded missing data alert! Pick another country-year combination.")