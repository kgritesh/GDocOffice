# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
import os
import webbrowser

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys

SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/{}/edit'

APPLICATION_MAP = {
    'spreadhsheet': {
        'extensions': ['.csv', '.xls', '.xlsx', '.xlsm', '.xlt', '.xltx',
                       '.xltm' '.ods', '.tsv', '.txt', '.tab'],
        'url': 'spreadsheets'

    },
    'document': {
        'extensions': ['.doc', '.docx', '.docm', '.dot', '.dotx', '.dotm', '.html', '.txt',
                       '.rtf', '.odt'],
        'url': 'document',
    },

    'presentation': {
        'extensions': ['.ppt', '.pptx', '.pptm', '.pps', '.ppsx', '.ppsm', '.pot',
                       '.potx', '.potm'],
        'url': 'presentation'
    },


    'drawing': {
        'extensions': ['.jpg', '.jpeg', '.png', '.svg', '.gdraw'],
        'url': 'drawing'
    },
}


def get_mime_type(app_type):
    return 'application/vnd.google-apps.{}'.format(app_type)


def get_url(app_type, file_id):
    url_part = APPLICATION_MAP[app_type]['url']
    return "https://docs.google.com/{}/d/{}/edit".format(url_part, file_id)


def create_ext_app_map():
    ext_map = {}
    for app, value in APPLICATION_MAP.items():
        for ext in value['extensions']:
            ext_map[ext] = app
    return ext_map


def main(filepath):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    ext_map = create_ext_app_map()
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)

    app = ext_map[ext]

    print "Name of file", name

    body = {
        'name': name,
        'mimeType': get_mime_type(app_type=app)
    }

    drive = GoogleDrive(gauth)
    gfile = drive.CreateFile({'title': filename})
    gfile.SetContentFile(filepath)
    gfile.Upload(param=dict(body=body, convert=True))
    url = get_url(app, gfile['id'])
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    main(sys.argv[1])
