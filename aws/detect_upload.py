import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print('Detected upload of file ' + key + ' to bucket ' + bucket)
    try:
        response = rekognition.start_face_detection(
            Video={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            NotificationChannel={
                'SNSTopicArn': 'arn:aws:sns:us-west-1:539380743829:AmazonRekognitionTopic',
                'RoleArn': 'arn:aws:iam::539380743829:role/RekognitionSNS'
            },
            FaceAttributes='ALL'
        )

        print("Started job " + response['JobId'])
        return response['JobId']

    except Exception as e:
        print(e)
        raise e
