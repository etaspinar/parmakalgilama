import cv2
import mediapipe as mp
import pyautogui
import time

# MediaPipe el tespit modelini yükle
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

start_time = time.time()
cap = cv2.VideoCapture(0) # Webcam'den görüntü alma

current_desktop = 1  # Başlangıcı birinci masaüstü olarak ayarlandı

#Webcamin başarıyla açılıp açılmadığını kontrol etme
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    results = hands.process(frame)  # El tespiti

    if results.multi_hand_landmarks:
        # İlk elin başparmağının ucu
        hand_landmarks = results.multi_hand_landmarks[0]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # İşaret parmağı ucu koordinatları
        x, y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])

        print("İşaret parmağı algılandı! Diğer masaüstüne geçiş yapılıyor.")
        
        # Masaüstü geçişini kontrol et
        if current_desktop == 1:
            pyautogui.hotkey("ctrl", "win", "right")
            current_desktop = 2
            print("İkinci masaüstüne gidiyorum.")

        # 1. masaüstüne dönmek için 5 saniye bekle
        time.sleep(5)
        
        # Tekrardan 1. masaüstüne dönme
        pyautogui.hotkey("ctrl","win","left")
        current_desktop=1
        print("Tekrar 1. Masaüstüne dönüyorum.")

    # Görüntüyü ekrana göster
    cv2.imshow('Parmak Algilama', frame)
    cv2.waitKey(1)
    if time.time() - start_time > 7:
        break

cap.release() #Webcam bağlantısını sonlandırma 
cv2.destroyAllWindows() #OpenCV penceresini kapatma
