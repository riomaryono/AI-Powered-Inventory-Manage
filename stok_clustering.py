import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import plotly.express as px
import io
from fpdf import FPDF

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="AI Smart Inventory Dashboard", layout="wide")

# CSS Kustom (Tetap mempertahankan desain kartu Anda)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    [data-testid="stMetricValue"] { color: #1f1f1f !important; }
    [data-testid="stMetricLabel"] { color: #5f6368 !important; }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .report-card {
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 15px;
        border-left: 10px solid;
        color: #1f1f1f;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk Membuat PDF
def generate_pdf(dataframe, summary_stats):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="LAPORAN ANALISIS STOK & RENCANA PEMBELIAN", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Ringkasan Statistik:", ln=True)
    pdf.set_font("Arial", '', 10)
    for key, value in summary_stats.items():
        pdf.cell(200, 8, txt=f"- {key}: {value}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(60, 10, "Nama Barang", 1)
    pdf.cell(30, 10, "Sisa Stok", 1)
    pdf.cell(30, 10, "Beli Baru", 1)
    pdf.cell(40, 10, "Kategori", 1)
    pdf.ln()
    
    pdf.set_font("Arial", '', 9)
    for i, row in dataframe.head(50).iterrows():
        pdf.cell(60, 10, str(row['Nama Barang'])[:30], 1)
        pdf.cell(30, 10, str(row['Sisa Stok']), 1)
        pdf.cell(30, 10, str(row['Rencana Beli']), 1)
        pdf.cell(40, 10, str(row['Kategori']), 1)
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

st.title("📊 Laporan Analisis & Prediksi Pembelian")

# 2. SIDEBAR
st.sidebar.header("📁 Menu Data")
uploaded_file = st.sidebar.file_uploader("Unggah File Excel", type=['xlsx', 'csv'])
buffer_stok = st.sidebar.slider("Buffer Stok (Cadangan) %", 0, 100, 20) / 100

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        
        if 'Sisa Stok' not in df.columns:
            df['Sisa Stok'] = df['Barang Masuk'] - df['Barang Keluar']
        
        df['Rencana Beli'] = (df['Barang Keluar'] * (1 + buffer_stok)) - df['Sisa Stok']
        df['Rencana Beli'] = df['Rencana Beli'].apply(lambda x: int(round(x)) if x > 0 else 0)

        # 3. PROSES AI K-MEANS
        X = df[['Barang Masuk', 'Barang Keluar']]
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['Cluster_ID'] = kmeans.fit_predict(X)
        
        centers = kmeans.cluster_centers_[:, 1]
        sorted_idx = np.argsort(centers)[::-1]
        
        label_map = {
            sorted_idx[0]: ('C1', 'Barang Cepat Habis', '#ffebee', '#c62828'), 
            sorted_idx[1]: ('C2', 'Barang Kebutuhan Normal', '#fff9c4', '#fbc02d'), 
            sorted_idx[2]: ('C3', 'Barang Jarang Terpakai', '#e8f5e9', '#2e7d32')
        }
        
        df['Cluster'] = df['Cluster_ID'].map(lambda x: label_map[x][0])
        df['Kategori'] = df['Cluster_ID'].map(lambda x: label_map[x][1])

        # 4. KPI METRICS
        m1, m2, m3, m4 = st.columns(4)
        total_items = len(df)
        total_masuk = df['Barang Masuk'].sum()
        total_keluar = df['Barang Keluar'].sum()
        health = (total_keluar / total_masuk) * 100
        
        m1.metric("Jenis Barang", f"{total_items} Item")
        m2.metric("Total Masuk", f"{total_masuk}")
        m3.metric("Total Keluar", f"{total_keluar}")
        m4.metric("Perputaran Stok", f"{round(health, 1)}%")

        stats_for_pdf = {
            "Total Jenis Barang": total_items,
            "Total Barang Masuk": total_masuk,
            "Total Barang Keluar": total_keluar,
            "Persentase Perputaran": f"{round(health, 1)}%"
        }

        st.divider()

        # 5. VISUALISASI GRAFIK BARU
        st.subheader("📈 Analisis Visual Lanjutan")
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            # Grafik 1: Top 10 Rencana Beli
            top_10_beli = df[df['Rencana Beli'] > 0].nlargest(10, 'Rencana Beli')
            fig_bar = px.bar(top_10_beli, x='Rencana Beli', y='Nama Barang', 
                             orientation='h', title="Top 10 Barang Prioritas Beli",
                             color='Rencana Beli', color_continuous_scale='Reds')
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_g2:
            # Grafik 2: Box Plot Distribusi Stok per Kategori
            fig_box = px.box(df, x="Kategori", y="Sisa Stok", color="Kategori",
                             title="Distribusi Sisa Stok per Kategori",
                             color_discrete_map={
                                 'Barang Cepat Habis': '#c62828', 
                                 'Barang Kebutuhan Normal': '#fbc02d', 
                                 'Barang Jarang Terpakai': '#2e7d32'
                             })
            st.plotly_chart(fig_box, use_container_width=True)

        # 6. GRAFIK SCATTER (UKURAN BESAR)
        st.subheader("📊 Peta Distribusi Stok (Masuk vs Keluar)")
        fig_scatter = px.scatter(df, x="Barang Masuk", y="Barang Keluar", 
                                 color="Kategori", size="Rencana Beli", 
                                 hover_name="Nama Barang",
                                 color_discrete_map={
                                     'Barang Cepat Habis': '#c62828', 
                                     'Barang Kebutuhan Normal': '#fbc02d', 
                                     'Barang Jarang Terpakai': '#2e7d32'
                                 },
                                 template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)

        # 7. RINGKASAN & DETAIL
        st.divider()
        col_list, col_recom = st.columns([1, 2])
        
        with col_list:
            st.subheader("Ringkasan Kelompok")
            summary = df.groupby(['Cluster', 'Kategori']).size().reset_index(name='Jumlah')
            st.table(summary)

        with col_recom:
            st.subheader("Rencana Strategis AI")
            rekom_text = {
                'C1': "Segera lakukan restock! Barang ini adalah penggerak utama toko.",
                'C2': "Stok stabil, lakukan pembelian sesuai kebutuhan operasional.",
                'C3': "Obral atau bundling barang ini agar tidak menjadi stok mati."
            }
            for i in sorted_idx:
                c_code, c_name, bg_color, text_color = label_map[i]
                st.markdown(f"""
                    <div class="report-card" style="background-color:{bg_color}; border-color:{text_color};">
                        <h4 style="color:{text_color}; margin:0;">{c_code} - {c_name}</h4>
                        <p style="margin:5px 0; font-size:0.9em;">{rekom_text[c_code]}</p>
                    </div>
                """, unsafe_allow_html=True)

        # 8. DATA TABEL
        with st.expander("Lihat Data Tabel Lengkap"):
            st.dataframe(df[['Nama Barang', 'Sisa Stok', 'Rencana Beli', 'Cluster']], use_container_width=True)

        # 9. DOWNLOAD
        st.sidebar.divider()
        st.sidebar.subheader("📥 Unduh Laporan")
        
        # Excel
        output_excel = io.BytesIO()
        with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Analisis')
        st.sidebar.download_button("📥 Excel (.xlsx)", output_excel.getvalue(), "Laporan_Stok.xlsx")

        # PDF
        pdf_bytes = generate_pdf(df, stats_for_pdf)
        st.sidebar.download_button("📄 PDF (.pdf)", pdf_bytes, "Laporan_AI_Stok.pdf")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Unggah file untuk melihat dashboard interaktif.")