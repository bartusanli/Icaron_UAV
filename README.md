# Icaron İHA OpenCV Development Environment

This project contains a Python virtual environment setup for developing the Icaron UAV (İHA) software using OpenCV.

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
