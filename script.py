import streamlit as st
import time
from google import genai
from google.genai import errors

# Streamlit పేజీ సెటప్
st.set_page_config(page_title="AI తెలుగు కథలు", page_icon="📖", layout="centered")

st.title("📖 అపరిమిత AI తెలుగు కథల జనరేటర్")
st.write("గూగుల్ అఫీషియల్ ఫ్రీ మోడల్‌తో 100% గ్యారెంటీగా పనిచేస్తుంది.")

# Streamlit Secrets నుండి API Key ని రీడ్ చేయడం
# (మీరు కాపీ చేసిన API Key ని Streamlit Settings లో "GEMINI_API_KEY" పేరుతో పెట్టండి)
api_key = st.secrets.get("GEMINI_API_KEY")

user_prompt = st.text_input("కథ దేని గురించి రాయాలి? (Topic/Idea):", 
                            placeholder="ఉదాహరణ: అనగనగా ఒక రాజు, కాకి-పాము కథ...")

if st.button("🚀 కథను సిద్ధం చేయి"):
    if not api_key:
        st.error("⚠️ Streamlit Secrets లో GEMINI_API_KEY కాన్ఫిగర్ చేయలేదు! దయచేసి సెట్టింగ్స్ చెక్ చేయండి.")
    elif not user_prompt:
        st.warning("⚠️ కథ రాయడానికి ఏదైనా ఒక టాపిక్ ఇవ్వండి!")
    else:
        full_prompt = f"""
        nuvvu telugu sahityam mariyu jaanapada kathalalo oka senior rachayithavi (Senior Telugu Story Teller).
        Topic: "{user_prompt}"
        
        Ee topic aadharanga kaneesam 5-6 paragraphs unde la oka adbhuthamaina, pedda telugu kathanu rayi.
        Kathalo manchi paathrala perlu, sambhashanalu, aasakthikaramaina malupulu mariyu spashtamaina mugimpu undali.
        Katha chivarlo prathyekanga "नीति (Moral):" ani petti oka manchi sandesanni ivvu.
        Katha motham kevalam spashtamaina Telugu Script lone undali.
        """
        
        story_generated = False
        max_retries = 3  # ఒకవేళ సర్వర్ బిజీగా ఉంటే 3 సార్లు ప్రయత్నిస్తుంది
        
        # గూగుల్ జెమిని క్లయింట్ ఇనిషియలైజేషన్
        client = genai.Client(api_key=api_key)
        
        for attempt in range(max_retries):
            with st.spinner(f"🤖 AI రచయిత కథను ఆలోచిస్తున్నారు... (Attempt {attempt + 1})"):
                try:
                    # గూగుల్ వారి సరికొత్త మరియు ఫాస్టెస్ట్ ఫ్రీ మోడల్ (gemini-2.5-flash)
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=full_prompt,
                    )
                    
                    if response.text:
                        st.success("✨ మీ కథ సిద్ధంగా ఉంది! ✨")
                        st.markdown("---")
                        st.write(response.text)
                        st.markdown("---")
                        story_generated = True
                        break  # సక్సెస్ అయింది కాబట్టి లూప్ ఆపేస్తాం
                        
                except errors.APIError as e:
                    # సర్వర్ ఓవర్‌లోడ్ (Rate Limit) అయితే 2 సెకన్లు ఆగి మళ్ళీ ట్రై చేస్తుంది
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        st.error(f"గూగుల్ సర్వర్ బిజీగా ఉంది. దయచేసి కొద్దిసేపటి తర్వాత ప్రయత్నించండి.")
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        st.error("ఏదో చిన్న సాంకేతిక లోపం వచ్చింది. మళ్ళీ క్లిక్ చేయండి.")
        
        if not story_generated:
            st.info("💡 ఒకవేళ ఎర్రర్ వస్తూనే ఉంటే, మీ AI Studio లో కొత్త API Key ని క్రియేట్ చేసి మార్చండి.")
