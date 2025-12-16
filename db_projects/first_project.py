import psycopg2

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="password"
    )

def register_user(name, phone):
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

def main():
    print("📋 KULLANICI KAYIT SİSTEMİ")
    print("------------------------")

    name = input("👤 İsminizi girin: ")
    phone = input("📞 Telefon numaranızı girin: ")

    confirm = input("Kaydetmek istiyor musunuz? (E/H): ")

    if confirm.lower() == "e":
        register_user(name, phone)
    else:
        print("❌ Kayıt iptal edildi.")

if __name__ == "__main__":
    main()
