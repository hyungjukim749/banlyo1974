import streamlit as st
from PIL import Image
import random
from datetime import datetime

class RepairChatbot:
    def __init__(self):
        self.responses = {
            "신발": [
                "신발 수선은 저희 전문 분야입니다! 어떤 부분이 문제인가요?",
                "신발 수선 가능합니다. 구체적인 상태를 알려주시면 더 자세히 안내해드릴게요.",
                "신발 수선은 보통 3-5일 정도 소요됩니다. 어떤 종류의 신발인가요?"
            ],
            "가방": [
                "가방 수선도 가능합니다! 어떤 부분이 고장났나요?",
                "가방 수선은 상태에 따라 2-4일 정도 걸립니다.",
                "가방 수선은 전문가가 직접 확인 후 견적을 알려드립니다."
            ],
            "옷": [
                "옷 수선도 가능합니다! 어떤 부분을 수선하고 싶으신가요?",
                "옷 수선은 보통 1-2일 정도 소요됩니다.",
                "옷 수선은 종류와 상태에 따라 가격이 다를 수 있습니다."
            ],
            "가격": [
                "수선 가격은 상태와 종류에 따라 다릅니다. 구체적으로 말씀해 주시면 더 정확한 견적을 알려드릴 수 있습니다.",
                "기본 수선은 5,000원부터 시작합니다. 자세한 견적은 상태 확인 후 안내해드립니다.",
                "수선 가격은 직접 확인 후 정확한 견적을 알려드립니다."
            ],
            "기본": [
                "반려1974에 오신 것을 환영합니다! 어떤 도움이 필요하신가요?",
                "안녕하세요! 수선 상담 도와드리겠습니다.",
                "반갑습니다! 어떤 물건을 수선하고 싶으신가요?"
            ]
        }
    
    def get_response(self, user_input):
        # 시간대별 인사
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            greeting = "좋은 아침이에요! "
        elif 12 <= current_hour < 17:
            greeting = "좋은 오후에요! "
        elif 17 <= current_hour < 22:
            greeting = "좋은 저녁이에요! "
        else:
            greeting = "안녕하세요! "
        
        # 키워드 기반 응답
        for keyword in self.responses:
            if keyword in user_input:
                return greeting + random.choice(self.responses[keyword])
        
        # 기본 응답
        return greeting + random.choice(self.responses["기본"])

def main():
    st.set_page_config(
        page_title="반려1974 수선 상담",
        page_icon="👞",
        layout="wide"
    )
    
    # CSS 스타일
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .chat-message.user {
            background-color: #E8E8E8;
            margin-left: 20%;
        }
        .chat-message.bot {
            background-color: #FFFFFF;
            margin-right: 20%;
            border: 1px solid #E8E8E8;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 타이틀
    st.title("👞 반려1974 수선 상담")
    st.markdown("---")
    
    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "bot" not in st.session_state:
        st.session_state.bot = RepairChatbot()
    
    # 채팅 기록 표시
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="chat-message user">
                        <div>👤 고객님: {message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message bot">
                        <div>💬 {message["role"]}: {message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    # 빠른 버튼
    st.markdown("### 빠른 상담")
    col1, col2, col3, col4 = st.columns(4)
    
    def handle_quick_button(message):
        st.session_state.messages.append({"role": "user", "content": message})
        st.session_state.messages.append({"role": "MARU", "content": st.session_state.bot.get_response(message)})
        st.experimental_rerun()
    
    with col1:
        if st.button("👟 신발"):
            handle_quick_button("신발 수선 상담받고 싶어요")
    with col2:
        if st.button("👜 가방"):
            handle_quick_button("가방 수선 문의드려요")
    with col3:
        if st.button("👔 옷"):
            handle_quick_button("옷 수선 가능한가요")
    with col4:
        if st.button("💰 가격"):
            handle_quick_button("수선 가격이 궁금해요")
    
    # 사진 업로드
    st.markdown("### 📸 사진 업로드")
    uploaded_file = st.file_uploader("수선할 물건 사진을 선택하세요", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 사진", use_column_width=True)
        st.session_state.messages.append({"role": "user", "content": f"사진 업로드: {uploaded_file.name}"})
        st.session_state.messages.append({"role": "MARU", "content": "사진 잘 받았어요! 상태 확인해보니 수선 가능해 보이네요! 😊"})
        st.experimental_rerun()
    
    # 메시지 입력
    st.markdown("### 💬 메시지 입력")
    user_input = st.text_input("메시지를 입력하세요", key="user_input")
    if st.button("📤 전송") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "MARU", "content": st.session_state.bot.get_response(user_input)})
        st.experimental_rerun()

if __name__ == "__main__":
    main() 