price_database = {}
print("item list program")
print("****************")

# শুরুতে আইটেম যোগ করার অংশ
try:
    total_price = int(input("Total number of items to add: "))
except ValueError:
    print("ভুল ইনপুট! আইটেম সংখ্যা ০ ধরা হলো।")
    total_price = 0

for i in range(1, total_price + 1):
    print(f"\n {i} enter price inf")
    name = input("enter name input: ")
    try:
        price = int(input("enter price input: "))
        
        # ডিসকাউন্ট হিসাব করা
        if price > 500:
            discount = price * 0.10
            final_price = price - discount
            print(f"10% Discount Price: {final_price}")
            print("***********")
            # ডিকশনারিতে নামটিকে Key এবং দামটিকে Value হিসেবে সেভ করা হলো
            price_database[name] = final_price
        else:
            print(f"not discount Regular Price: {price}")
            print("**********")
            price_database[name] = price
    except ValueError:
        print("ভুল প্রাইস ইনপুট! এই আইটেমটি সেভ করা হয়নি।")

# মেইন মেন্যু লুপ
while True:
    print("\n1. exit")
    print("2. add")
    print("3. search by price")
    print("4. all list")
    print("5. delete price")
    
    choice = input("enter your choice: ")
    
    if choice == '1':
        print("enter choice exit")
        break
        
    elif choice == '2':
        print("\n--- enter add price ---")
        new_name = input("new item name: ")
        
        if new_name in price_database:
            print("This item already exists in the database!")
        else:
            try:
                new_price = int(input("enter item price: "))
                if new_price > 500:
                    new_price = new_price - (new_price * 0.10)
                    print(f"10% Discount Applied! Price: {new_price}")
                
                price_database[new_name] = new_price
                print(f"Added successfully: {new_name} -> {new_price} Tk")
            except ValueError:
                print("ভুল ইনপুট! প্রাইস অবশ্যই সংখ্যা হতে হবে।")
                
    elif choice == '3':
        try:
            search_price = int(input("enter search price: "))
            # দাম দিয়ে পণ্য খোঁজার লজিক
            found_items = [name for name, price in price_database.items() if price == search_price]
            
            if found_items:
                print("\nprice information available:")
                for item in found_items:
                    print(f"Product Name: {item} | Price: {search_price} Tk")
            else:
                print("\nnot price available")
        except ValueError:
            print("ভুল ইনপুট! খোঁজার জন্য সঠিক সংখ্যা লিখুন।")
            
    elif choice == '4':
        if not price_database:
            print("\ndatabase empty")
        else:
            print("\n--- Current Data List ---")
            for name, price in price_database.items():
                print(f"Product: {name} -> Price: {price} Tk")
                
    elif choice == '5':
        try:
            delete_price = int(input("delete price: "))
            
            # ডিকশনারির ভ্যালু বা দামের সাথে মিল আছে কিনা দেখা
            if delete_price in price_database.values():
                # যে যে পণ্যের দাম মিলে যাবে তাদের নাম খুঁজে বের করা
                keys_to_delete = [key for key, value in price_database.items() if value == delete_price]
                
                # ডিকশনারি থেকে মুছে ফেলা
                for key in keys_to_delete:
                    del price_database[key]
                    
                print(f"\nconfirm: {delete_price} successfully deleted.")
            else:
                print("no data available")
        except ValueError:
            print("ভুল ইনপুট! ডিলিট করার জন্য সঠিক সংখ্যা লিখুন (যেমন: cm বা অন্য টেক্সট নয়)।")
            
    else:
        print("\nInvalid Choice! Please select between 1-5.")

print("\nprogram closed")
    
