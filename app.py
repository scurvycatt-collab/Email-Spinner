import streamlit as st
import google.generativeai as genai

# 1. Cấu hình giao diện Web
st.title("🇺🇸 Hệ Thống Xào Nấu Email (Bản Tiếng Anh)")
st.markdown("Nhập nhiều mẫu email đầu vào. Hệ thống sẽ trộn, xào nấu và viết lại thành MỘT bản tiếng Anh duy nhất, bám sát 100% ý gốc, không thêm thắt rườm rà.")

# Nhập API Key ở thanh bên
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

# 2. Các ô nhập liệu
col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input("Tên khách hàng (VD: John)")
with col2:
    app_name = st.text_input("Tên App/Game (VD: Flappy Bird)")

# Ô nhập liệu lớn để dán nhiều mẫu mail
base_emails = st.text_area(
    "Dán các mẫu email gốc vào đây (Tiếng Anh hay Việt đều được, enter xuống dòng để phân cách các mẫu):", 
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
                
                # --- PROMPT MỚI: ÉP TIẾNG ANH & CẤM THÊM THẮT ---
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
                4. Output ONLY the final email text ready to be sent. No introductory remarks, no explanations, no placeholders.
                
                Source Emails to spin:
                \"\"\"{base_emails}\"\"\"
                """
                
                with st.spinner('Đang trộn và viết lại bằng Tiếng Anh...'):
                    response = model.generate_content(prompt)
                    
                    st.success("Thành công! Copy email bên dưới để gửi nhé:")
                    # Dùng text_area để dễ dàng bôi đen copy
                    st.text_area("Kết quả:", response.text, height=250)
                    
        except Exception as e:
            st.error(f"Hệ thống báo lỗi từ Google: {e}")