import streamlit as st
import datetime
import random
from PIL import Image
import io

class Repair1974WebBot:
    def __init__(self):
        self.name = "MARU"
        self.shop_name = "반려1974"
        
        # 수선 카테고리별 응답
        self.repair_responses = {
            "신발": [
                "신발 수선이시군요! 어떤 부분이 문제인가요? 사진도 함께 보내주시면 더 정확한 상담 가능해요! 👟",
                "신발 수선 전문이에요! 사진 업로드하시면 상태 확인 후 정확한 견적 드릴게요!",
                "신발 어디가 불편하신가요? 📸 사진으로 올려주세요!"
            ],
            "구두": [
                "구두 수선이시네요! 굽 교체, 밑창 수리 등 가능해요! 사진으로 상태 확인해드릴게요 👠",
                "구두는 저희 전문 분야예요! 사진 올려주시면 정확한 상담 도와드릴게요!"
            ],
            "운동화": [
                "운동화 수선도 맡겨주세요! 📸 사진 업로드하시면 손상 부위 정확히 확인해드려요!",
                "브랜드 운동화도 원래 모양 그대로 복구해드려요! 사진 보내주세요!"
            ],
            "가방": [
                "가방 수선이시군요! 지퍼, 손잡이 등 어떤 부분인가요? 사진으로 확인해드릴게요! 👜",
                "명품 가방도 전문적으로 수선해드려요! 사진 업로드 부탁드려요!"
            ]
        }
        
        # 브랜드별 응답
        self.brand_responses = {
            "루이비통": "루이비통은 정말 섬세하게 작업해야 해요! 사진으로 상태 확인 후 전문 기술로 복구해드려요",
            "샤넬": "샤넬 제품은 고급 소재라 특별한 기법이 필요해요! 사진 보내주세요",
            "나이키": "나이키 운동화 수선 전문이에요! 사진으로 모델과 손상 부위 확인해드릴게요",
            "아디다스": "아디다스도 완벽하게 복구해드려요! 📸 사진 업로드해주세요"
        }

    def get_response(self, user_input):
        """사용자 입력에 대한 응답 생성"""
        user_input = user_input.lower().strip()
        
        # 브랜드 인식
        for brand, response in self.brand_responses.items():
            if brand.lower() in user_input:
                return f"{response} 어떤 부분 수선이 필요하신가요?"
        
        # 수선 카테고리 인식
        for category, responses in self.repair_responses.items():
            if category in user_input:
                return random.choice(responses)
        
        # 인사 응답
        if any(word in user_input for word in ["안녕", "하이", "hello"]):
            return f"안녕하세요! {self.shop_name} {self.name}입니다! 📸 사진 업로드로 정확한 상담 받으세요!"
        
        # 기본 응답
        default_responses = [
            "어떤 수선이 필요하신지 자세히 알려주세요! 📸 사진도 함께 올려주시면 더 정확해요!",
            f"{self.shop_name}는 사진 상담으로 정확한 견적을 드려요! 뭐가 문제인가요?",
            "구체적으로 어떤 물건인지 말씀해주시고, 📸 사진도 업로드해주세요!"
        ]
        
        return random.choice(default_responses)

def main():
    st.set_page_config(
        page_title="반려1974 수선 상담",
        page_icon="🛠️",
        layout="wide"
    )
    
    # CSS 스타일
    st.markdown("""
        <style>
        .stApp {
            max-width: 800px;
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
        .stButton>button {
            width: 100%;
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'bot' not in st.session_state:
        st.session_state.bot = Repair1974WebBot()
    
    # 헤더
    st.title("🛠️ 반려1974 수선 전문 상담")
    st.markdown("---")
    
    # 채팅 기록 표시
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                    <div style="
                        background-color: #E8E8E8;
                        padding: 1.5rem;
                        border-radius: 0.5rem;
                        margin-bottom: 1rem;
                        margin-left: 20%;
                    ">
                        <div>👤 고객님: {message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="
                        background-color: #FFFFFF;
                        padding: 1.5rem;
                        border-radius: 0.5rem;
                        margin-bottom: 1rem;
                        margin-right: 20%;
                        border: 1px solid #E8E8E8;
                    ">
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
    
    # 하단 정보
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            📸 사진 상담으로 정확한 견적 | 📞 매장 방문 상담 | 영업시간: 09:00-19:00
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 