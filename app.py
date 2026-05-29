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

# 🛑 PENGATURAN BISNIS (Kamu bisa ganti password-nya di sini sesuka hati)
PASSWORD_PREMIUM = "TiktokCuan2026" 

# Inisialisasi hitungan uji coba gratis di browser user
if "hitung_trial" not in st.session_state:
    st.session_state.hitung_trial = 0

status_berlangganan = False
sisa_trial = max(0, 3 - st.session_state.hitung_trial)

# 2. SISTEM CEK TRIAL ATAU PREMIUM
if sisa_trial > 0:
    st.info(f"🎁 Kamu memiliki **{sisa_trial} kali** uji coba gratis tersisa!")
    status_berlangganan = True
else:
    st.error("🛑 Batas uji coba gratis kamu sudah habis (Maksimal 3x)!")
    st.write("Silakan beli **Password Berlangganan** untuk akses tanpa batas. Hubungi Admin via WA: [08xxxxxxxxxx]")
    
    input_pass = st.text_input("🔑 Masukkan Password Berlangganan:", type="password")
    if input_pass == PASSWORD_PREMIUM:
        st.success("🎉 Password Benar! Akses Premium Terbuka ✨")
        status_berlangganan = True
    elif input_pass != "":
        st.error("❌ Password salah, bro! Silakan cek kembali atau hubungi admin.")

# 3. KOTAK INPUT UTAMA
topik_user = st.text_input(
    label="Apa topik video yang ingin kamu buat?", 
    placeholder="Contoh: Tips jualan online shop untuk pemula"
)

# 4. LOGIKA TOMBOL GENERATE AI
if st.button("Buat Script Video! ✨", type="primary"):
    if not status_berlangganan:
        st.error("🛑 Maaf, kamu tidak bisa membuat script. Silakan masukkan password langganan yang valid terlebih dahulu!")
    elif not topik_user:
        st.warning("⚠️ Tolong isi topiknya dulu ya bro/sist!")
    elif not GEMINI_API_KEY:
        st.error("🛑 API Key Gemini belum dimasukkan di pengaturan Secrets Streamlit!")
    else:
        # Jika berhasil jalan dan masih pakai kuota gratis, kurangi kuotanya
        if st.session_state.hitung_trial < 3:
            st.session_state.hitung_trial += 1
            
        with st.spinner("Harap tunggu, AI lagi nulis script terbaik buat kamu... 🤖"):
            try:
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
                st.rerun() # Refresh halaman biar kuota langsung terupdate di layar
                
            except Exception as e:
                st.error(f"Waduh, ada gangguan koneksi ke AI: {e}")

st.caption("Dibuat dengan ❤️ menggunakan Python & Streamlit Cloud.")
