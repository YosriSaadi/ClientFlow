import os
import sqlite3


def get_connection():
    return sqlite3.connect(DB_NAME)


APP_NAME = "ClientFlow"

def get_db_path():
    appdata = os.getenv("APPDATA")
    if not appdata:
        raise RuntimeError("APPDATA environment variable not found")

    app_dir = os.path.join(appdata, APP_NAME)
    os.makedirs(app_dir, exist_ok=True)  # 🔥 THIS LINE FIXES IT

    return os.path.join(app_dir, "app.db")

DB_NAME = get_db_path()

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        telephone TEXT,
        adresse TEXT,
        email TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ventes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        date TEXT,
        reference TEXT,
        montant_total REAL,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS paiements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vente_id INTEGER,
        date TEXT,
        montant REAL,
        mode TEXT,
        note TEXT,
        FOREIGN KEY(vente_id) REFERENCES ventes(id)
    )
    """)

    # Add new columns if not exist
    try:
        c.execute("ALTER TABLE clients ADD COLUMN adresse TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    try:
        c.execute("ALTER TABLE clients ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE ventes ADD COLUMN description TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()
    conn.close()




def reset_db():
    """Reset the database by dropping all tables and recreating them"""
    conn = get_connection()
    c = conn.cursor()

    # Drop all tables
    c.execute("DROP TABLE IF EXISTS paiements")
    c.execute("DROP TABLE IF EXISTS ventes")
    c.execute("DROP TABLE IF EXISTS clients")

    conn.commit()
    conn.close()

    # Reinitialize the database
    init_db()
    create_indexes()
    print("Database reset successfully.")


def create_indexes():
    conn = get_connection()
    c = conn.cursor()

    # Recherche rapide par nom
    c.execute("CREATE INDEX IF NOT EXISTS idx_clients_nom ON clients(nom)")

    # Recherche rapide par email
    c.execute("CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email)")

    # Recherche rapide par téléphone si besoin
    c.execute("CREATE INDEX IF NOT EXISTS idx_clients_telephone ON clients(telephone)")

    # Pour les ventes liées à un client
    c.execute("CREATE INDEX IF NOT EXISTS idx_ventes_client_id ON ventes(client_id)")

    # Pour les paiements liés à une vente
    c.execute("CREATE INDEX IF NOT EXISTS idx_paiements_vente_id ON paiements(vente_id)")

    conn.commit()
    conn.close()
    print("Indexes created successfully.")





