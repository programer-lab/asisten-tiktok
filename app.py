import streamlit as st
import google.generativeai as genai

# 1. Mengatur Tampilan Halaman Web
st.set_page_config(page_title="AI Script Generator", page_icon="🎬", layout="centered")

st.title("🧙‍♂️ AI Asisten TikTok & Reels")
st.write("Dapatkan script video pendek siap pakai dalam hitungan detik. Cukup masukkan topikmu!")

# Ambil API Key secara aman dari sistem Streamlit Cloud
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = None

# 2. Membuat Kolom Input untuk Pengguna
topik_user = st.text_input(
    label="Apa topik video yang ingin kamu buat?", 
    placeholder="Contoh: Tips jualan online shop untuk pemula"
)

# 3. Logika Tombol Ketika Diklik
if st.button("Buat Script Video! ✨", type="primary"):
    if not topik_user:
        st.warning("⚠️ Tolong isi topiknya dulu ya bro/sist!")
    elif not GEMINI_API_KEY:
        st.error("🛑 API Key Gemini belum dimasukkan di pengaturan Secrets Streamlit!")
    else:
        with st.spinner("Harap tunggu, AI lagi nulis script terbaik buat kamu... 🤖"):
            try:
                # Menggunakan library standar yang stabil di Streamlit Cloud
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                perintah_prompt = f"""
                Kamu adalah seorang Script Writer profesional untuk TikTok dan Instagram Reels. 
                Gaya bahasamu sangat santai, menggunakan bahasa gaul anak muda Jakarta (lu, gue, aja, bgt, dll), persuasif, dan kreatif.
                Tugas: Buatlah script video pendek berdurasi 30 detik berdasarkan topik ini: {topik_user}.
                Format Output harus rapi: JUDUL, HOOK (0-3d), ISI VIDEO (4-25d), CTA (26-30d), REKOMENDASI VISUAL.
                """
                
                response = model.generate_content(perintah_prompt)
                
                st.success("🔥 Selesai! Ini script video buat kamu:")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Waduh, ada gangguan koneksi ke AI: {e}")

st.caption("Dibuat dengan ❤️ menggunakan Python & Streamlit Cloud.")
