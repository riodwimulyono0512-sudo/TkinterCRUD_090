import tkinter as tk
from tkinter import messagebox
import sqlite3


# Membuat database SQLite
def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Membuat database dan tabel
create_db()


# Fungsi prediksi fakultas berdasarkan nilai tertinggi
def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Nilai Sama"


# Fungsi untuk submit dan menyimpan nilai
def submit_nilai():
    nama = entry_nama.get().strip()

    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())

    except ValueError:
        messagebox.showerror(
            "Error",
            "Nilai Biologi, Fisika, dan Inggris harus berupa angka!"
        )
        return

    if not nama:
        messagebox.showerror(
            "Error",
            "Nama siswa tidak boleh kosong!"
        )
        return

    # Menentukan hasil prediksi
    hasil_prediksi = prediksi_fakultas(bio, fis, ing)

    # Menyimpan data ke SQLite
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil_prediksi))

    conn.commit()
    conn.close()

    # Menampilkan hasil prediksi
    label_hasil.config(
        text=f"Hasil Prediksi Fakultas: {hasil_prediksi}"
    )

    messagebox.showinfo(
        "Berhasil",
        f"Data siswa berhasil disimpan!\n"
        f"Nama: {nama}\n"
        f"Prediksi Fakultas: {hasil_prediksi}"
    )

    # Mengosongkan input setelah submit
    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)


# Membuat windows aplikasi
root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas")
root.geometry("400x430")
root.resizable(False, False)


# Judul aplikasi
label_judul = tk.Label(
    root,
    text="Aplikasi Prediksi Fakultas",
    font=("Arial", 16, "bold")
)
label_judul.pack(pady=15)


# Input nama siswa
tk.Label(root, text="Nama Siswa").pack()
entry_nama = tk.Entry(root, width=30)
entry_nama.pack(pady=5)


# Input nilai Biologi
tk.Label(root, text="Nilai Biologi").pack()
entry_bio = tk.Entry(root, width=30)
entry_bio.pack(pady=5)


# Input nilai Fisika
tk.Label(root, text="Nilai Fisika").pack()
entry_fis = tk.Entry(root, width=30)
entry_fis.pack(pady=5)


# Input nilai Inggris
tk.Label(root, text="Nilai Inggris").pack()
entry_ing = tk.Entry(root, width=30)
entry_ing.pack(pady=5)


# Tombol submit nilai
button_submit = tk.Button(
    root,
    text="Submit Nilai",
    command=submit_nilai,
    bg="lightblue",
    width=20
)
button_submit.pack(pady=15)


# Label hasil prediksi
label_hasil = tk.Label(
    root,
    text="Hasil Prediksi Fakultas: -",
    font=("Arial", 10, "bold")
)
label_hasil.pack(pady=5)


# Menjalankan aplikasi
root.mainloop()