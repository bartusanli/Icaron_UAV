# Icaron İHA OpenCV Development Environment

This project contains a Python virtual environment setup for developing the Icaron UAV (İHA) software using OpenCV.

<img width="792" height="628" alt="WhatsApp Image 2026-05-13 at 12 29 50" src="https://github.com/user-attachments/assets/b8a7042b-a7cf-4751-8c4c-5a37ad6a35b8" />

<img width="797" height="630" alt="WhatsApp Image 2026-05-13 at 12 30 33" src="https://github.com/user-attachments/assets/2db76432-be37-4730-a41c-2bd68afa743d" />

<img width="787" height="630" alt="WhatsApp Image 2026-05-13 at 12 31 00" src="https://github.com/user-attachments/assets/b53d3cb7-1919-47e0-9300-453121e163d0" />



## Setup Instructions

1. Open a command prompt and navigate to the project directory:
   ```
   cd "C:\Users\bartu_110gm8e\Documents\Antigravity\Icaron_IHA"
   ```
2. Create a virtual environment (if not already created):
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Command Prompt**:
     ```
     venv\Scripts\activate.bat
     ```
   - **PowerShell**:
     ```
     .\venv\Scripts\Activate.ps1
     ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

After these steps, you can start developing your OpenCV-based Python scripts within this environment.

## Packages

- opencv-python
- numpy
- imutils
