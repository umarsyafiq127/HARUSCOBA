from flask import Flask, request, render_template_string
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)

def hapus_background(image_pil):
    try:
        # Mengonversi gambar ke bytes
        image_bytes = io.BytesIO()
        image_pil.save(image_bytes, format="PNG")
        # Proses hapus background dengan rembg
        output_bytes = remove(image_bytes.getvalue())
        # Mengonversi kembali ke objek PIL.Image
        output_image = Image.open(io.BytesIO(output_bytes))
        return output_image
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

# Template HTML sederhana untuk form upload dan tampilan gambar
template = '''
<!doctype html>
<html>
<head>
  <title>Hapus Background Gambar</title>
</head>
<body>
  <h1>Hapus Background Gambar</h1>
  <form method="POST" enctype="multipart/form-data">
    <input type="file" name="gambar" accept="image/*" required>
    <input type="submit" value="Upload dan Proses">
  </form>
  {% if original_img %}
  <h2>Gambar Asli</h2>
  <img src="data:image/png;base64,{{ original_img }}" alt="Gambar Asli" style="max-width: 500px;">
  {% endif %}
  {% if processed_img %}
  <h2>Gambar Tanpa Background</h2>
  <img src="data:image/png;base64,{{ processed_img }}" alt="Gambar Tanpa Background" style="max-width: 500px;">
  <br>
  <!-- Link download menggunakan atribut download -->
  <a href="data:image/png;base64,{{ processed_img }}" download="hasil.png">Download Gambar</a>
  {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    original_img_data = None
    processed_img_data = None
    if request.method == 'POST':
        if 'gambar' in request.files:
            file = request.files['gambar']
            if file:
                # Membuka file gambar sebagai objek PIL.Image
                image_pil = Image.open(file.stream)
                # Encode gambar asli ke base64 untuk ditampilkan di HTML
                buffered = io.BytesIO()
                image_pil.save(buffered, format="PNG")
                original_img_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                # Proses hapus background
                hasil_image = hapus_background(image_pil)
                if hasil_image:
                    buffered2 = io.BytesIO()
                    hasil_image.save(buffered2, format="PNG")
                    processed_img_data = base64.b64encode(buffered2.getvalue()).decode('utf-8')
    return render_template_string(template, original_img=original_img_data, processed_img=processed_img_data)

if __name__ == '__main__':
    app.run(debug=True)
