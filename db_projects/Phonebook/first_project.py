import psycopg2

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
        (name, phone)
    )

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ KAYIT BAŞARILI!")


def phone_exists(phone):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM contacts WHERE phone = %s",
        (phone,)
    )

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



def main():
    while True:
        print("\n📋 KULLANICI KAYIT SİSTEMİ")
        print("------------------------")
        print("1️⃣ Yeni kayıt ekle")
        print("2️⃣ Kayıtları listele")
        print("3️⃣ Çıkış")

        choice = input("Seçiminiz: ")

        if choice == "1":
            name = input("👤 İsminizi girin: ")
            phone = input("📞 Telefon numaranızı girin: ")
            register_user(name, phone)

        elif choice == "2":
            list_contacts()

        elif choice == "3":
            print("👋 Görüşürüz!")
            break

        else:
            print("❌ Geçersiz seçim!")


if __name__ == "__main__":
    main()
