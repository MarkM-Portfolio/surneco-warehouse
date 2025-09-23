FROM python:3

ARG APP_DIR=/usr/src/surneco-warehouse

WORKDIR ${APP_DIR}

COPY requirements.txt .

#RUN $ mkdir ~/lib
#$ ln -s $(brew --prefix zbar)/lib/libzbar.dylib ./lib/libzbar.dylib)

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN pyinstaller --onefile --windowed --icon=app.ico surneco-warehouse.py

# RUN chown -R node:node ${APP_DIR}

# USER node

# CMD [ "python", "surneco-warehouse.py" ]
CMD [ "tail", "-f" ] # for debug