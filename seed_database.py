#!/usr/bin/env python3
"""
Script para insertar datos semilla en la base de datos.
Uso: python seed_database.py [--clear] [--create]
"""

import argparse
import sys

from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.db.seed_data import clear_seed_data, create_seed_data


def main():
    parser = argparse.ArgumentParser(description="Database seeding script")
    parser.add_argument("--clear", action="store_true", help="Clear existing seed data")
    parser.add_argument("--create", action="store_true", help="Create new seed data")
    parser.add_argument(
        "--reset", action="store_true", help="Clear and recreate seed data"
    )

    args = parser.parse_args()

    # If no arguments provided, default to create
    if not any([args.clear, args.create, args.reset]):
        args.create = True

    db = SessionLocal()
    try:
        if args.clear or args.reset:
            print("🗑️  Clearing existing seed data...")
            clear_seed_data(db)
            print("✅ Seed data cleared successfully!")

        if args.create or args.reset:
            print("🌱 Creating new seed data...")
            create_seed_data(db)
            print("✅ Seed data created successfully!")

        print("\n🎉 Database seeding completed!")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
