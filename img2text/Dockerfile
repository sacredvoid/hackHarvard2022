FROM pytorch/pytorch:latest

RUN pip install transformers flask werkzeug

ADD image_to_text.py /home/app/image_to_text.py
ADD app.py /home/app/app.py

# CMD ["/home/app/app.py"]
WORKDIR /home/app/
EXPOSE 5000
CMD [ "python" , "app.py" ]