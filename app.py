import os
import io
import base64
from flask import Flask, request, render_template_string
from rembg import remove
from PIL import Image

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="id">
  <head>
    <meta charset="utf-8">
    <title>Hapus Background Gambar</title>
  </head>
  <body>
    <h1>Upload Gambar untuk Menghapus Background</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/png, image/jpeg">
      <input type="submit" value="Proses">
    </form>
    {% if image_url %}
      <h2>Hasil Gambar Tanpa Background</h2>
      <img src="{{ image_url }}" alt="Gambar Hasil" style="max-width:500px;"><br>
      <a href="{{ image_url }}" download="hasil.png">⬇️ Download Gambar</a>
    {% endif %}
  </body>
</html>
"""

def hapus_background(image_pil):
    try:
        # Simpan gambar ke buffer bytes dengan format PNG
        image_bytes = io.BytesIO()
        image_pil.save(image_bytes, format="PNG")
        # Proses penghapusan background dengan rembg
        output_bytes = remove(image_bytes.getvalue())
        # Buka kembali hasilnya sebagai objek PIL.Image
        output_image = Image.open(io.BytesIO(output_bytes))
        return output_image
    except Exception as e:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    if request.method == "POST":
        if "file" not in request.files:
            return "File tidak ditemukan!"
        file = request.files["file"]
        if file.filename == "":
            return "Tidak ada file yang dipilih!"
        try:
            image_pil = Image.open(file.stream)
        except Exception as e:
            return f"Error membuka gambar: {e}"
        
        hasil_image = hapus_background(image_pil)
        if hasil_image is None:
            return "Terjadi kesalahan saat menghapus background!"
        
        # Simpan hasil gambar ke buffer untuk encoding base64
        hasil_io = io.BytesIO()
        hasil_image.save(hasil_io, format="PNG")
        hasil_io.seek(0)
        encoded_image = base64.b64encode(hasil_io.getvalue()).decode("utf-8")
        image_url = f"data:image/png;base64,{encoded_image}"
        
    return render_template_string(HTML_TEMPLATE, image_url=image_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
