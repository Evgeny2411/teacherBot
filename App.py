import streamlit as st
from streamlit_chat import message
from MathChat import Bot
from langchain.schema import HumanMessage, AIMessage

bot = Bot.ColumnDivisionBot()

st.markdown(
    """
    <h1 style='text-align: center;'>Mathter</h1>
    """,
    unsafe_allow_html=True,)
st.markdown("Hey there! Let me know if you're ready for the lesson of column division by texting 'I'm ready!' and we'll get started!")
st.markdown("---")

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

    if submit_button and user_input:
        st.session_state['messages'].append((HumanMessage(content = user_input)))
        processing_result = bot.process_message(user_input)
        if processing_result == 'Fine':
            bot_response = bot.generate_response(st.session_state['messages'])
        elif processing_result == 'Offensive':
            bot_response = bot.offensive_input(st.session_state['messages'])
        elif processing_result == 'Distracted':
            bot_response = bot.get_attention(st.session_state['messages'])

        st.session_state['messages'].append((AIMessage(content = bot_response)))
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(bot_response)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write()
