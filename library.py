import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from db_config import get_connection

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Kütüphane Yönetim Sistemi", layout="wide")

# --- CSS ---
st.markdown("""
<style>
.stButton>button {
    background-color: #3A7BD5;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
}
.stButton>button:hover {
    background-color: #3366cc;
}
.card {
    background: white;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
h2 {
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

# --- Dashboard ---
def dashboard(conn):
    st.title(" Kütüphane Yönetim Paneli")
    cursor = conn.cursor()

    # Kartlar
    col1, col2, col3 = st.columns(3)
    cursor.execute("SELECT COUNT(*) FROM Uyeler")
    uye_sayisi = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Kitaplar")
    kitap_sayisi = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Odunc")
    odunc_sayisi = cursor.fetchone()[0]

    col1.markdown(f"<div class='card'><h3>Üye Sayısı</h3><h2>{uye_sayisi}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><h3>Kitap Sayısı</h3><h2>{kitap_sayisi}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'><h3>Ödünç Sayısı</h3><h2>{odunc_sayisi}</h2></div>", unsafe_allow_html=True)

    # En çok ödünç alınan kitaplar
    cursor.execute("""
        SELECT K.Baslik, COUNT(O.OduncID) AS OduncSayisi
        FROM Kitaplar K
        LEFT JOIN Odunc O ON K.KitapID = O.KitapID
        GROUP BY K.KitapID, K.Baslik
        ORDER BY OduncSayisi DESC
    """)
    rows = cursor.fetchall()

    clean_rows = []
    for r in rows:
        if isinstance(r, tuple) and len(r) == 2:
            clean_rows.append(r)
        else:
            clean_rows.append((r[0], 0))

    if clean_rows:
        df = pd.DataFrame(clean_rows, columns=["Kitap", "Ödünç Sayısı"])
        fig = px.bar(df, x="Kitap", y="Ödünç Sayısı", title=" En Çok Ödünç Alınan Kitaplar")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(" Görüntülenecek ödünç kitap verisi bulunamadı.")

# --- Üye Ekle ---
def uye_ekle(conn):
    st.subheader(" Yeni Üye Ekle")
    ad = st.text_input("Ad")
    soyad = st.text_input("Soyad")
    email = st.text_input("Email")

    if st.button("Üyeyi Kaydet"):
        if ad and soyad and email:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Uyeler (Ad, Soyad, Email) VALUES (?, ?, ?)", (ad, soyad, email))
            conn.commit()
            st.success(f"{ad} {soyad} adlı üye başarıyla eklendi.")
        else:
            st.warning("Lütfen tüm alanları doldurun!")

# --- Kitap Ekle ---
def kitap_ekle(conn):
    st.subheader(" Yeni Kitap Ekle")
    baslik = st.text_input("Kitap Başlığı")
    yazar = st.text_input("Yazar")
    stok = st.number_input("Stok Sayısı", min_value=1, step=1)

    if st.button("Kitabı Kaydet"):
        if baslik and yazar and stok:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Kitaplar (Baslik, Yazar, Stok) VALUES (?, ?, ?)", (baslik, yazar, stok))
            conn.commit()
            st.success(f"{baslik} adlı kitap başarıyla eklendi.")
        else:
            st.warning("Lütfen tüm alanları doldurun!")

# --- Kitap Ödünç Al ---
def kitap_odunc_al(conn):
    st.subheader(" Kitap Ödünç Al")
    uye_id = st.number_input("Üye ID", min_value=1, step=1)
    kitap_id = st.number_input("Kitap ID", min_value=1, step=1)

    if st.button("Ödünç Al"):
        cursor = conn.cursor()
        cursor.execute("SELECT Stok FROM Kitaplar WHERE KitapID = ?", (kitap_id,))
        result = cursor.fetchone()

        if not result:
            st.error(" Kitap bulunamadı.")
            return

        stok = result[0]
        if stok > 0:
            cursor.execute("INSERT INTO Odunc (UyeID, KitapID, AlisTarihi) VALUES (?, ?, ?)",
                           (uye_id, kitap_id, datetime.now()))
            cursor.execute("UPDATE Kitaplar SET Stok = Stok - 1 WHERE KitapID = ?", (kitap_id,))
            conn.commit()
            st.success(" Kitap başarıyla ödünç alındı.")
        else:
            st.warning(" Stokta kitap kalmadı!")

# --- Ana Uygulama ---
def main():
    conn = get_connection()
    if not conn:
        st.error(" Veritabanına bağlanılamadı!")
        return

    st.sidebar.title(" Menü")
    menu = ["Dashboard", "Üye Ekle", "Kitap Ekle", "Kitap Ödünç Al"]
    secim = st.sidebar.selectbox("Bir sayfa seç:", menu)

    if secim == "Dashboard":
        dashboard(conn)
    elif secim == "Üye Ekle":
        uye_ekle(conn)
    elif secim == "Kitap Ekle":
        kitap_ekle(conn)
    elif secim == "Kitap Ödünç Al":
        kitap_odunc_al(conn)

    conn.close()

if __name__ == "__main__":
    main()
