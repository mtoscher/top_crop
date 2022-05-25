import streamlit as st
import pandas as pd
import random
import numpy as np

all = pd.read_csv('all_production_quiz_small.csv')

st.title("TOP CROPS")
 
st.write("""Let's play this quiz to see how much you know about where our food grows.""")

countries = all.Area.unique()
#countries = np.insert(countries, 0, '')
years = all.Year.unique()
years.sort()

st.session_state['country'] = st.selectbox('Select a country:', countries)
st.session_state['year'] = st.selectbox('Select a year:', years)

selection = all[all.Area == st.session_state['country']][all.Year == st.session_state['year']]
selection = selection[['Item', 'Value', 'Unit']][selection.Value > 0.0].sort_values(by='Value').set_index('Item')

if not selection.empty: 

    if 'quiz' not in st.session_state:
      max = selection[selection.Value == selection.Value.max()]
      st.session_state['sample'] = selection.sample(n=3)
      shuffler = [0, 1, 2, 3]
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

    if st.session_state['choice'] == st.session_state['quiz'].Value.sort_values(ascending=False).head(1).index:
        st.title(f'HOORAY! :rocket: {st.session_state.choice} is correct! You nailed it!')
        for key in st.session_state.keys():
            del st.session_state[key]
    elif st.session_state['choice'] == 'default':
        t.write('You need to select one of the crops.')
    else:
        st.write(f'Congratulations on trying. Unfortunately, {st.session_state.choice} is awfully wrong, really. :see_no_evil:')

else:
    st.write("Oh no! It's the dreaded missing data alert! Pick another country-year combination.")