import pyodbc
import streamlit as st

def get_connection():
    """SQL Server LibraryDB bağlantısı"""
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=LibraryDB;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        st.error(f"Veritabanı bağlantısı hatası: {e}")
        return None
