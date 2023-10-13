from modules.gdrive import GoogleDrive
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    gdrive = GoogleDrive(os.getenv('CREDENTIALS_FILE'), os.getenv('TOKEN_FILE'))
    gdrive.connect(os.getenv('DRIVE_DISPLAY_NAME'))
    # gdrive.list_files(print_output = True, metadata = True)

    # Get start page token
    start_page_token = gdrive.get_start_page_token()

    # List files
    print(gdrive.list_files())

    # List changes
    print(gdrive.list_changes(start_page_token=93))