#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#RUN FILE ONCE TO INITIALIZE THE DATABASE

from database import Database


def initialize_database():
    
    print("=" * 50)
    print("S.P.E.A.K Database Initialization")
    print("=" * 50)
    
    #GET DATABASE DETAILS FROM USER
    print("\nEnter your MySQL credentials:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    user = input("Username (default: root): ").strip() or "root"
    password = input("Password: (default: none) ").strip()
    database = input("Database name (default: speak_db): ").strip() or "speak_db"
    
    #CREATE DATABASE INSTANCE
    db = Database(host=host, user=user, password=password, database=database)
    
    #CREATE DATABASE
    print("\n[1/3] Creating database...")
    if not db.create_database():
        print("Failed to create database")
        return
    
    #CONNECT TO DATABASE
    print("[2/3] Connecting to database...")
    if not db.connect():
        print("Failed to connect to database")
        return
    
    #CREATE TABLES
    print("[3/3] Creating tables...")
    if not db.create_tables():
        print("Failed to create tables")
        db.close()
        return
    
    db.close()
    
    print("\n" + "=" * 50)
    print("Database initialized successfully!")
    print("=" * 50)
    print("\nYou can now run your application with main.py")
    print(f"\nDatabase Configuration:")
    print(f"  Host: {host}")
    print(f"  User: {user}")
    print(f"  Database: {database}")
    print("\nIMPORTANT: Update these credentials in config.py")


if __name__ == "__main__":
    initialize_database()