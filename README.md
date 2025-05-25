**Seberapa IF sih Kamu?**

**Deskripsi**

“Seberapa IF sih kamu?” adalah aplikasi kuis interaktif berbasis gestur kepala yang awalnya dikonsep sebagai filter TikTok untuk menguji pengetahuan dasar Informatika. Dikembangkan menggunakan Python, OpenCV, dan Pygame, setiap pengguna akan dihadapkan pada serangkaian soal pilihan ganda yang ditampilkan dan jawaban diberikan dengan menggeser kepala ke kiri (opsi A) atau kanan (opsi B). Aplikasi ini dilengkapi dengan logika penilaian, umpan balik visual dan suara setiap kali menjawab, serta sistem scoring yang menghitung dan menampilkan skor akhir setelah seluruh pertanyaan terjawab. Proyek ini dibuat sebagai tugas mata kuliah IF4021.

---

## Daftar Isi

* [Fitur](#fitur)
* [Struktur Direktori](#struktur-direktori)
* [Persyaratan](#persyaratan)
* [Cara Menjalankan](#cara-menjalankan)
* [Format Soal](#format-soal)
* [Penjelasan Modul](#penjelasan-modul)
* [Potensi Pengembangan](#potensi-pengembangan)
* [Progress](#progress)
* [Anggota Tim](#anggota-tim)

---

## Fitur

* Deteksi wajah dan pergerakan kepala (kiri/kanan) menggunakan Haar Cascade.
* Antarmuka kuis overlay di atas video live feed.
* Feedback visual (highlight frame) dan audio (beep/ping) untuk jawaban benar/salah.
* Cooldown 3 detik dan deteksi posisi netral sebelum menerima input berikutnya.
* JSON-driven bank soal, mudah diperluas.

---

## Struktur Direktori

```
seberapa-if-kamu/
├── __pycache__/                             # Cache bytecode Python
├── assets/                                  # Resource aplikasi
│   ├── haarcascade_frontalface_default.xml  # Model deteksi wajah
│   ├── soal.json                            # Bank soal (JSON)
│   ├── sound_beep.mp3                       # Suara jawaban salah
│   └── sound_ping.mp3                       # Suara jawaban benar
├── head_tracker.py                          # Modul pendeteksi arah kepala
├── quiz_logic.py                            # Logika kuis (soal, skor)
├── main.py                                  # Entry point aplikasi
├── requirements.txt                         # Daftar dependensi Python
└── RunFilter.command                        # Script shell (macOS/Linux)
```

---

## Persyaratan

* Python 3.10 atau lebih baru
* OpenCV
* Pygame
* Numpy

**Install dependensi**

```bash
pip install -r requirements.txt
```

---

## Cara Menjalankan

1. Pastikan kamera terhubung dan dapat diakses.
2. Jalankan:

   * **Windows**: buka terminal di folder proyek, jalankan `python main.py`
   * **macOS/Linux**: jalankan `./RunFilter.command` atau `bash RunFilter.command`
3. Ikuti instruksi di layar:

   * Arahkan muka ke tengah hingga netral, lalu geser kepala ke kiri/kanan untuk memilih jawaban.
   * Tekan `q` untuk keluar kapan saja.
4. Setelah sesi kuis selesai, skor akhir akan ditampilkan selama 5 detik.

---

## Format Soal

File soal disimpan di `assets/soal.json`, contoh format:

```json
[
  {
    "question": "Kepanjangan CPU?",
    "option_a": "Central Processing Unit",
    "option_b": "Central Process Unit",
    "answer": "A"
  }
]
```

Tambahkan atau sesuaikan entri sesuai kebutuhan.

---

## Penjelasan Modul

* **head\_tracker.py**: Memuat kelas `HeadTracker` untuk deteksi wajah dan perhitungan pergeseran `center_x` guna menentukan arah gerak kepala.
* **quiz\_logic.py**: Kelas `Quiz` menyimpan daftar soal, melacak indeks soal, dan skor.
* **main.py**: Menggabungkan deteksi wajah, logika kuis, dan UI—mengontrol alur kuis, menampilkan pertanyaan, memproses input gestur, serta menampilkan hasil.

---

## Potensi Pengembangan

* Ganti Haar Cascade dengan MediaPipe Face Mesh untuk akurasi lebih baik.
* Perluas format soal ke multiple options (A–D).
* Tambahkan statistik ke file CSV/SQLite (waktu respons, akurasi per soal).
* Paketkan aplikasi menjadi executable (PyInstaller) untuk distribusi mudah.

---

## Progress

* **2025-04-23**: Pembentukan tim, diskusi ide dan konsep.
* **2025-04-24**: Penentuan konsep, referensi, dan judul proyek.
* **2025-04-27**: Revisi konsep, setup GitHub, implementasi simulasi awal.
* **2025-05-01**: Pengembangan prototype aplikasi.
* **2025-05-02**: Pembaruan `README.md` dan dokumentasi progres.
* **2025-05-25**: Upload Prototype App ke Github Pribadi.

---

## Anggota Tim

* Elinca Savina (121140073)
* Hasna Dhiya Azizah (121140029)
* Dhian Adi Nugraha (121140055)

---