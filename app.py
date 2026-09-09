# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
import json

class AttendanceApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        
        # সার্ভার ইউআরএল (আপনার PythonAnywhere লিঙ্কটি এখানে দিন)
        self.server_url = "https://pythonanywhere.com"
        
        self.add_widget(Label(text="Employee Attendance System", font_size=24, size_hint_y=None, height=50))
        
        # ID ইনপুট ফিল্ড
        self.emp_id_input = TextInput(hint_text="Enter Employee ID or Scan QR", multiline=False, size_hint_y=None, height=50)
        self.add_widget(self.emp_id_input)
        
        # সাবমিট বাটন
        self.submit_btn = Button(text="Submit Attendance", size_hint_y=None, height=50, background_color=(0, 0.7, 0, 1))
        self.submit_btn.bind(on_press=self.send_attendance)
        self.add_widget(self.submit_btn)
        
        # রেজাল্ট দেখার লেবেল
        self.result_label = Label(text="Status: Waiting for input...", font_size=16)
        self.add_widget(self.result_label)

    def send_attendance(self, instance):
        emp_id = self.emp_id_input.text.strip()
        if not emp_id:
            self.result_label.text = "Error: Please enter an ID"
            return
            
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        params = json.dumps({'emp_id': emp_id})
        
        # সার্ভারে ডাটা পাঠানো হচ্ছে
        UrlRequest(
            self.server_url,
            req_body=params,
            req_headers=headers,
            on_success=self.on_success,
            on_failure=self.on_error,
            on_error=self.on_error
        )

    def on_success(self, request, result):
        self.result_label.text = f"Success: {result.get('message')}"
        self.emp_id_input.text = "" # ইনপুট ফিল্ড ক্লিয়ার করা

    def on_error(self, request, result):
        self.result_label.text = f"Failed to mark attendance. Check Server/ID."

class MainApp(App):
    def build(self):
        return AttendanceApp()

if __name__ == '__main__':
    MainApp().run()
