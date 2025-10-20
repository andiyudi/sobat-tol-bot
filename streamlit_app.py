import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Impor semua 'tools' yang telah kita buat
from tools import (
    get_toll_tariff,
    get_traffic_info,
    get_rest_area_info,
    get_emergency_number
)

# Muat environment variables (GOOGLE_API_KEY)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Konfigurasi Model ---

# 1. Definisikan persona dan instruksi utama
SYSTEM_PROMPT = """
Anda adalah "Sobat-Tol", asisten AI resmi layanan jalan tol Indonesia.
Persona Anda: Ramah, profesional, akurat, dan lugas.
Tugas Anda:
1. Jawab pertanyaan pengguna terkait tarif tol, lalu lintas, rest area, dan nomor darurat.
2. Gunakan "tools" (fungsi) yang tersedia untuk mendapatkan data terbaru.
3. JANGAN menjawab pertanyaan di luar topik jalan tol. Jika ditanya hal lain (misal: cuaca, resep, politik), jawab dengan sopan: "Maaf Sobat, saya hanya bisa membantu terkait informasi jalan tol."
4. Selalu panggil pengguna dengan sapaan "Sobat".
5. Berikan jawaban dalam Bahasa Indonesia yang baik dan benar.
"""

# 2. Daftarkan "Tools"
AVAILABLE_TOOLS = [
    get_toll_tariff,
    get_traffic_info,
    get_rest_area_info,
    get_emergency_number
]

# 3. Inisialisasi Model
# Kita lakukan ini sekali saja
@st.cache_resource
def get_model():
    print("Model di-load...")
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT,
        tools=AVAILABLE_TOOLS
    )
    return model

# --- Logika Utama Aplikasi Streamlit ---

# Set judul halaman
st.set_page_config(page_title="Sobat-Tol", page_icon="🛣️")
st.title("Sobat-Tol 🛣️")
st.caption("Asisten AI Jalan Tol Anda")

# KUNCI UTAMA: Menggunakan Session State
# Streamlit menjalankan ulang skrip setiap ada interaksi.
# Kita perlu menyimpan histori chat & sesi model di 'st.session_state'

# 1. Inisialisasi chat session jika belum ada
if "chat_session" not in st.session_state:
    print("Memulai chat session baru...")
    model = get_model()
    # Aktifkan 'automatic function calling'
    st.session_state.chat_session = model.start_chat(
        enable_automatic_function_calling=True
    )

# 2. Inisialisasi histori pesan jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Tampilkan pesan-pesan dari histori
for message in st.session_state.messages:
    # Tampilkan pesan dengan role (user/assistant) yang sesuai
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Tangani input dari pengguna
if prompt := st.chat_input("Tanya Sobat-Tol... (cth: Berapa tarif Jakarta-Semarang?)"):
    
    # a. Tampilkan pesan pengguna di UI
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # b. Tambahkan pesan pengguna ke histori
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # c. Kirim pesan ke Gemini & tampilkan 'loading'
    with st.spinner("Sobat-Tol sedang mencari jawaban..."):
        try:
            # Kirim prompt ke model.
            # 'automatic_function_calling' akan menangani pemanggilan 'tools'
            response = st.session_state.chat_session.send_message(prompt)
            
            # d. Tampilkan respons dari AI
            with st.chat_message("assistant"):
                st.markdown(response.text)
                
            # e. Tambahkan respons AI ke histori
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            # Tangani error
            st.error(f"Maaf Sobat, terjadi error: {e}")
            # Hapus pesan terakhir yg error agar bisa dicoba lagi
            st.session_state.messages.pop()