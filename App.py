import streamlit as st
from streamlit_chat import message
from MathChat import Bot
import time
from langchain.schema import HumanMessage, AIMessage
bot = Bot.ColumnDivisionBot()
last_interaction_time = time.time()

st.markdown(
    """
    <h1 style='text-align: center;'>Mathter</h1>
    """,
    unsafe_allow_html=True,)
st.markdown(
    """
    <h3 style='text-align: center;'>Hello! Let me know if you're ready for a column division lesson by writing "I'm ready!" and we'll get started!</h3>
    """,
    unsafe_allow_html=True,)
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = bot.init_messages()

response_container = st.container()

container = st.container()


with container:
    with st.form(key = 'main_form', clear_on_submit = True):
        user_input = st.text_area('You:', key = 'input', height = 50)
        submit_button = st.form_submit_button(label='Send')

    # This code can't be compiled because streamlit app don't run continuously, but realisation of checking activity
    # could be done with some js-based solution
    #
    # if (time.time() - last_interaction_time)> 60:
    #     logging.info('ACTIVITY LOST')
    #     bot_response = bot.no_activity_motivation(st.session_state['messages'])
    #     st.session_state['messages'].append((AIMessage(content = bot_response)))
    #     st.session_state['generated'].append(bot_response)
    #     last_interaction_time = time.time()

    if submit_button and user_input:
        last_interaction_time = time.time()
        st.session_state['messages'].append((HumanMessage(content = user_input)))
        bot_response = bot.generate_chat_response(st.session_state['messages'], user_input)
        st.session_state['messages'].append((AIMessage(content = bot_response)))
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(bot_response)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write()
