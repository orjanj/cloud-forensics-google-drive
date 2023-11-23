from modules.gdrive import GoogleDrive
from modules.file import File
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    gdrive = GoogleDrive(os.getenv('CREDENTIALS_FILE'), os.getenv('TOKEN_FILE'))
    gdrive.connect()
    # gdrive.list_files(print_output = False, metadata = True)

    # Get start page token
    start_page_token = gdrive.get_start_page_token()

    # List files and write to file
    file = File("file_list.json")
    file.write(gdrive.list_files(metadata = True))
    # Metadata must be set to print json blob to file
    # setting this to `False` will only give a file list and file id

    # List changes
    file = File("file_changes.json")
    file.write(gdrive.list_changes(start_page_token=93))
