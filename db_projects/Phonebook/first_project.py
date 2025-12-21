import psycopg2
import tkinter as tk
from tkinter import messagebox

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="pass"
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

def refresh_list():
    listbox.delete(0, tk.END)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts ORDER BY id;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    for r in rows:
        listbox.insert(tk.END, f"{r[0]} {r[1]} - {r[2]}")

# ---------- Pencere ----------

root = tk.Tk()
root.title("📒 Telefon Rehberi")
root.geometry("450x400")

# ---------- Giriş Alanları ----------

tk.Label(root, text="İsim").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Telefon").pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

# ---------- Butonlar ----------

tk.Button(root, text="➕ Ekle", width=20, command=add_contact_gui).pack(pady=5)
tk.Button(root, text="✏️ Güncelle", width=20, command=update_contact_gui).pack(pady=5)
tk.Button(root, text="🗑️ Sil", width=20, command=delete_contact_gui).pack(pady=5)

# ---------- Liste ----------

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

tk.Button(root, text="🔄 Yenile", width=20, command=refresh_list).pack(pady=5)

refresh_list()

root.mainloop()




# def main():
#     while True:
#         print("\n📋 KULLANICI KAYIT SİSTEMİ")
#         print("------------------------")
#         print("1️⃣ Yeni kayıt ekle")
#         print("2️⃣ Kayıtları listele")
#         print("3️⃣ Kayıt sil")
#         print("4️⃣ Kayıt güncelle")
#         print("5️⃣ Çıkış")
#
#         choice = input("Seçiminiz: ")
#
#         if choice == "1":
#             name = input("👤 İsminizi girin: ")
#             phone = input("📞 Telefon numaranızı girin: ")
#             register_user(name, phone)
#
#         elif choice == "2":
#             list_contacts()
#
#         elif choice == "3":
#             list_contacts()
#             contact_id = input("🆔 Silinecek ID: ")
#
#             if contact_id.isdigit():
#                 delete_contact(int(contact_id))
#             else:
#                 print("❌ ID sadece sayı olabilir!")
#
#         elif choice == "4":
#             list_contacts()
#             contact_id = input("🆔 Güncellenecek ID: ")
#
#             if not contact_id.isdigit():
#                 print("❌ ID sadece sayı olabilir!")
#                 continue
#
#             new_name = input("👤 Yeni isim: ")
#             new_phone = input("📞 Yeni telefon: ")
#
#             update_contact(int(contact_id), new_name, new_phone)
#
#         elif choice == "5":
#             print("👋 Görüşürüz!")
#             break
#
#         else:
#             print("❌ Geçersiz seçim!")
#
#
# if __name__ == "__main__":
#     main()
