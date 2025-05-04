FROM python:3.9-slim

WORKDIR /app

COPY /.streamlit /app/.streamlit/
COPY /images /app/images/
COPY /pages /app/pages/
COPY Cloudy_Points.py /app/
COPY requirements-interface.txt /app/

ENV PORT=8501

RUN pip install -r requirements-interface.txt

CMD streamlit run Cloudy_Points.py --server.port $PORT --server.address=0.0.0.0
