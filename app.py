import streamlit as st
from rembg import remove
from PIL import Image
import io

def hapus_background(image_pil):
    try:
        # Menghapus latar belakang
        image_bytes = io.BytesIO()
        image_pil.save(image_bytes, format="PNG")
        output_bytes = remove(image_bytes.getvalue())  # Proses hapus background
        
        # Konversi kembali ke objek PIL.Image
        output_image = Image.open(io.BytesIO(output_bytes))
        return output_image
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return None

# Antarmuka Streamlit
st.title("🖼️ Hapus Background Gambar")

uploaded_file = st.file_uploader("📤 Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image_pil = Image.open(uploaded_file)  # Membuka sebagai objek PIL.Image
    st.image(image_pil, caption="🖼️ Gambar Asli", use_column_width=True)

    # Proses hapus background
    hasil_image = hapus_background(image_pil)

    if hasil_image:
        st.image(hasil_image, caption="✅ Gambar Tanpa Background", use_column_width=True)
        
        # Menyimpan hasil ke buffer untuk diunduh
        hasil_io = io.BytesIO()
        hasil_image.save(hasil_io, format="PNG")
        hasil_io.seek(0)

        st.download_button(
            label="⬇️ Download Gambar",
            data=hasil_io,
            file_name="hasil.png",
            mime="image/png"
        )
