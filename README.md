# PoC for cloud forensics

This repository is a PoC for using Google Drive API through Python to retrieve metadata about files and file changes in Google Drive, as a study project in Introduction to Digital Forensics.

The only scope for this was to identify changes regarding checksums (if changes are done, and then reverted; a really simple test, really).
Also, looking whether revisions of files were changed separately to ensure that the files were "forensicly safe".


## Prerequisits (pr. 23.11.2023)
* Created a [Google Cloud project](https://developers.google.com/workspace/guides/create-project)
* A Google account with Google Drive enabled
* Python 3.10.7 or greater
* [pip](https://pypi.org/project/pip/) package management tool installed

##### References:
https://developers.google.com/drive/api/quickstart/python#prerequisites


## Setting up environment
1. Enable the Google Drive API (follow [these steps](https://developers.google.com/drive/api/quickstart/python#enable_the_api))
2. Configure OAuth (follow [these steps](https://developers.google.com/drive/api/quickstart/python#configure_the_oauth_consent_screen))
3. Authorize credentials for desktop application (follow [these steps](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application))
4. Download the `credentials.json` file, and add the file to the [json](./json/) directory

**Note:** If you have a `token.json` from before, and it's a while since last login, this file must be removed to generate a new.

5. Run the following command to install required Python libraries:
```bash
pip3 install -r requirements.txt
```

## Run the script and fetch the output JSON files
1. Log in to the given Google Drive account in the preferred web browser.

2. Run the following command in a terminal (tested with Bash and Linux):
```bash
python3 main.py
```

3. You will be prompted with a message like this in the terminal:
```
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=<CLIENT_ID>.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A43519%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.metadata.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.appdata&state=dAnko28YG2JEBFH8zb7SLn7YlJDRwX&access_type=offline
```

4. This will open the browser and you have to grant access to the data by selecting the given scopes, such as:
* See, change or delete files on Google Drive, and create new
* See, add and delete configuration data in your Google Drive account
* See information about your Google Drive files

5. A message like this will appear:

`The authentication flow has completed. You may close this window.`

6. The browser window could now be closed, and you should see a fresh [token.json](./json/token.json) file created in the [json](./json/) folder

7. The output to the [forensics-output](./forensics-output/) will appear as to files such as this:
```bash
ls -l forensics-output/
-rw-rw-r-- 1 user user  1234 nov.  18 13:37 20231120133706_file_list.json
-rw-rw-r-- 1 user user 31337 nov.  18 13:37 20231120133707_file_changes.json
```