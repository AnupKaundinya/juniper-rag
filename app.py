import streamlit as st
from query import query

st.set_page_config(page_title="Juniper Switch Assistant", page_icon="🔀")
st.title("Juniper Switch Assistant")
st.caption("Ask anything about the EX or QFX line of switches.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about Juniper switches..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching datasheets..."):
            answer, sources = query(prompt)
        st.markdown(answer)
        with st.expander("Sources"):
            for s in set(sources):
                st.write(f"- {s}")

    st.session_state.messages.append({"role": "assistant", "content": answer})

     