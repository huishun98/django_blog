from django.views.decorators.http import require_POST
from django.views.generic.base import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings

import csv
import io
import boto3
import json
import sys
import os
import shutil
import zipfile
from io import BytesIO
import ast

from botocore.client import Config
from website.models import Article, Category

from datetime import date, datetime


def update_publish_timestamp(slug, time=datetime.now()):
    Article.objects.update_or_create(
        slug=slug,
        defaults={
            'published_at': time
        })


def save_article(slug, form_data):
    payload = {
        'title': form_data.get('title'),
        'description': form_data.get('description'),
        'content': form_data.get('content'),
        'saved_at': datetime.now(),
    }

    categories = form_data.getlist('category')

    if slug == 'new-post':
        article = Article.objects.create(
            title=form_data.get('title'),
            description=form_data.get('description'),
            content=form_data.get('content')
        )
        for cat in categories:
            cat, _ = Category.objects.get_or_create(name=cat)
            article.category.add(cat)
        return article

    Article.objects.update_or_create(
        slug=slug,
        defaults=payload)
    article = set_categories(slug, categories)
    return article


def delete_article(slug):
    print('deleting...')
    try:
        response = Article.objects.filter(slug=slug).delete()
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
        print(HttpResponse(json.dumps(response),
                           content_type="application/json"))


def delete_category(name):
    print('deleting...')
    try:
        response = Category.objects.filter(name=name).delete()
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
        print(HttpResponse(json.dumps(response),
                           content_type="application/json"))


def get_s3_conn():
    return boto3.resource(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )


def create_aws_zip(file_path):

    # make into another funtion to repeat in db_wrappers.py
    # byte = BytesIO()
    zf = zipfile.ZipFile(file_path, "w")

    zipped_files = []

    conn = get_s3_conn()
    bucket = conn.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    for obj in bucket.objects.all():
        key = obj.key
        body = obj.get()['Body'].read()

        zipped_files.append(key)

        open(key, 'wb').write(body)
        zf.write(key)
        os.unlink(key)

    zf.close()
    return zf


@login_required(login_url='/login/')
@require_POST
def download_blogposts(request):
    items = Article.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % settings.BACKUP_POSTS_FILENAME

    writer = csv.writer(response, delimiter='\\')
    writer.writerow(['title', 'slug', 'description', 'category',
                     'content', 'created_at', 'published_at', 'saved_at'])

    for obj in items:
        cat_list = [cat.name for cat in obj.category.all()
                    if len(cat.name.strip()) > 0]
        writer.writerow([
            obj.title,
            obj.slug,
            obj.description,
            cat_list,
            obj.content.strip('\"'),
            obj.created_at,
            obj.published_at,
            obj.saved_at
        ])

    return response


@login_required(login_url='/login/')
@require_POST
def delete_blogposts(request):
    Article.objects.all().delete()
    Category.objects.all().delete()
    return redirect('settings')


@login_required(login_url='/login/')
@require_POST
def upload_blogposts(request):
    csv_file = request.FILES.get('file')

    if not csv_file:
        return redirect('settings')

    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter='\\', quotechar='|'):
        slug = column[1]
        Article.objects.update_or_create(
            slug=slug,
            defaults={
                'title': column[0].strip('\"'),
                'description': column[2].strip('\"'),
                'content': column[4].replace('""', '"').strip('\"'),
                'created_at': column[5],
                'published_at': column[6] if column[6] else None,
                'saved_at': column[7]
            }
        )
        categories = [item for item in ast.literal_eval(column[3]) if len(item.strip()) > 0]
        set_categories(slug, categories)

    return redirect('settings')


def set_categories(slug, categories):
    article = Article.objects.get(slug=slug)
    if len(article.category.all()) > 1:
        article.category.clear()
    for cat in categories:
        cat, _ = Category.objects.get_or_create(name=cat)
        article.category.add(cat)
    return article


@login_required(login_url='/login/')
@require_POST
def download_aws_media(request):

    byte = BytesIO()

    if settings.DEBUG:
        zf = zipfile.ZipFile(byte, "w")
        zipped_files = []

        path = settings.MEDIA_ROOT
        names = os.listdir(path)

        for name in names:
            filename = path + "/" + name
            zipped_files.append(filename)

        for fpath in zipped_files:
            _, fname = os.path.split(fpath)
            zf.write(fpath, fname)
        zf.close()

    else:
        zf = create_aws_zip(byte)

    resp = HttpResponse(
        byte.getvalue(), content_type="application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % settings.BACKUP_MEDIA_FILENAME
    return resp


@login_required(login_url='/login/')
@require_POST
def upload_aws_media(request):

    zip_folder = request.FILES.get('file')

    with zipfile.ZipFile(zip_folder) as opened_folder:

        if settings.DEBUG:
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            for name in opened_folder.namelist():
                data = opened_folder.read(name)
                f = open(os.path.join(settings.MEDIA_ROOT, name), 'wb')
                f.write(data)
                f.close()

        else:
            s3 = get_s3_conn()
            for name in opened_folder.namelist():
                data = opened_folder.read(name)
                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                    Key=name, Body=data)

    return redirect('settings')


@login_required(login_url='/login/')
@require_POST
def delete_aws_media(request):

    if settings.DEBUG:
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)
        return redirect('settings')

    conn = get_s3_conn()
    bucket = conn.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
    try:
        response = bucket.objects.all().delete()
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
        print(HttpResponse(json.dumps(response),
                           content_type="application/json"))

    return redirect('settings')
