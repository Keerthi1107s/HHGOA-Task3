import cv2
import os
import numpy as np

# Model files
FACE_MODEL = "face_detection_yunet_2026may.onnx"
RECOGNITION_MODEL = "face_recognition_sface_2021dec.onnx"

# Check models exist
if not os.path.exists(FACE_MODEL):
    print("❌ Face detection model not found!")
    exit()

if not os.path.exists(RECOGNITION_MODEL):
    print("❌ Face recognition model not found!")
    exit()

# Get image
image_path = input("Enter the path of your image: ")

image = cv2.imread(image_path)

if image is None:
    print("❌ Could not open image.")
    exit()

# -----------------------------
# 1. DETECT FACE
# -----------------------------

detector = cv2.FaceDetectorYN.create(
    FACE_MODEL,
    "",
    (320, 320),
    0.6,
    0.3,
    5000
)

detector.setInputSize((image.shape[1], image.shape[0]))

_, faces = detector.detect(image)

if faces is None:
    print("❌ No face detected.")
    exit()

print(f"✅ Faces detected: {len(faces)}")

# -----------------------------
# 2. LOAD FACE RECOGNITION
# -----------------------------

recognizer = cv2.FaceRecognizerSF.create(
    RECOGNITION_MODEL,
    ""
)

# Take the first detected face
face = faces[0]

# Align and crop the face
aligned_face = recognizer.alignCrop(image, face)

# Create face encoding
face_feature = recognizer.feature(aligned_face)

print("✅ Face encoding created!")

# Show some of the numbers
print("🔢 Encoding shape:", face_feature.shape)
print("🔢 First 10 values:", face_feature[0][:10])

# -----------------------------
# 3. SAVE ENCODING
# -----------------------------

np.save("face_encoding.npy", face_feature)

print("💾 Face encoding saved as face_encoding.npy")

# -----------------------------
# 4. SHOW FACE
# -----------------------------

x, y, w, h = face[:4].astype(int)

cv2.rectangle(
    image,
    (x, y),
    (x + w, y + h),
    (0, 255, 0),
    2
)

cv2.putText(
    image,
    "Face + Encoding",
    (x, y - 10),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)

cv2.imwrite("face_encoded.jpg", image)

print("💾 Result saved as face_encoded.jpg")

print("✅ Face encoding step completed.")