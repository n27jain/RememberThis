FROM public.ecr.aws/lambda/python:3.7

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir moviepy==1.0.3

# Copy function code
COPY process_rekognition_results.py ${LAMBDA_TASK_ROOT}

CMD [ "process_rekognition_results.lambda_handler" ]
