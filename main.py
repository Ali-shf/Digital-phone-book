import os
from dotenv import load_dotenv
from modules import PhoneBook
from validations import phone_validator, email_validator, name_validator
from utils.email_utils import Send_message

load_dotenv()
SENDER_EMAIL = os.getenv("GMAIL_USER")
APP_PASSWORD = os.getenv("GMAIL_PASS")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_validated(prompt_msg, validator_func, error_msg, required=True):
    while True:
        value = input(prompt_msg).strip()
        if required and not value:
            print("⚠️ This field is required. Please enter a value.")
            continue
        if value and not validator_func(value):
            print(f"❌ {error_msg} Try again.")
            continue
        return value

def input_optional_validated(prompt_msg, validator_func, error_msg):
    """
    Prompt user for input that can be empty (skip) or validated if entered.
    Returns None if skipped (empty input).
    """
    while True:
        value = input(prompt_msg).strip()
        if value == "":
            return None  # User chose to skip
        if not validator_func(value):
            print(f"❌ {error_msg} Try again.")
            continue
        return value

def main():
    pb = PhoneBook()

    while True:
        clear_screen()
        print("\n 📱 Welcome to Digital Phone Book 📱")  
        print("1. List all contacts")
        print("2. Add new contact")
        print("3. Edit a contact")
        print("4. Delete a contact")
        print("5. Search for a contact")
        print("6. Sort contacts")
        print("7. delete all contacts")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        match choice:
            case "1": 
                print("\n📇 All Contacts:")
                for contact in pb.get_all_contacts():
                    print(contact)
                input("\nPress Enter to continue...")

            case "2":
                first_name = input_validated("Enter first name: ", name_validator, "Invalid first name! Only alphabetic characters allowed.")
                last_name = input_validated("Enter last name: ", name_validator, "Invalid last name! Only alphabetic characters allowed.")
                phone = input_validated("Enter phone number: ", phone_validator, "Invalid phone number!")
                email = input_validated("Enter email: ", email_validator, "Invalid email address!")
                try:
                    pb.add_contact(first_name, last_name, phone, email)
                    send_welcome_meg = Send_message(email, f"{first_name} {last_name}", SENDER_EMAIL, APP_PASSWORD)
                    send_welcome_meg.send()
                except Exception as e:
                    print(f" {e}")
                input("\nPress Enter to continue...")

            case "3":
                first_name = input("First name: ").strip()
                last_name = input("Last name: ").strip()
                
                full_name = f"{first_name} {last_name}"
                
                if first_name == "" or last_name == "":
                    print("No firstname or lastname provided.")
                    input("\nPress Enter to continue...")
                    continue

                elif full_name not in pb.contacts:
                    print(f"❌ {full_name} not found!")
                    input("\nPress Enter to continue...")
                    continue
                
                new_phone = input_optional_validated("New phone (leave empty to skip): ", phone_validator, "Invalid phone number!")
                new_email = input_optional_validated("New email (leave empty to skip): ", email_validator, "Invalid email address!")

                try:
                    pb.edit_contact(first_name, last_name, new_phone, new_email)
                    send_edit_meg = Send_message(new_email, f"{first_name} {last_name}", SENDER_EMAIL, APP_PASSWORD)
                    send_edit_meg.send(body=f"You've edited {first_name} {last_name} contact")
                except Exception as e:
                    print(f"{e}")
                input("\nPress Enter to continue...")
            
            case "4":
                first = input("First name: ").strip()
                last = input("Last name: ").strip()
                try:
                    pb.delete_contact(first, last)
                except Exception as e:
                    print(f"{e}")
                input("\nPress Enter to continue...")

            case "5":
                first_name = input("First name: ").strip()
                last_name = input("Last name: ").strip()
                try:
                    phone, email = pb.get_contact_by_name(first_name, last_name)
                    print(f"📞 Phone: {phone}, 📧 Email: {email}")
                except Exception as e:
                    print(f"{e}")
                input("\nPress Enter to continue...")

            case "6":
                pb.sort_contacts_by_name()
                input("\nPress Enter to continue...")

            case "7":
                pb.delete_all_contacts()
                input("\nPress Enter to continue...")

            case "8":
                print("👋 Exiting. Goodbye!")
                break

            case _:
                print(" Invalid option. Please choose a number from 1 to 7.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
