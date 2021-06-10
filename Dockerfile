FROM python:3.8.5

COPY ./app/ ./app

WORKDIR ./app

# pip install
COPY requirements.txt ./
RUN pip install --upgrade pip && \ 
    pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html && \ 
    pip install --target ./ --no-cache-dir -r requirements.txt 


CMD ["python", "api.py"]