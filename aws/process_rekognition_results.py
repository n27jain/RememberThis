import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import boto3


rekognition = boto3.client('rekognition')


def lambda_handler(event, context):
    print('Rekognition results published to SNS')

    try:
        message = event['Records'][0]['Sns']['Message']
        message = json.loads(message)
        job_id = message['JobId']
        response = rekognition.get_face_detection(JobId=job_id)

        if response['JobStatus'] == 'FAILED':
            print('Rekognition failed')
        else:
            for face in response['Faces']:
                print(face)

    except Exception as e:
        print(e)
        raise e
