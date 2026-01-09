# 📊 SmartStock AI: Dashboard Analisis & Prediksi Inventaris

**SmartStock AI** adalah solusi manajemen stok berbasis Data Science yang menggunakan algoritma **K-Means Clustering** untuk mengotomatisasi pengelompokan barang dan memprediksi kebutuhan stok di masa depan. Aplikasi ini membantu pemilik bisnis mengoptimalkan perputaran barang dan mengurangi risiko stok mati.

---

## 🖥️ Tampilan Dashboard

### 1. Ringkasan Performa (KPI Metrics)
Memberikan ringkasan cepat mengenai total item, volume barang masuk/keluar, serta skor kesehatan perputaran stok secara real-time.
![Ringkasan Metrik](image_28bcac.png)

### 2. Analisis Visual Lanjutan
Terdapat visualisasi interaktif untuk melihat prioritas pembelian dan distribusi stok berdasarkan kategori:
* **Top 10 Barang Prioritas:** Mengurutkan item yang paling mendesak untuk dibeli kembali berdasarkan analisis keluar-masuk barang.
* **Box Plot Distribusi:** Melihat persebaran sisa stok di setiap kategori untuk mendeteksi penumpukan barang (*overstock*).
![Visualisasi Lanjutan](image_28bcac.png)

### 3. Peta Distribusi Stok (Scatter Plot)
Memetakan hubungan antara **Barang Masuk** dan **Barang Keluar**. Ukuran titik mewakili besarnya rencana pembelian yang disarankan oleh sistem.



### 4. Strategi Rekomendasi AI
Sistem secara otomatis mengelompokkan barang ke dalam 3 kategori strategis menggunakan algoritma Machine Learning:
* 🔴 **C1 - Barang Cepat Habis:** Memerlukan restock segera karena perputarannya sangat cepat.
* 🟡 **C2 - Barang Kebutuhan Normal:** Perputaran stabil, pembelian dilakukan sesuai kebutuhan operasional.
* 🟢 **C3 - Barang Jarang Terpakai:** Risiko stok mati, disarankan untuk bundling atau promo.
![Rencana Strategis](image_28c068.png)

---

## 🚀 Fitur Unggulan
* **AI-Powered Segmentation:** Segmentasi barang otomatis menggunakan algoritma K-Means Clustering.
* **Dynamic Prediction:** Menghitung rencana pembelian secara otomatis dengan parameter *Buffer Stock* yang bisa disesuaikan.
* **Interactive Data Table:** Detail setiap item dapat dilihat pada tabel yang dapat difilter dan dicari.
* **Multi-Format Export:** Unduh laporan hasil analisis langsung ke format **Excel (.xlsx)** atau **PDF (.pdf)**.
* **Modern Dark UI:** Antarmuka dashboard yang bersih dan nyaman dipandang.

## 🛠️ Teknologi yang Digunakan
* **Python** - Bahasa pemrograman utama.
* **Streamlit** - Framework UI Dashboard.
* **Scikit-Learn** - Implementasi K-Means Clustering.
* **Plotly** - Grafik data interaktif.
* **Pandas** - Manipulasi dan analisis data.
* **FPDF & XlsxWriter** - Pembuatan dokumen laporan.

## 📦 Cara Instalasi
1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/UsernameAnda/SmartStock-AI.git](https://github.com/UsernameAnda/SmartStock-AI.git)
    cd SmartStock-AI
    ```

2.  **Instal Library:**
    ```bash
    pip install streamlit pandas scikit-learn plotly fpdf openpyxl xlsxwriter
    ```

3.  **Jalankan Aplikasi:**
    ```bash
    streamlit run app.py
    ```

--
