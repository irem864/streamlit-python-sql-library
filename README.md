# Streamlit Python SQL Library / Streamlit Python SQL Kütüphane Uygulaması

## Project Overview / Proje Hakkında
This is a Library Management System built with **Python**, **Streamlit**, and **SQLite**.  
It allows users to manage members, books, and borrowing, while providing an interactive dashboard.  

Bu proje, **Python**, **Streamlit** ve **SQLite** kullanılarak geliştirilmiş bir Kütüphane Yönetim Sistemi’dir.  
Kullanıcıların üyeleri, kitapları ve ödünç işlemlerini yönetmesine ve etkileşimli bir dashboard görüntülemesine olanak tanır.

---

## Features / Özellikler
- **Dashboard**: Overview of total members, books, and borrow statistics.  
  **Dashboard**: Toplam üye, kitap ve ödünç istatistiklerini gösterir.
- **Member Management**: Add new members easily.  
  **Üye Yönetimi**: Yeni üyeleri kolayca ekleyebilme.
- **Book Management**: Add new books and track their stock.  
  **Kitap Yönetimi**: Yeni kitap ekleme ve stok takibi.
- **Borrow Books**: Borrow books and automatically update stock.  
  **Kitap Ödünç Alma**: Kitap ödünç al ve stok otomatik güncelle.
- **Interactive Charts**: Plotly bar charts show most borrowed books.  
  **Etkileşimli Grafikler**: En çok ödünç alınan kitapları bar grafiği ile gösterir.

---

## Installation / Kurulum
1. Clone the repository / Repo’yu klonlayınız:
```bash
git clone https://github.com/irem864/streamlit-python-sql-library.git
cd streamlit-python-sql-library
Create a virtual environment and activate it / Sanal ortam oluşturun ve aktif edin:

bash Kodu kopyalayınız: python -m venv venv
venv\Scripts\activate   # Windows
Install dependencies / Bağımlılıkları yükle:

bash Kodu kopyalayınız:pip install -r requirements.txt

Run the app / Uygulamayı çalıştır:

bash Kodu kopyala : streamlit run library.py

Requirements / Gereksinimler
Python 3.8+

Streamlit

pandas

plotly

SQLite

Python 3.8+

Streamlit

pandas

plotly

SQLite
