import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import boto3
import os


rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
prefix = '/mnt/files/'


def lambda_handler(event, context):
    print('Rekognition results published to SNS')

    try:
        message = event['Records'][0]['Sns']['Message']
        message = json.loads(message)
        job_id = message['JobId']
        print('Job ID is ' + job_id)
        response = rekognition.get_face_detection(JobId=job_id)
        print('Got Rekognition response')

        if response['JobStatus'] == 'FAILED':
            print('Rekognition failed')
        else:
            bucket = message['Video']['S3Bucket']
            key = message['Video']['S3ObjectName']
            print('Beginning download of ' + key + ' from ' + bucket)
            s3.download_file(bucket, key, prefix + key)
            print('Downloaded file ' + prefix + key)
            faces = response['Faces']

            segments_to_save = []
            segment_start = 0
            segment_end = 0
            found_first_smile = False

            for face in faces:
                if face['Face']['Smile']['Value']:
                    # Need to record the timestamp of the first smile
                    if not found_first_smile:
                        segment_start = segment_end = face['Timestamp']
                        found_first_smile = True

                    # Smiles must be within 20 seconds of each other to be in the same segment
                    if face['Timestamp'] - segment_end > 20000:
                        segments_to_save.append([max(segment_start - 10000, 0), segment_end + 10000])
                        segment_start = face['Timestamp']

                    segment_end = face['Timestamp']

            # The last segment smile segment won't get saved within the loop
            segments_to_save.append([max(segment_start - 10000, 0), segment_end + 10000])
            print('Determined segments to clip')

            directory = key.split('.')[0] + '/'
            for i in range(len(segments_to_save)):
                start = segments_to_save[i][0] / 1000
                end = segments_to_save[i][1] / 1000
                filename = 'tempvideo' + str(i) + '.mp4'
                ffmpeg_extract_subclip(prefix + key, start, end, prefix + filename)
                print('Uploading clip ' + str(i+1))
                s3.upload_file(prefix + filename, 'remember-this-clips', directory + str(i+1) + '.mp4')
                print('Finished uploading clip ' + str(i+1))
                os.remove(prefix + filename)

            print('Deleting ' + prefix + key)
            os.remove(prefix + key)

    except Exception as e:
        print(e)
        raise e
