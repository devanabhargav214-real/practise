import streamlit as st
import os
import google.generativeai as genai

# Streamlit పేజీ సెటప్
st.set_page_config(page_title="AI తెలుగు కథలు", page_icon="📖", layout="centered")

st.title("📖 AI తెలుగు కథల జనరేటర్")
st.write("టాపిక్ ఎంటర్ చేసి 'కథను సిద్ధం చేయి' బటన్ క్లిక్ చేయండి.")

# Streamlit Secrets నుండి API Key ని రీడ్ చేయడం
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Streamlit Secrets లో GEMINI_API_KEY కాన్ఫిగర్ చేయలేదు!")

# కస్టమర్ కేవలం టాపిక్ మాత్రమే ఇస్తారు
user_prompt = st.text_input("కథ దేని గురించి రాయాలి? (Topic/Idea):", 
                            placeholder="ఉదాహరణ: తెనాలి రామకృష్ణ కథలు, ఒక తెలివైన కాకి...")

if st.button("🚀 కథను సిద్ధం చేయి"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key అందుబాటులో లేదు. దయచేసి సెట్టింగ్స్ చెక్ చేయండి.")
    elif not user_prompt:
        st.warning("కథ రాయడానికి ఏదైనా ఒక టాపిక్ ఇవ్వండి!")
    else:
        with st.spinner("🤖 AI తెలుగు రచయిత కథను ఆలోచిస్తోంది... కాసేపు ఆగండి..."):
            try:
                # జెమిని మోడల్ సెటప్ (త్వరితగతిన మరియు అద్భుతంగా పనిచేస్తుంది)
                # దీనితో మార్చండి (ఇలా ఇస్తే 100% పనిచేస్తుంది):
                model = genai.GenerativeModel("models/gemini-1.5-flash")

                # AI కి ఇచ్చే స్ట్రిక్ట్ ఇన్‌స్ట్రక్షన్స్ (పెద్ద కథ రావడం కోసం)
                full_prompt = f"""
                నువ్వు తెలుగు సాహిత్యం మరియు జానపద కథలలో ఒక సీనియర్ రచయితవి (Senior Telugu Story Teller).
                టాపిక్: "{user_prompt}"
                
                ఈ టాపిక్ ఆధారంగా కనీసం 5-6 పారాగ్రాఫ్‌లు ఉండేలా ఒక అద్భుతమైన, పెద్ద తెలుగు కథను రాయి.
                కథలో మంచి పాత్రల పేర్లు, సంభాషణలు (dialogues), ఆసక్తికరమైన మలుపులు (twists) మరియు స్పష్టమైన ముగింపు ఉండాలి.
                కథ చివర్లో ప్రత్యేకంగా "నీతి (Moral):" అని పెట్టి ఒక మంచి సందేశాన్ని ఇవ్వు.
                కథ మొత్తం కేవలం స్పష్టమైన తెలుగు లిపి (Telugu Script) లోనే ఉండాలి.
                """
                
                # కథను జనరేట్ చేయడం
                response = model.generate_content(full_prompt)
                
                # రిజల్ట్ డిస్ప్లే
                st.success("✨ మీ కథ సిద్ధంగా ఉంది! ✨")
                st.markdown("---")
                st.write(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"ఏదో తప్పు జరిగింది: {e}")
            
