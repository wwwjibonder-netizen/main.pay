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

# আপনার PythonAnywhere এপিআই ইউআরএল (yourusername পরিবর্তন করুন)
SERVER_URL = "jibonder"

class QRFaceScannerApp(App):
    def build(self):
        self.title = "QR & Face Attendance Scanner"
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.image_view = Image()
        self.layout.add_widget(self.image_view)

        self.status_label = Label(
            text="ক্যামেরা চালু হচ্ছে... কিউআর কোড বা ফেস সামনে ধরুন",
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        self.layout.add_widget(self.status_label)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.capture = cv2.VideoCapture(0)
        self.last_scanned_id = ""
        
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
        return self.layout

    def update_frame(self, dt):
        success, frame = self.capture.read()
        if not success:
            self.status_label.text = "ক্যামেরা অ্যাক্সেস করা যাচ্ছে না!"
            return

        frame = cv2.flip(frame, 0)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        qr_codes = decode(frame)
        for code in qr_codes:
            emp_id = code.data.decode('utf-8')
            (x, y, w, h) = code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if emp_id != self.last_scanned_id:
                self.last_scanned_id = emp_id
                self.send_attendance_to_server(emp_id)

        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image_view.texture = texture

    def send_attendance_to_server(self, emp_id):
        self.status_label.text = f"আইডি পাওয়া গেছে: {emp_id}। সার্ভারে পাঠানো হচ্ছে..."
        try:
            response = requests.post(SERVER_URL, json={"emp_id": emp_id}, timeout=5)
            res_data = response.json()
            if response.status_code == 200:
                self.status_label.text = f"✅ সফল: {res_data.get('message')}"
            else:
                self.status_label.text = f"❌ এরর: {res_data.get('error', 'অজানা সমস্যা')}"
        except Exception as e:
            self.status_label.text = "❌ সার্ভারের সাথে কানেক্ট করা যাচ্ছে না!"

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    QRFaceScannerApp().run()
