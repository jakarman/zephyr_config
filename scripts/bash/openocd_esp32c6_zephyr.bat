@echo off
cd /d C:\Users\USER\Desktop\zephyrproject\my_tools\openocd-esp32\bin
openocd.exe -s ..\share\openocd\scripts\ -c "set ESP_RTOS none; set ESP_FLASH_SIZE 0" -f board/esp32c6-builtin.cfg
