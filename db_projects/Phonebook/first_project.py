import psycopg2
import tkinter as tk
from tkinter import messagebox

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="ferdi7o92"
    )

def register_user(name, phone):

    if phone_exists(phone):
        print("⚠️ Bu telefon numarası zaten kayıtlı!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ KAYIT BAŞARILI!")


def phone_exists(phone):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM contacts WHERE phone = %s",
        (phone,))
    exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()
    return exists

def contact_exists(contact_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM contacts WHERE id = %s",
        (contact_id,))

    exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()
    return exists



def list_contacts():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, phone FROM contacts ORDER BY id;")
    rows = cursor.fetchall()

    if not rows:
        print("📭 Henüz kayıt yok.")
    else:
        print("\n📒 KAYITLI KİŞİLER")
        print("-----------------")
        for row in rows:
            print(f"🆔 {row[0]} | 👤 {row[1]} | 📞 {row[2]}")

    cursor.close()
    conn.close()

def delete_contact(contact_id):

    if not contact_exists(contact_id):
        print("❌ Böyle bir kayıt bulunamadı!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE id = %s",
        (contact_id,))

    conn.commit()
    cursor.close()
    conn.close()
    print("🗑️ Kayıt silindi!")

def update_contact(contact_id, new_name, new_phone):

    if not contact_exists(contact_id):
        print("❌ Böyle bir kayıt bulunamadı!")
        return

    # Telefon başka bir kayıtta var mı kontrol et
    if phone_exists(new_phone):
        print("⚠️ Bu telefon numarası başka bir kayıtta kullanılıyor!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE contacts
        SET name = %s, phone = %s
        WHERE id = %s
        """,
        (new_name, new_phone, contact_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    print("✏️ Kayıt güncellendi!")

def add_contact_gui():
    name = entry_name.get()
    phone = entry_phone.get()

    if not name or not phone:
        messagebox.showwarning("Uyarı", "İsim ve telefon boş olamaz!")
        return

    register_user(name, phone)
    refresh_list()
    clear_entries()


def delete_contact_gui():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Uyarı", "Silmek için bir kayıt seç!")
        return

    contact_id = listbox.get(selected[0]).split()[0]
    delete_contact(int(contact_id))
    refresh_list()

def update_contact_gui():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Uyarı", "Güncellemek için bir kayıt seç!")
        return

    contact_id = listbox.get(selected[0]).split()[0]
    name = entry_name.get()
    phone = entry_phone.get()

    if not name or not phone:
        messagebox.showwarning("Uyarı", "Yeni isim ve telefon gir!")
        return

    update_contact(int(contact_id), name, phone)
    refresh_list()

def on_select(event):
    selected = listbox.curselection()
    if not selected:
        return

    data = listbox.get(selected[0])
    parts = data.split("|")

    name = parts[1].strip()
    phone = parts[2].strip()

    entry_name.delete(0, tk.END)
    entry_name.insert(0, name)

    entry_phone.delete(0, tk.END)
    entry_phone.insert(0, phone)

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)



def refresh_list():
    listbox.delete(0, tk.END)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts ORDER BY id;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    for r in rows:
        listbox.insert(tk.END, f"{r[0]:<3} | {r[1]:<15} | {r[2]}")

def add_contact_gui():
    name = entry_name.get()
    phone = entry_phone.get()

    if not name or not phone:
        messagebox.showwarning("Uyarı", "İsim ve telefon boş olamaz!")
        return

    register_user(name, phone)
    refresh_list()

def delete_contact_gui():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Uyarı", "Silmek için bir kayıt seç!")
        return

    contact_id = listbox.get(selected[0]).split("|")[0].strip()
    delete_contact(int(contact_id))
    refresh_list()

def update_contact_gui():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Uyarı", "Güncellemek için bir kayıt seç!")
        return

    contact_id = listbox.get(selected[0]).split("|")[0].strip()
    name = entry_name.get()
    phone = entry_phone.get()

    if not name or not phone:
        messagebox.showwarning("Uyarı", "Yeni isim ve telefon gir!")
        return

    update_contact(int(contact_id), name, phone)
    refresh_list()

# ---------- Pencere ----------
root = tk.Tk()
root.title("📒 Telefon Rehberi")
root.geometry("500x450")
root.configure(bg="#f2f2f2")

# ---------- Üst Başlık ----------
title = tk.Label(root, text="Telefon Rehberi", font=("Arial", 18, "bold"), bg="#f2f2f2")
title.pack(pady=10)

# ---------- Form Alanı ----------
form_frame = tk.Frame(root, bg="#f2f2f2")
form_frame.pack(pady=5)

tk.Label(form_frame, text="İsim:", bg="#f2f2f2", font=("Arial", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_name = tk.Entry(form_frame, width=25, font=("Arial", 11))
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Telefon:", bg="#f2f2f2", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_phone = tk.Entry(form_frame, width=25, font=("Arial", 11))
entry_phone.grid(row=1, column=1, padx=5, pady=5)

# ---------- Butonlar ----------
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="➕ Ekle", width=12, bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold"), command=add_contact_gui).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="✏️ Güncelle", width=12, bg="#2196F3", fg="white",
          font=("Arial", 10, "bold"), command=update_contact_gui).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="🗑️ Sil", width=12, bg="#F44336", fg="white",
          font=("Arial", 10, "bold"), command=delete_contact_gui).grid(row=0, column=2, padx=5)

tk.Button(
    btn_frame,
    text="🧹 Temizle",
    width=12,
    bg="#9E9E9E",
    fg="white",
    font=("Arial", 10, "bold"),
    command=clear_entries
).grid(row=0, column=3, padx=5)


# ---------- Liste ----------
list_frame = tk.Frame(root)
list_frame.pack(pady=10)

listbox = tk.Listbox(list_frame, width=50, height=10, font=("Courier New", 10))
listbox.pack(side="left", fill="y")

scrollbar = tk.Scrollbar(list_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

listbox.bind("<<ListboxSelect>>", on_select)


# ---------- Yenile ----------
tk.Button(root, text="🔄 Yenile", width=15, command=refresh_list).pack(pady=5)

refresh_list()
root.mainloop()