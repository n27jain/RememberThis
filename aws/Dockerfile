FROM amazon/aws-lambda-python:3.7

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY process_rekognition_results.py ${LAMBDA_TASK_ROOT}

CMD [ "process_rekognition_results.lambda_handler" ]
