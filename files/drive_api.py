import datetime
import io
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def create_folder(name, parent=''):
    """create folder with name and inside parent folder id
    :returns dectionary with name id mimetype
     ex. {'kind': 'drive#file', 'id': '1nML9f8GBTKu2mnNfy5qClHmU4sLFlsj5', 'name': 'test1', 'mimeType': 'application/vnd.google-apps.folder'}
     """
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent != '':
        file_metadata['parents'] = [parent]

    res = service.files().create(body=file_metadata).execute()
    print(f'folder created {name}')
    return res


def upload_file(file_name, file_path, folder_id, mime_type):
    """ upload file to folder id given
    :returns dictionary with id namein drive mimetype
    ex. {'kind': 'drive#file', 'id': '18Vi0eE5qdA220tIaoIiodtbU3eknWLuZ', 'name': 'mytestfile1.png', 'mimeType': 'image/png'}
    """
    # folder_id = '1TrJz2EY2QKX46GqR8HaBFjJi9WSHsUro'
    # file_names = ['hash.txt']
    # mime_types = ['text/plain']

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(
        body=file_metadata,
        media_body=media
    ).execute()
    print(f'file uploaded {file_name}')
    return file


def download_file(file_id, file_path):
    """download file with id and save to path given
     :returns path where saved ex. test.png
     """
    # file_id = '1R-p5M50CZ6e4gOEP6GDd7Tx8YrnzzqM4'
    # file_name = 'test.txt'

    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        # print("Download progress {}".format(status.progress() * 100))
    fh.seek(0)
    with open(file_path, 'wb') as f:
        f.write(fh.read())
    print('file downloaded ')
    return file_path


def update_file(file_path, mime_type, file_id_old):
    """update existing fle with file id given in any folder in drive
    :returns dictionary with id name mimetype ex. {
    'kind': 'drive#file', 'id': '1KkekFhjEOTxg87T495cS3giBE7Stww4N', 'name': 'mytestfile1.png', 'mimeType':
    'image/png'}
    """
    # folder_id = '1TrJz2EY2QKX46GqR8HaBFjJi9WSHsUro'
    # file_names = ['hash.txt']
    # mime_types = ['text/plain']
    # fileid= '1LuG__t3cqjzDpK1lMVvU6jl0lXTjhpgU'

    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().update(
        fileId=file_id_old,
        media_body=media
    ).execute()
    print(f'file updated {file_path}')
    return file


def list_files(folder_id=''):
    """returns list of dictionaries with id name and mimetype
    ex.[{'kind': 'drive#file', 'id': '1R-p5M50CZ6e4gOEP6GDd7Tx8YrnzzqM4', 'name': 'try.txt', 'mimeType': 'text/plain'}, {'kind': 'drive#file', 'id': '1LuG__t3cqjzDpK1lMVvU6jl0lXTjhpgU', 'name': 'hash.txt', 'mimeType': 'text/plain'}, {'kind': 'drive#file', 'id': '1xwmHTL2qXewYahqept3nOeDuGPOzhpP1', 'name': 'hash.txt', 'mimeType': 'text/plain'}]
    """
    # folder_id = '1TrJz2EY2QKX46GqR8HaBFjJi9WSHsUro'
    if folder_id != '':
        query = f"parents = '{folder_id}'"
        resp = service.files().list(q=query).execute()
        files = resp.get('files')

        next_page_token = resp.get('nextPageToken')
        while next_page_token:
            resp = service.files().list(q=query).execute()
            files.extend(resp.get('files'))
            next_page_token = resp.get('nextPageToken')
        return files

    else:
        query = "mimeType = 'application/vnd.google-apps.folder'"
        resp = service.files().list(q=query).execute()
        files = resp.get('files')

        next_page_token = resp.get('nextPageToken')
        while next_page_token:
            resp = service.files().list(q=query).execute()
            files.extend(resp.get('files'))
            next_page_token = resp.get('nextPageToken')
        return files


def set_data(name, data, mime_type='text/plain'):
    """ upload file to folder id given
    :returns dictionary with id namein drive mimetype
    ex. {'kind': 'drive#file', 'id': '18Vi0eE5qdA220tIaoIiodtbU3eknWLuZ', 'name': 'mytestfile1.png', 'mimeType': 'image/png'}
    """
    folder_id = get_folder_id('MyPasswordWallet')
    with open(f'{name}', 'w') as file:
        file.write(data)
    status_file, id_file = if_exists(name)
    if not status_file:
        res = upload_file(name, f'{name}', folder_id, mime_type)
    else:
        res = update_file(f'{name}', mime_type, id_file)
    os.remove(f'{name}')
    return res


def get_data(name):
    """returns data in the file in binary mode"""
    file_status, file_id = if_exists(name)
    if file_status:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            # print("Download progress {}".format(status.progress() * 100))
        fh.seek(0)
        return fh.read().decode('ascii')
    else:
        return '{}'


def get_folder_id(name):
    folders = list_files()
    for folder in folders:
        if folder['name'] == name:
            id = folder['id']
            print(f'Folder exists {name}')
            return id
    res = create_folder(name)
    return res['id']


def if_exists(name):
    folder_id = get_folder_id('MyPasswordWallet')

    files = list_files(folder_id)
    for file in files:
        if file['name'] == name:
            file_id = file['id']
            print(f'file exists {name}')
            return True, file_id
    return False, ''


if __name__ == '__main__':
    print('Working')
