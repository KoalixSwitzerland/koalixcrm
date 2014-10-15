
from __future__ import unicode_literals

import mimetypes
import os
import shutil
import zipfile

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.timezone import now

try:
    BACKUP_DIR = '%s/%s' % (settings.PROJECT_ROOT, settings.ADMIN_BACKUP_DIR_NAME)
except AttributeError:
    BACKUP_DIR = '%s/admin_backups' % settings.STATIC_ROOT
SQL_BACKUP_DIR = '%s/sql' % BACKUP_DIR


def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        rel_path = os.path.relpath(root, path)
        for file in files:
            filename = os.path.join(root, file)
            if os.path.isfile(filename): # regular files only
                arcname = os.path.join(rel_path, file)
                zip.write(filename, arcname)


def send_file(path, filename=None, mimetype=None):

    if filename is None:
        filename = os.path.basename(path)

    if mimetype is None:
        mimetype, encoding = mimetypes.guess_type(filename)

    response = HttpResponse(file(path, "rb").read(), content_type=mimetype)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


@staff_member_required
def admin_backup(request):
    '''
    Backs up the media and database of a Mezzanine project and returns it as a
    zip file to the admin requesting it
    '''
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)
    os.mkdir(BACKUP_DIR)
    os.mkdir(SQL_BACKUP_DIR)

    zip_path = os.path.normpath('%s/backup-%s.zip' % (BACKUP_DIR, str(now()).split('.')[0].replace(':', '').replace(' ', '_')))
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

    if not os.path.exists(zip_path):
        raise Exception("Could not create ZIP file. Check folder permissions.")

    # backup database[s]
    for db in settings.DATABASES:
        db = settings.DATABASES[db]
        if db['ENGINE'] == 'django.db.backends.sqlite3':
            if os.path.isabs(db['NAME']):
                db_file = db['NAME']
            else:
                db_file = '%s/%s' % (settings.PROJECT_ROOT, db['NAME'])
            shutil.copy(db_file, SQL_BACKUP_DIR)

        elif db['ENGINE'] == 'django.db.backends.mysql':
            os.system('mysqldump -u %s %s -p%s > %s/%s.sql' % (
                db['USER'],
                db['NAME'],
                db['PASSWORD'],
                SQL_BACKUP_DIR,
                db['NAME']))

        elif db['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            # requires that a .pgpass file is configured
            os.system('pg_dump -Fc -w -U %s -f %s/%s.sql %s' % (
                db['USER'],
                SQL_BACKUP_DIR,
                db['NAME'],
                db['NAME']))

    zipdir(SQL_BACKUP_DIR, zipf)
    # add the media library to the zip
    zipdir(settings.MEDIA_ROOT, zipf)
    zipf.close()

    return send_file(zip_path)
