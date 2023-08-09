import streamlit as st
from MathChat import Bot

bot = Bot.ColumnDivisionBot()

def main():
    st.title("AI Teacher")
    st.markdown("Hey there! Want to learn column division? Let me know if you're ready for the lesson by texting 'Ready!' and we'll get started!")

    if 'dialogues' not in st.session_state:
        st.session_state.dialogues = []

    chat_history_placeholder = st.empty()

    user_input = st.text_input("Type your answer!")
    if st.button("Send"):
        st.session_state.dialogues.append(('You', user_input))
        bot_response = bot.generate_response(user_input)
        st.session_state.dialogues.append(('Bot', bot_response))

    chat_history_placeholder.markdown('\n\n'.join(f'**{speaker}:** {message}' for speaker, message in st.session_state.dialogues))

if __name__ == "__main__":
    main()