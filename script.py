import streamlit as st
import time
import g4f  # API Key అవసరం లేని ఉచిత లైబ్రరీ

# Streamlit పేజీ సెటప్
st.set_page_config(page_title="AI తెలుగు కథలు", page_icon="📖", layout="centered")

st.title("📖 అపరిమిత AI తెలుగు కథల జనరేటర్")
st.write("కస్టమర్ ఎన్నిసార్లు క్లిక్ చేసినా ఎర్రర్ రాకుండా బ్యాకప్ మోడల్స్‌తో డిజైన్ చేయబడింది.")

user_prompt = st.text_input("కథ దేని గురించి రాయాలి? (Topic/Idea):", 
                            placeholder="ఉదాహరణ: అనగనగా ఒక రాజు, కాకి-పాము కథ...")

# 1. బ్యాకప్ మోడల్స్ లిస్ట్ (ఒకటి పని చేయకపోతే ఇంకొకటి ఆటోమేటిక్‌గా రన్ అవుతుంది)
AVAILABLE_MODELS = [
    g4f.models.gpt_4o,      # మొదటి ఛాయిస్
    g4f.models.gpt_4,       # బ్యాకప్ 1
    g4f.models.llama_3_1_70b # బ్యాకప్ 2
]

if st.button("🚀 కథను సిద్ధం చేయి"):
    if not user_prompt:
        st.warning("⚠️ కథ రాయడానికి ఏదైనా ఒక టాపిక్ ఇవ్వండి!")
    else:
        full_prompt = f"""
        నువ్వు తెలుగు సాహిత్యంలో ఒక సీనియర్ రచయితవి.
        టాపిక్: "{user_prompt}"
        
        ఈ టాపిక్ ఆధారంగా కనీసం 5-6 పారాగ్రాఫ్‌లు ఉండేలా ఒక అద్భుతమైన, పెద్ద తెలుగు కథను రాయి.
        కథలో మంచి పాత్రల పేర్లు, సంభాషణలు, ఆసక్తికరమైన మలుపులు ఉండాలి.
        కథ చివర్లో ప్రత్యేకంగా "नीति (Moral):" అని పెట్టి ఒక మంచి సందేశాన్ని ఇవ్వు.
        కథ మొత్తం కేవలం స్పష్టమైన తెలుగు లిపి (Telugu Script) లోనే ఉండాలి.
        """
        
        story_generated = False
        
        # 2. ఆటోమేటిక్ రీ-ట్రై లూప్ (ఎర్రర్ రాకుండా కాపాడుతుంది)
        for index, model in enumerate(AVAILABLE_MODELS):
            with st.spinner(f"🤖 AI రచయిత ఆలోచిస్తున్నారు... (Attempt {index + 1})"):
                try:
                    # సర్వర్‌పై లోడ్ తగ్గించడానికి చిన్న గ్యాప్
                    time.sleep(1) 
                    
                    response = g4f.ChatCompletion.create(
                        model=model,
                        messages=[{"role": "user", "content": full_prompt}],
                    )
                    
                    # రెస్పాన్స్ కరెక్ట్‌గా వస్తే డిస్ప్లే చేయడం
                    if response and len(str(response).strip()) > 10:
                        st.success("✨ మీ కథ సిద్ధంగా ఉంది! ✨")
                        st.markdown("---")
                        st.write(response)
                        st.markdown("---")
                        story_generated = True
                        break # కథ జనరేట్ అయిపోయింది కాబట్టి లూప్ ఆపేస్తాం
                        
                except Exception as e:
                    # బ్యాక్‌ఎండ్‌లో ఎర్రర్ వస్తే సైలెంట్‌గా నెక్స్ట్ మోడల్‌కి వెళ్తుంది, కస్టమర్‌కి ఎర్రర్ చూపించదు
                    continue
        
        # 3. ఒకవేళ ఏ మోడల్ కూడా పనిచేయకపోతే సేఫ్ మెసేజ్
        if not story_generated:
            st.error("😥 సర్వర్ చాలా బిజీగా ఉంది. దయచేసి ఒక్క నిమిషం ఆగి మళ్ళీ 'కథను సిద్ధం చేయి' క్లిక్ చేయండి.")
