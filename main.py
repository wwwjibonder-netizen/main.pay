import sys
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import sqlite3
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
def your_original_python_code():
    # উদাহরণ হিসেবে একটি ডামি লুপ দেওয়া হলো, এখানে আপনার আসল কোডটি রিপ্লেস করুন
    print("====== স্টুডেন্ট ডাটাবেস সিস্টেম ======")
    print("১. নতুন স্টুডেন্ট যোগ করুন")
    print("২. সব স্টুডেন্টের তালিকা দেখুন")
    
    # আপনার কোডের input() গুলো ঠিক এভাবেই কাজ করবে
    choice = input("আপনার পছন্দ নির্বাচন করুন: ")
    print(f"আপনি নির্বাচন করেছেন: {choice}")
    # ========================================================

# অ্যান্ড্রয়েডে টেক্সট ইনপুট-আউটপুট দেখানোর জন্য টার্মিনাল উইন্ডো মেকানিজম
class AndroidTerminalWidget(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.readonly = True
        self.background_color = (0, 0, 0, 1) # কালো স্ক্রিন
        self.foreground_color = (1, 1, 1, 1) # সাদা টেক্সট
        self.font_name = "Roboto"
        self.font_size = "16sp"
        sys.stdout = self
        sys.stderr = self

    def write(self, string):
        self.text += string

    def flush(self):
        pass

class TerminalApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        
        # টার্মিনালের ব্ল্যাক স্ক্রিন ডিসপ্লে
        self.terminal = AndroidTerminalWidget()
        root.add_widget(self.terminal)
        
        # টাইপ করার জন্য নিচের ইনপুট বক্স
        self.input_box = TextInput(size_hint_y=None, height=50, multiline=False, hint_text="এখানে টাইপ করে এন্টার চাপুন...")
        self.input_box.bind(on_text_validate=self.on_enter)
        root.add_widget(self.input_box)
        
        # ব্যাকগ্রাউন্ড থ্রেডে আপনার আসল কোডটি রান করানো
        threading.Thread(target=your_original_python_code, daemon=True).start()
        
        return root

    def on_enter(self, instance):
        user_input = self.input_box.text
        print(user_input) # স্ক্রিনে ইনপুটটি দেখাবে
        self.input_box.text = ''
        # বিল্ট-ইন ইনপুট মেকানিজমে ডেটা পাঠানো
        sys.stdin.write(user_input + '\n')

if __name__ == '__main__':
    # অ্যান্ড্রয়েডের জন্য ইনপুট স্ট্রীম প্যাচ
    import io
    sys.stdin = io.StringIO()
    TerminalApp().run()
    
