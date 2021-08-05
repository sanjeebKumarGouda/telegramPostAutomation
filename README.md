# telegramPostAutomation
## Automating Telegram Post using Selenium library in Python
1. Install **```autoit-v3-setup```** (setup file is uploaded)
2. Install **```SciTE4AutoIt3```** (setup file is uploaded)
3. Keep **```chromedriver.exe```** (setup file is uploaded) in your local machine and use its path in python script.
4. Also to automate Windows GUI (to upload file) we need to write another script and create an executable file for that which will be called during the execution of the main python script.
5. GUI automation script and its .exe file **```[fileUploadScript.au3 and fileUploadScript.exe]```** is also uploaded. (We need to edit that script as per our requirement)

6. open Anaconda prompt, change file directory path i.e., cd path_to_folder
7. **```conda create -n telegramAutomation python=3.7```**
8. **```conda activate telegramAutomation```**
9. **```conda install spyder```**

```pip install -r path_of_requirments.txt```

10. **```selenium==3.141.0```**
11. **```oauth2client==4.1.3```**
12. **```df2gspread==1.0.4```**
13. **```gspread==3.7.0```**
14. **```pandas==1.2.0```**

15. After above installation type **```spyder```** in Anaconda prompt. Now Spyder IDE will open in sometime.
16. open **```script_final.py```** in spyder
Edit in Lines 28,40,48,66,68,145,149,174,175,180 in script.(change path of files used according to your local machine)
17. When a new folder needs to be added we need to edit the ```script_final.py``` script. Steps for that
* When new folder for commodity “garlic” needs to be added inside vegetables then in script line-145 add ```{"vegetables_garlic_hindi" : "vegetables_garlic_hi", "vegetables_garlic_english":"vegetables_garlic_en"}```
* When new folder for category “fruits” needs to be added then inside fruits folder “apple” needs to added then in script line-145 add ```{"fruits_apple_hindi" : "fruits_apple_hi", " fruits _apple_english":"fruits_apple_en"}``` These changes are case sensitive.

18. Then Inside each new ```Folder > Subfolder [i.e., fruits > apple > hindi]``` we need to add files like ```fruits_apple_hi.au3``` (this file name will different for different category name, commodity name & language) file then open it and edit it. After editing, right click on that file and click ```Compile Script (x64)```, so that ```fruits_apple_hi.exe``` file will be generated.
