FROM python:3.11-slim
COPY wait_for_approval.py /wait_for_approval.py
RUN pip install requests
ENTRYPOINT ["python", "/wait_for_approval.py"]