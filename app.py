import streamlit as st
import cohere

# 1. వెబ్‌సైట్ టైటిల్ మరియు సెటప్
st.set_page_config(page_title="నా సొంత AI చాట్‌బాట్", page_icon="🤖")
st.title("🤖 నా సొంత AI చాట్‌బాట్")
st.write("Cohere API మరియు Streamlit తో తయారు చేయబడింది.")

# 2. మీ Cohere API Key ని ఇక్కడ ఎంటర్ చేయండి
COHERE_API_KEY = "EJbzTtucEtxhxczbUqGfTwy5A8sFUvSU4pBLXKJr"

# కాన్ఫిగరేషన్ చెక్
if COHERE_API_KEY == "మీ_API_KEY_ఇక్కడ_పెట్టండి":
    st.warning("దయచేసి మీ Cohere API Key ని కోడ్‌లో అప్‌డేట్ చేయండి!")
else:
    # Cohere క్లయింట్‌ను కనెక్ట్ చేయడం
    co = cohere.Client(COHERE_API_KEY)

    # 3. చాట్ హిస్టరీ (మెసేజ్ రికార్డ్స్) ని సేవ్ చేయడానికి మెమరీ సెటప్
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # స్క్రీన్ పై పాత మెసేజ్‌లను చూపించడం
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. యూజర్ నుండి ప్రశ్న తీసుకోవడం (Chat Input Box)
    if user_query := st.chat_input("నన్ను ఏదైనా అడగండి..."):
        
        # యూజర్ అడిగిన ప్రశ్నను స్క్రీన్ పై చూపించి, మెమరీలో సేవ్ చేయడం
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # AI పాత్రను మరియు మోడల్‌ను సెట్ చేసి రెస్పాన్స్ అడగడం
        with st.chat_message("assistant"):
            with st.spinner("ఆలోచిస్తున్నాను..."):
                response = co.chat(
                    model="command-r-plus-08-2024",
                    message=user_query,
                    preamble="You are a helpful and polite AI Assistant. Answer clearly."
                )
                ai_response = response.text
                st.markdown(ai_response)
        
        # AI ఇచ్చిన సమాధానాన్ని మెమరీలో సేవ్ చేయడం
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
