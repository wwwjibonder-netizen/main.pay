import os
import cv2
import requests
from pyzbar.pyzbar import decode
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.button import Button

# আপনার PythonAnywhere এপিআই ইউআরএল (yourusername পরিবর্তন করুন)
SERVER_URL = "https://pythonanywhere.com"

class QRFaceScannerApp(App):
    def build(self):
        self.title = "QR & Face Attendance Scanner"
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # ১. ক্যামেরা ভিউ দেখানোর জন্য ইমেজ উইজেট
        self.image_view = Image()
        self.layout.add_widget(self.image_view)

        # ২. স্ট্যাটাস বা মেসেজ দেখানোর জন্য লেবেল
        self.status_label = Label(
            text="ক্যামেরা চালু হচ্ছে... কিউআর কোড বা ফেস সামনে ধরুন",
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        self.layout.add_widget(self.status_label)

        # ৩. ফেস ডিটেকশনের জন্য OpenCV-এর বিল্ট-ইন ক্লাসিফায়ার লোড করা
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcarcade_frontalface_default.xml')

        # ৪. মোবাইলের মেইন ক্যামেরা চালু করা (০ = ব্যাক ক্যামেরা, ১ = ফ্রন্ট ক্যামেরা)
        self.capture = cv2.VideoCapture(0)
        
        # একই আইডি বারবার সাথে সাথে স্ক্যান হওয়া রোধ করতে ভ্যারিয়েবল
        self.last_scanned_id = ""
        
        # প্রতি সেকেন্ডে ৩০ বার ক্যামেরা ফ্রেম আপডেট করার জন্য ক্লক শিডিউল
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

        return self.layout

    def update_frame(self, dt):
        success, frame = self.capture.read()
        if not success:
            self.status_label.text = "ক্যামেরা অ্যাক্সেস করা যাচ্ছে না!"
            return

        # ফ্রেমটি সোজা করার জন্য প্রয়োজনে ফ্লিপ করা (মোবাইলের ক্যামেরার জন্য)
        frame = cv2.flip(frame, 0)

        # --- ফেস ডিটেকশন (Face Detection) লজিক ---
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # ডিটেক্ট হওয়া ফেসের চারপাশে সবুজ রঙের বক্স আঁকা
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # --- কিউআর কোড স্ক্যান (QR Code Scanner) লজিক ---
        qr_codes = decode(frame)
        for code in qr_codes:
            emp_id = code.data.decode('utf-8')
            
            # কিউআর কোডের চারপাশে নীল রঙের বক্স আঁকা
            (x, y, w, h) = code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # নতুন কোনো আইডি স্ক্যান হলে সার্ভারে পাঠানো
            if emp_id != self.last_scanned_id:
                self.last_scanned_id = emp_id
                self.send_attendance_to_server(emp_id)

        # OpenCV ফ্রেমকে Kivy টেক্সচারে রূপান্তর করে স্ক্রিনে দেখানো
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image_view.texture = texture

    def send_attendance_to_server(self, emp_id):
        self.status_label.text = f"আইডি পাওয়া গেছে: {emp_id}। সার্ভারে পাঠানো হচ্ছে..."
        try:
            # PythonAnywhere এপিআই-তে পোস্ট রিকোয়েস্ট পাঠানো
            response = requests.post(SERVER_URL, json={"emp_id": emp_id}, timeout=5)
            res_data = response.json()
            
            if response.status_code == 200:
                if res_data.get("status") == "check_in":
                    self.status_label.text = f"✅ চেক-ইন সফল: {res_data.get('message')}"
                else:
                    self.status_label.text = f"✅ চেক-আউট সফল: {res_data.get('message')}"
            else:
                self.status_label.text = f"❌ এরর: {res_data.get('error', 'অজানা সমস্যা')}"
        except Exception as e:
            self.status_label.text = "❌ সার্ভারের সাথে কানেক্ট করা যাচ্ছে না!"
            print(f"Server Error: {e}")

    def on_stop(self):
        # অ্যাপ বন্ধ করার সময় ক্যামেরা রিলিজ করা
        self.capture.release()

if __name__ == '__main__':
    QRFaceScannerApp().run()
