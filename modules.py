import json
from datetime import datetime
from validations import phone_validator, email_validator, name_validator


class Contact:
    def __init__(self, first_name, last_name, phone_number, email, created_at=None, updated_at=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or self.created_at
    

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

    def update_contact(self, phone_number=None, email=None):
        if phone_number is not None:
            if not phone_validator(phone_number):
                raise ValueError("Invalid phone number.")
            self.phone_number = phone_number

        if email is not None:
            if not email_validator(email):
                raise ValueError("Invalid email address.")
            self.email = email
        
        self.updated_at = datetime.now().isoformat()

    

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


    @classmethod
    def from_dict(cls, data):
        obj = cls(data["first_name"], data["last_name"], data["phone_number"], data["email"])
        obj.created_at = data.get("created_at", datetime.now().isoformat())
        obj.updated_at = data.get("updated_at", obj.created_at)
        return obj
    

class PhoneBook:
    
    def __init__(self, file_path="contacts.json"):
        self.contacts = dict()
        self.file_path = file_path
        self.load_from_file()
    def add_contact(self, first_name, last_name, phone_number, email):
        full_name = f"{first_name} {last_name}"
        if full_name in self.contacts:
            raise ValueError("❌ Contact already exists!")
        
        if not phone_validator(phone_number):
            raise ValueError("❌ Invalid phone number!")
        
        if not name_validator(first_name):
            raise ValueError("❌ First name is not valid! Only alphabetic characters are allowed.")
        
        if not name_validator(last_name):
            raise ValueError("❌ Last name is not valid! Only alphabetic characters are allowed.")

        if not email_validator(email):
            raise ValueError("❌ Invalid email!")
        
        
        new_contact = Contact(first_name, last_name, phone_number, email)
        self.contacts[full_name] = new_contact
        self.save_to_file()
        print(f"✅ Contact '{full_name}' added successfully.")
        return True
    

    def edit_contact(self, first_name, last_name, new_phone=None, new_email=None):
        full_name = f"{first_name} {last_name}"
        contact = self.contacts.get(full_name)
        if not contact:
            raise ValueError(f"❌ {contact} not found!")
            
        
        if new_phone is None and new_email is None:
            raise ValueError("⚠️ No new phone or email provided. Nothing to update.")


        try:
            contact.update_contact(phone_number=new_phone, email=new_email)
        except ValueError as e:
            print(f"❌ {e}")
            return False
        
        self.save_to_file()
        print(f"✅ Contact '{full_name}' updated.")
        return True
    

    def delete_contact(self, first_name, last_name):
        full_name = f"{first_name} {last_name}"
        if full_name in self.contacts:
            del self.contacts[full_name]
            self.save_to_file()
            print(f"✅ Contact '{full_name}' deleted.")
            return True
        raise ValueError("❌ Contact not found!")
        
    
    def get_all_contacts(self):
        if not self.contacts:
            yield "📭 Phone book is empty."
            return
        for full_name, contact in self.contacts.items():
            yield f"{full_name} | 📞 {contact.phone_number} | 📧 {contact.email}"
    
    def get_contact_by_name(self, first_name, last_name):
        full_name = f"{first_name} {last_name}"
        if not full_name in self.contacts:
            raise Exception(f"{full_name} not found.")
        
        for contact in self.contacts.values():
            if contact.full_name == full_name:
                if contact.phone_number is None:
                    raise Exception(f"⚠️  {full_name}'s phone number is empty!")
                elif contact.email is None:
                    raise Exception(f"⚠️  {full_name}'s email is empty!")
                
                return contact.phone_number, contact.email

    def sort_contacts_by_name(self):
        self.contacts = dict(sorted(self.contacts.items(), key=lambda item: item[0].lower()))
        self.save_to_file()
        print("✅ Contact has been sorted")

    def save_to_file(self):
        data = {name: contact.to_dict() for name, contact in self.contacts.items()}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    
    def load_from_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for name, contact in data.items():
                    self.contacts[name] = Contact.from_dict(contact)
            print("📂 Contacts loaded from file.")
        except:
            print("⚠️ No saved contacts found; starting fresh.")