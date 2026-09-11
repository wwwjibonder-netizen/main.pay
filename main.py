
import flet as ft
import requests

# ⚠️ মনোযোগ দিন: নিচের লাইনে YOUR_SUBDOMAIN কেটে আপনার PythonAnywhere-এর লিঙ্কটি বসিয়ে দিন
SERVER_URL = "https://www.pythonanywhere.com/user/jibonder/" 

def main(page: ft.Page):
    page.title = "QR Attendance System"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    result_text = ft.Text(
        value="QR কোড স্ক্যান করুন অথবা নিচে আইডি লিখুন",
        size=16, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    emp_id_input = ft.TextField(
        label="Employee ID (ম্যানুয়াল ইনপুট)", 
        width=280, 
        text_align=ft.TextAlign.CENTER
    )

    # সার্ভারে ডেটা পাঠানোর মূল ফাংশন
    def send_attendance_request(emp_id):
        if not emp_id:
            result_text.value = "❌ অনুগ্রহ করে একটি সঠিক ID দিন!"
            result_text.color = "red"
            page.update()
            return

        result_text.value = "🔄 সার্ভারে অনুরোধ পাঠানো হচ্ছে..."
        result_text.color = "blue"
        page.update()

        try:
            response = requests.post(
                f"{SERVER_URL}/api/attendance", 
                json={"emp_id": str(emp_id).strip()}
            )
            data = response.json()

            if response.status_code == 200:
                if data.get("status") == "check_in":
                    result_text.value = f"✅ সফল Check-in!\n⏰ সময়: {data.get('time_in')}"
                else:
                    result_text.value = f"✅ সফল Check-out!\n⏱️ মোট সময়: {data.get('total_time')} ঘণ্টা\n🔥 ওভারটাইম: {data.get('overtime')} ঘণ্টা"
                result_text.color = "green"
                emp_id_input.value = "" 
            else:
                result_text.value = f"❌ ভুল: {data.get('error', 'অনুমোদিত নয়')}"
                result_text.color = "red"
        except Exception as ex:
            result_text.value = "❌ সার্ভারের সাথে যোগাযোগ করা যাচ্ছে না!"
            result_text.color = "red"
        
        page.update()

    # QR কোড স্ক্যান সফল হলে এই ফাংশনটি কাজ করবে
    def on_scan_success(e):
        scanned_id = e.data
        if scanned_id:
            emp_id_input.value = scanned_id
            send_attendance_request(scanned_id)

    # কিউআর কোড স্ক্যানার উইজেট
    qr_scanner = ft.QrCodeScanner(
        on_scan=on_scan_success,
        visible=True,
        width=300,
        height=300
    )

    def manual_submit(e):
        send_attendance_request(emp_id_input.value)

    submit_btn = ft.ElevatedButton(
        text="ম্যানুয়াল সাবমিট", 
        on_click=manual_submit
    )

    # অ্যাপের স্ক্রিন সাজানো
    page.add(
        ft.AppBar(
            title=ft.Text("Smart Attendance System", color="white"),
            bgcolor="blue",
            center_title=True
        ),
        ft.Container(height=20),
        ft.Text("ক্যামেরার সামনে QR কোডটি ধরুন", size=18, weight=ft.FontWeight.W_500),
        ft.Container(
            content=qr_scanner,
            border=ft.border.all(2, "blue"),
            border_radius=12,
            padding=10
        ),
        ft.Container(height=15),
        result_text,
        ft.Container(height=15),
        ft.Divider(height=1, color="grey"),
        ft.Container(height=15),
        emp_id_input,
        submit_btn
    )

ft.app(target=main)
