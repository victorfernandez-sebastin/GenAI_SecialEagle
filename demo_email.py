import pyautogui
import time
import webbrowser

# Global pause between commands
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True  # Move mouse to top-left to stop script

# Step 1: Open Gmail in the browser
webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
time.sleep(5)  # Wait for Gmail to load

# Step 2: Click the Compose button (replace x, y with your actual coordinates)
pyautogui.click(x=142, y=254)  # <-- Update this to your Compose button
time.sleep(2)

# Step 3: Type recipient email
pyautogui.write('receiver@example.com')
pyautogui.press('tab')  # Navigate to subject
pyautogui.press('tab')  # Navigate to subject

# Step 4: Type subject
pyautogui.write('Test Email from Python RPA')
pyautogui.press('tab')  # Navigate to body

# Step 5: Type email body
pyautogui.write('Hi,\n\nThis is a test email sent using PyAutoGUI automation.\n\nRegards,\nRPA Bot')
time.sleep(1)

# Step 6: Send the email using Ctrl + Enter
pyautogui.hotkey('ctrl', 'enter')
print("Email sent!")
