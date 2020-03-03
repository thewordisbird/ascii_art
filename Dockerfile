FROM python:3.6

# set a directory for the app:
WORKDIR /usr/src/app

# install uodates and system dependencies:
RUN apt-get -yqq update

# copy all files to the container
COPY . .

# Install the app requirements and the app as an editable package (This is for testing only)
RUN pip --no-cache-dir install -r requirements.txt 
RUN pip --no-cache-dir install -e .

CMD python ascii_art/ascii_art.py

