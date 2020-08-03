from __future__ import print_function
import fnmatch
import io
import os
import httplib2
from apiclient import discovery
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from oauth2client import file, client, tools
import argparse, pyperclip
from pathlib import Path


argfile = None
argcopy = None
parser = argparse.ArgumentParser(
    prog="ocr",
    usage='%(prog)s option1=value1"',)
parser.add_argument("--file", help="OCR the specified file instead of current folder.")
parser.add_argument("--copy", help="Copy OCR output into clipboard", action="store_true")
args = parser.parse_args()
if args.file != None:
    argfile = args.file
if args.copy != None:
    argcopy = args.copy


SCOPES = ("https://www.googleapis.com/auth/drive")

# Authentication
#detect/save credentials in the script path so we can run the script in other folders
scriptpath = os.path.dirname(os.path.abspath(__file__))
store = file.Storage(scriptpath + '\\token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(scriptpath + '\\credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

http = creds.authorize(httplib2.Http())
service = discovery.build("drive", "v3", http=http)


def get_file_names():
    # Create a dictionary of supported file types
    #  file_names = {filetype: list of files of this filetype}
    file_names = {"pdf": [], "jpg": [], "png": [], "gif":[], "bmp":[], "doc":[]}

    for x in os.listdir('.'):
        # os.listdir('.') returns all the files in the current folder
        for file_type in file_names.keys():
            if fnmatch.fnmatch(x, "*." + file_type):
                # If the file is of the file_type append it to the
                # corresponding list in the file_names dictionary
                file_names[file_type].append(x.replace("." + file_type,""))
    return file_names


if argfile == None:
    # print a the file lists by type
    files = get_file_names()
    for type in files:
        print(type)
        for file in files[type]:
            print("Type: " + type + "\tFile: "+ file)


def ocr(input, input_filetype, output):
    # get the mimetype based on the file extension
    mime_types = {"pdf": 'application/pdf', "jpg": 'image/jpeg', "png": 'image/png',
                 "gif": 'image/gif', "bmp": 'image/bmp', "doc": 'application/msword'}
    input_mime_type = mime_types[input_filetype]

    file_metadata = {'name': input, 'mimeType': 'application/vnd.google-apps.spreadsheet'}
    # Upload the file to Google Drive
    media = MediaFileUpload(input, mimetype=input_mime_type, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    # Print the file id
    print('File ID: %s' % file.get('id'))
    # Export the file to txt and download it
    request = service.files().export_media(fileId=file.get('id'), mimeType="text/plain")
    dl = MediaIoBaseDownload(io.FileIO(output, "wb"), request)
    is_complete = False
    while not is_complete:
        status, is_complete = dl.next_chunk()
    # Delete the uploaded file
    service.files().delete(fileId=file["id"]).execute()
    print("Output saved to " + output + ".")
    # Uncomment the following if you want to show the exported file's contents
    f = open(output, 'r', encoding="UTF-8")
    # Read file contents and remove the extra underlines at the start
    contents = f.read().replace("________________\n", "", 1)
    # Pretty print file contents
    print("\n_________________________ File Name _____________________________\n")
    print(output)
    print("\n_________________________ File Contents _________________________\n")
    print(contents)
    print("\n_________________________________________________________________\n")
    if argcopy == True:
        pyperclip.copy(contents)


if argfile == None:
    # Search for the files
    files = get_file_names()

    for file_type in files.keys():
        # Convert files for every file type
        #print("Converting: ", file_type)
        for file in files[file_type]:
            ocr(file + "." + file_type, file_type, file + "_" + file_type + "_text.txt")
else:
    file_typedot = Path(argfile).suffix
    file_type = file_typedot[1:]
    ocr(argfile, file_type, argfile + "_text.txt")
