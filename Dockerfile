# AWS Lambda Python 3.11 container image.
# Tip: pin the base image by digest for reproducible builds, e.g.
# FROM public.ecr.aws/lambda/python:3.11@sha256:<digest>
FROM public.ecr.aws/lambda/python:3.11

# 1. Runtime environment
ENV TMPDIR=/tmp

# 2. Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 3. Application source
COPY src/ ${LAMBDA_TASK_ROOT}/src
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}"

# 4. Handler (override per function via ImageConfig.Command)
CMD [ "src.extract.app.handler" ]
