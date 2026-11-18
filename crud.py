from datetime import datetime
import json
import os

DATA_FILE = "freelance_records.json"


# --- Validation & Storage Helpers ---
def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: JSON file is empty or corrupted. Starting with empty data.")
            return {}
    return {}


def save_data(directory):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(directory, f, indent=4)


# 1. CREATE
def create(directory):
    client_id = input("Enter Client ID (e.g., C101): ").strip().upper()
    if not client_id:
        print("Error: Client ID cannot be empty.")
        return
    if client_id in directory:
        print(f"Error: Client ID '{client_id}' already exists.")
        return

    name = input("Enter Client Name: ").strip()
    project = input("Enter Project Title: ").strip()
    if not name or not project:
        print("Error: Client Name and Project Title are required.")
        return

    deadline = input("Enter Deadline (YYYY-MM-DD): ").strip()
    if not is_valid_date(deadline):
        print("Error: Invalid date format. Use YYYY-MM-DD (e.g., 2026-12-10).")
        return

    try:
        budget = float(input("Enter Project Budget (INR): ").strip())
    except ValueError:
        print("Error: Budget must be a valid number.")
        return

    status = input("Enter Status [Pending / In Progress / Paid]: ").strip() or "Pending"

    directory[client_id] = {
        "name": name,
        "project": project,
        "deadline": deadline,
        "budget": budget,
        "status": status,
    }
    save_data(directory)
    print(f"Success: Record '{client_id}' created and saved.")


# 2. READ (All or Single Record)
def read(directory):
    if not directory:
        print("Directory is empty. No records found.")
        return

    filter_id = input("Enter Client ID to search (or press Enter to view all): ").strip().upper()
    if filter_id:
        if filter_id not in directory:
            print(f"Error: Client ID '{filter_id}' not found.")
            return
        records = {filter_id: directory[filter_id]}
    else:
        records = directory

    print("\n" + "=" * 86)
    print(f"{'ID':<8} | {'Client Name':<18} | {'Project':<20} | {'Deadline':<10} | {'Budget':<10} | {'Status'}")
    print("-" * 86)
    for cid, data in records.items():
        print(
            f"{cid:<8} | {data['name']:<18} | {data['project']:<20} | "
            f"{data['deadline']:<10} | {data['budget']:<10.2f} | {data['status']}"
        )
    print("=" * 86)


# 3. UPDATE
def update(directory):
    client_id = input("Enter Client ID to update: ").strip().upper()
    if client_id not in directory:
        print(f"Error: Client ID '{client_id}' not found.")
        return

    current = directory[client_id]
    print("Press Enter to keep the existing value.")

    new_project = input(f"Project [{current['project']}]: ").strip()
    new_deadline = input(f"Deadline [{current['deadline']}]: ").strip()
    new_budget = input(f"Budget [{current['budget']}]: ").strip()
    new_status = input(f"Status [{current['status']}]: ").strip()

    if new_project:
        current["project"] = new_project
    if new_deadline:
        if not is_valid_date(new_deadline):
            print("Error: Invalid date format. Update aborted.")
            return
        current["deadline"] = new_deadline
    if new_budget:
        try:
            current["budget"] = float(new_budget)
        except ValueError:
            print("Error: Invalid budget entered. Update aborted.")
            return
    if new_status:
        current["status"] = new_status

    save_data(directory)
    print(f"Success: Record '{client_id}' updated.")


# 4. DELETE
def delete(directory):
    client_id = input("Enter Client ID to delete: ").strip().upper()
    if client_id not in directory:
        print(f"Error: Client ID '{client_id}' not found.")
        return

    confirm = input(f"Are you sure you want to delete '{client_id}' ({directory[client_id]['name']})? (y/n): ").strip().lower()
    if confirm == "y":
        directory.pop(client_id)
        save_data(directory)
        print(f"Success: Record '{client_id}' deleted.")
    else:
        print("Deletion cancelled.")


# --- Main Application Loop ---
def main():
    directory = load_data()
    while True:
        print("\n--- Freelance Client & Project Directory ---")
        print("1. Create Record")
        print("2. Read Records")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            create(directory)
        elif choice == "2":
            read(directory)
        elif choice == "3":
            update(directory)
        elif choice == "4":
            delete(directory)
        elif choice == "5":
            print("All changes saved to freelance_records.json. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()