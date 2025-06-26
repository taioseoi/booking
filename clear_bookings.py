import sqlite3
from config import DATABASE

def clear_bookings():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM bookings")
    conn.commit()
    conn.close()
    print("Bookings cleared!")

if __name__ == "__main__":
    clear_bookings()