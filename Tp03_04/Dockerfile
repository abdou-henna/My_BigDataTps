FROM python:3.13

WORKDIR /app

COPY app/amazon_reviews_us_Digital_Video_Download_v1_00.tsv /app/
COPY app/Analyse.ipynb /app/
COPY reports/PowerBiReport.pdf /reports/


COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install jupyter

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root"]
