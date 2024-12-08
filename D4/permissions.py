import os
if os.access('/dev/ttyACM0', os.R_OK | os.W_OK):
    print("Permission to access /dev/ttyACM0 granted")
else:
    print("No permission to access /dev/ttyACM0")
