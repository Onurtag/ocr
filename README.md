# ocr  
Simple OCR script that uses Google Drive's OCR capabilities.  

To make it work, install python, extract this repo to a folder and then do the following:  
  
1. Visit ```https://developers.google.com/drive/api/v3/quickstart/python```  
2. Click Enable The Drive API  
3. Login with your Google account  
4. Click "Download Client configuration"  
5. Copy the credentials.json to the same folder with ocr.py  
6. install the requirements with the following command:  
```pip install -r requirements.txt```  

### **Commandline arguments:**  
- **--file="C:\path\to\file.png"** : Allows you to specify a single file to OCR.  
- **--copy** : OCR output will be automatically copied to clipboard  

### **Example usage with ShareX:**  
Add the following action  
- **Path:** C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe  
- **Arguments:** python "C:\your\path\to\ocr.py" --copy --file=$input  
- **Hidden Window:** Enabled 

❗ *On first run it will open your browser to verify permissions. If you see "This app isn't verified" ... click on Advanced and click on Go to Quickstart (unsafe). Then click Allow and Allow. You can close the browser tab. The execution begins.*  

### **Manual Execution on a folder:**  
Copy any files you need to convert in the same folder with the script and run "python ocr.py" in your preferred commandline (powershell/cmd/etc). You can also call the script from another folder to ocr files that are in that folder.  
-> Filetypes supported: pdf, jpg, png, gif, bmp, doc  
  
The script will list the supported files, upload each one to Google Drive and export/download the text version of them.  
  
Example: original.jpg -> the exported will be original_jpg_text.txt, original.pdf -> the exported will be original_pdf_text.txt etc  
