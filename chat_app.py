import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = "gemini-3.8-flash"


@st.cache_resource
def get_client():
    return genai.Client()


def text_step(step_type, text):
    return {'type': step_type, 'content': [{'type': 'text', 'text': text}]}


def stream_text(events):
    # The stream also carries status, thought and start/stop events;
    # only text deltas are part of the visible reply.
    for event in events:
        if event.event_type == 'step.delta' and event.delta.type == 'text':
            yield event.delta.text


st.set_page_config(page_title="Chat with Memory", page_icon="💬")
st.title("💬 Chat with Memory")
st.caption(f"Powered by {MODEL} — the full conversation is sent on every message")

# Streamlit reruns this script on every interaction, so the history
# lives in session_state instead of a plain list.
if 'conversations' not in st.session_state:
    st.session_state.conversations = []

conversations = st.session_state.conversations

with st.sidebar:
    st.subheader("Output settings")
    system_instruction = st.text_area(
        "System instruction",
        value="You are a friendly, concise assistant.",
    )
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.1)
    max_output_tokens = st.slider("Max output tokens", 64, 4096, 1024, 64)
    thinking_level = st.selectbox("Thinking level", ["minimal", "low", "medium", "high"], index=1)

    st.divider()
    st.metric("Messages in history", len(conversations))
    if st.button("Clear chat"):
        conversations.clear()
        st.rerun()

for item in conversations:
    role = 'user' if item['type'] == 'user_input' else 'assistant'
    with st.chat_message(role):
        st.markdown(item['content'][0]['text'])

if user_query := st.chat_input("Say something..."):
    with st.chat_message('user'):
        st.markdown(user_query)
    conversations.append(text_step('user_input', user_query))

    with st.chat_message('assistant'):
        try:
            events = get_client().interactions.create(
                model=MODEL,
                input=conversations,
                stream=True,
                system_instruction=system_instruction,
                generation_config={
                    'temperature': temperature,
                    'max_output_tokens': max_output_tokens,
                    'thinking_level': thinking_level,
                },
            )
            # write_stream shows each chunk as it arrives and returns the full text
            reply = st.write_stream(stream_text(events))
        except Exception as e:
            # Drop the unanswered message so the history stays valid
            conversations.pop()
            st.error(f"Request failed: {e}")
            st.stop()
    conversations.append(text_step('model_output', reply))
    st.rerun()
