FROM tiagopeixoto/graph-tool

WORKDIR /app
COPY . .

RUN pacman -S --noconfirm python-pip 
RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "src/main.py"]