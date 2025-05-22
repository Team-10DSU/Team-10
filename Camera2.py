import time
import socket
import cv2
from ultralytics import YOLO
from twilio.rest import Client

# Retrieve the local IP address
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Twilio credentials
account_sid = 'AC44361a591a1c28a3cd1e8db09a4fc5c3'
auth_token = '342f0ea16bb3858d59bfa37e75ded807'
client = Client(account_sid, auth_token)

def send_twilio_notification(alert_msg):
    try:
        message = client.messages.create(
            body=alert_msg,
            from_='+16315055650',
            to='+919482195691'
        )
        print("SMS Notification sent, SID:", message.sid)
    except Exception as e:
        print("Error sending SMS:", str(e))

def make_twilio_call():
    try:
        twiml = '<Response><Say voice="alice">Threat detected. Please check the system.</Say></Response>'
        call = client.calls.create(
            twiml=twiml,
            to='+919482195691',
            from_='+16315055650'
        )
        print("Call initiated, SID:", call.sid)
    except Exception as e:
        print("Error initiating call:", str(e))

# Mapping from class index to threat message
threat_messages = {
    0: "Fire is detected",
    1: "Gun is detected",
    2: "Knife is detected"
}

# Load your YOLO model
model = YOLO(r'X:\Major Project\MP\Detection.pt')

# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

print("Press 'q' to quit.")

# Timestamp of the last notification sent (in seconds)
last_notification_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # Run detection with specified confidence and IoU thresholds
    results = model(frame, conf=0.7, iou=0.5)
    filtered_boxes = results[0].boxes

    # Annotate the frame with detections
    annotated_frame = results[0].plot()
    cv2.imshow("Detection", annotated_frame)

    # Collect unique threat messages for the current frame
    detected_threats = set()
    for i, box in enumerate(filtered_boxes):
        conf = box.conf.item()
        cls = int(box.cls.item())
        coordinates = box.xyxy.tolist()[0]
        print(f"Detection {i+1}: Class: {cls}, Confidence: {conf:.2f}, Coordinates: {coordinates}")
        if cls in threat_messages:
            detected_threats.add(threat_messages[cls])

    # Check for threats and notification cooldown
    current_time = time.time()
    if detected_threats and (current_time - last_notification_time >= 600):
        alert_msg = ", ".join(detected_threats)
        alert_msg_with_ip = f"{alert_msg}. IP Address: {ip_address}"
        print("Alert:", alert_msg_with_ip)
        print("Sending notification and initiating call...")
        send_twilio_notification(alert_msg_with_ip)
        make_twilio_call()
        last_notification_time = current_time

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()