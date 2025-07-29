from modules import PhoneBook
def main():
    pb = PhoneBook()

    # pb.add_contact("Marjan", "Hekmat", "09126134972", "Marjan@gmail.com")

    pb.edit_contact("Marjan", "Hekmat", new_phone="09127845789")  

if __name__ == "__main__":
    main()