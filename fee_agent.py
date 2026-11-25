import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "sandbox.db"

def connect(db_path=DB_PATH):
    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    return db

def initialize(db_path=DB_PATH):
    db = connect(db_path)
    db.execute('''
        CREATE TABLE IF NOT EXISTS student (
            sid TEXT PRIMARY KEY,
            assessed_fee INTEGER NOT NULL CHECK (assessed_fee >= 0),
            registered_fee INTEGER NOT NULL DEFAULT 0 CHECK (registered_fee IN (0, 1))
        );
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS bank_transaction (
            ref TEXT PRIMARY KEY,
            sid TEXT,
            amount_pesewas INTEGER NOT NULL CHECK (amount_pesewas >= 0),
            currency TEXT NOT NULL,
            settlement_status TEXT NOT NULL DEFAULT 'PENDING' CHECK (registered_fee IN ('PENDING', 'SETTLED'))
        );
    ''')
    db.execute('''
            CREATE TABLE IF NOT EXISTS posted_payment (
                ref TEXT PRIMARY KEY,
                sid TEXT,
                amount_pesewas INTEGER NOT NULL CHECK (amount_pesewas >= 0),
                posted_at TEXT NOT NULL
            );
        ''')
    db.execute('''
                CREATE TABLE IF NOT EXISTS case (
                    case_id TEXT PRIMARY KEY,
                    ref TEXT,
                    sid TEXT,
                    state TEXT,
                    reason TEXT
                );
            ''')
    db.execute('''
                    CREATE TABLE IF NOT EXISTS audit (
                        audit_id TEXT PRIMARY KEY,
                        case_id TEXT,
                        step TEXT,
                        created_at TEXT NOT NULL
                    );
                ''')
    db.commit()
    db.close()

class BankLookupTool: 
    def lookup(self, db, ref):
        return db.execute('SELECT * FROM bank_transaction' \
        'where ref=?', (ref,)).fetchone()