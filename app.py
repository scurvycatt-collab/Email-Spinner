import streamlit as st
import google.generativeai as genai

# Danh sách từ khóa dễ kích hoạt bộ lọc Spam (Spam Trigger Words)
SPAM_KEYWORDS = [
    "free", "guarantee", "100%", "$$$", "risk-free", "risk free", "act now", 
    "click here", "buy now", "no cost", "guaranteed ecpm", "boost revenue", 
    "100% fill rate", "zero risk", "best price", "cheap", "make money"
]

# 1. Cấu hình giao diện Web
st.title("🇺🇸 Hệ Thống Xào Nấu Email (Bản Tiếng Anh + Spam Checker)")
st.markdown("Nhập mẫu email gốc. Hệ thống sẽ xào nấu sang Tiếng Anh chuyên nghiệp và TỰ ĐỘNG QUÉT từ khóa dễ bị vào hòm Spam.")

# Nhập API Key ở thanh bên
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

# 2. Các ô nhập liệu
col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input("Tên khách hàng (VD: John)")
with col2:
    app_name = st.text_input("Tên App/Game (VD: Flappy Bird)")

base_emails = st.text_area(
    "Dán các mẫu email gốc vào đây (Tiếng Anh hay Việt đều được):", 
    height=200
)

# 3. Nút bấm và Xử lý AI
if st.button("Tạo bản Email Tiếng Anh 🚀"):
    if not api_key:
        st.warning("Vui lòng nhập API Key ở cột bên trái trước!")
    elif not base_emails:
        st.warning("Vui lòng nhập các mẫu email gốc!")
    else:
        genai.configure(api_key=api_key)
        
        try:
            valid_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if not valid_models:
                st.error("Lỗi: API Key của bạn không có quyền truy cập model nào!")
            else:
                best_model = valid_models[0].replace('models/', '')
                model = genai.GenerativeModel(best_model)
                
                prompt = f"""
                You are a B2B Business Development expert. 
                I will provide you with several source email templates. 
                Your task is to combine, spin, and rewrite them into a SINGLE, highly engaging cold email in ENGLISH.
                
                Strict Rules:
                1. Output MUST be in English.
                2. ONLY use the information, value propositions, and context provided in the source emails. DO NOT add any extra fluff, fake features, or unnecessary details.
                3. Personalize the email using these exact variables:
                   - Recipient Name: {customer_name}
                   - App/Game Name: {app_name}
                4. Output ONLY the final email text ready to be sent. No introductory remarks, no explanations.
                
                Source Emails to spin:
                \"\"\"{base_emails}\"\"\"
                """
                
                with st.spinner('Đang trộn, xào nấu và rà soát Spam...'):
                    response = model.generate_content(prompt)
                    final_email = response.text
                    
                    # --- TÍNH NĂNG MỚI: KIỂM TRA SPAM ---
                    detected_spam = []
                    for word in SPAM_KEYWORDS:
                        # Kiểm tra xem từ khóa có nằm trong email không (không phân biệt hoa thường)
                        if word.lower() in final_email.lower():
                            detected_spam.append(word)
                            
                    # Hiển thị kết quả kiểm tra
                    if detected_spam:
                        st.warning(f"⚠️ **CẢNH BÁO SPAM!** Phát hiện các cụm từ nhạy cảm, dễ bị Gmail tóm: **{', '.join(detected_spam)}**.\n\nBạn nên cân nhắc sửa hoặc xóa bớt để an toàn hơn.")
                    else:
                        st.success("✅ **TUYỆT VỜI!** Email sạch sẽ, không phát hiện từ khóa Spam nguy hiểm.")
                    
                    # Hiển thị kết quả cuối cùng
                    st.text_area("Kết quả:", final_email, height=250)
                    
        except Exception as e:
            st.error(f"Hệ thống báo lỗi từ Google: {e}")
