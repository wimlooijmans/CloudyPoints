FROM python:3.12
WORKDIR /src
COPY requirements.txt .
COPY /models/DPT_Hybrid_1.ckpt ../models/DPT_Hybrid_1.ckpt
COPY /src/berlin_000000_000019_depth_image.png .
COPY /src/berlin_000000_000019_left_image.png .
COPY /src/cityscapes_dataset.py .
COPY /src/model_loader.py .
COPY /src/run.py .
COPY /src/templates/welcome.html /src/templates/
COPY /src/templates/result.html /src/templates/
EXPOSE 8080
RUN pip install -r requirements.txt
ENV FLASK_APP=run.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]