import streamlit as st

def main():
    st.title("Chat Interface")
    st.markdown("Welcome to the chat! Here, you will learn how to column devise.")

    if 'dialogues' not in st.session_state:
        st.session_state.dialogues = []

    chat_history_placeholder = st.empty()

    user_input = st.text_input("Type your message here...")
    if st.button("Send"):
        st.session_state.dialogues.append(('You', user_input))
        bot_response = "This is a bot response"
        st.session_state.dialogues.append(('Bot', bot_response))

    chat_history_placeholder.markdown('\n\n'.join(f'**{speaker}:** {message}' for speaker, message in st.session_state.dialogues))

if __name__ == "__main__":
    main()