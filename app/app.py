import boto3
import requests
import json
import tempfile
import os
from datetime import datetime, timezone, timedelta

def get_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_data_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def upload_to_s3(bucket, file_path, key):
    profile = os.environ.get('AWS_PROFILE')

    if profile:
        session = boto3.Session(profile_name=profile)
        s3 = session.client('s3')
    else:
        s3 = boto3.client('s3')

    s3.upload_file(file_path, bucket, key)

def lambda_handler(event, context):
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST)
    date_str = now.strftime('%Y%m%d')

    urls = [
        ("https://zenn-api.netlify.app/trendTech.json", 'zenn', f'zenn_trendTech_{date_str}.json'),
        ("https://zenn-api.netlify.app/trendIdea.json", 'zenn', f'zenn_trendIdea_{date_str}.json'),
        ("https://qiita-api.vercel.app/trend.json", 'qiita', f'qiita_trend_{date_str}.json'),
    ]

    bucket = os.environ.get('S3_BUCKET_NAME')

    with tempfile.TemporaryDirectory() as temp_dir:
        for url, prefix, file_name in urls:
            temp_file_path = f"{temp_dir}/{file_name}"
            s3_key = f"{prefix}/{file_name}"
            try:
                data = get_data_from_api(url)
                save_data_to_file(data, temp_file_path)
                upload_to_s3(bucket, temp_file_path, s3_key)
            except requests.exceptions.RequestException as e:
                print(f"Error while fetching data from {url}: {e}")
            except IOError as e:
                print(f"Error while saving data to {temp_file_path}: {e}")
            except Exception as e:
                print(f"Error while uploading data to S3: {e}")
