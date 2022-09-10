# yamdb_final
yamdb_final
![workflow](https://github.com/NikolayRudakkov/yambd_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## **�� ������:**


* ���: ������� �������	
* ��� ������������: ������� ����� ������.��������� Python-�����������
* ��������: https://github.com/NikolayRudakov/


## **��������:**

������ YaMDb �������� ������ (Review) ������������� �� ������������ (Titles). ������������ ������� �� ���������: ������, ��������, �������. ������ ��������� (Category) ����� ���� �������� ��������������� (��������, ����� �������� ��������� ���������������� ��������� ��� ���������).
���� ������������ � YaMDb �� ��������, ����� ������ ���������� ����� ��� ��������� ������.
� ������ ��������� ���� ������������: �����, ������ ��� ������. ��������, � ��������� ������ ����� ���� ������������ ������-��� � ���-���-��� � ������������ �������, � � ��������� ������� � ����� ������� ������ ���������� � ������ ����� ����.
������������ ����� ���� �������� ���� (Genre) �� ������ ����������������� (��������, �������, ���� ��� ��������). ����� ����� ����� ��������� ������ �������������.
����������� ��� ����������� ������������ ��������� � ������������� ��������� ������ (Review) � ������ ������������ ������ � ��������� �� ������ �� ������ (����� �����); �� ���������������� ������ ����������� ���������� ������ ������������ � ������� (����� �����). �� ���� ������������ ������������ ����� �������� ������ ���� �����.

---
# �������� Workflow
##### Workflow ������� �� ������ �����:
###### tests
- �������� ���� �� ������������ PEP8, �������������� ������ ������.
###### Push Docker image to Docker Hub
- ������ � ���������� ������ �� DockerHub.
###### deploy 
- �������������� ������ �� ������ ������ ��� ���� � ������� ����� main.
###### send_massage
- �������� ����������� � ��������-���.

## ���������� � ������ �������
##### ������������ �����������
����������� ����������� �� ��������� ������:
```bash
git clone https://github.com/NikolayRudaov/yamdb_final.git
```

## ��������� �� ��������� ������� (Ubuntu):
##### ��� 1. ��������� ���� �� ���� ��������� ������
������, ��� ���������� � ������, ���������� ��������� ���� �� ���� ��������� ������:
```bash
ssh <USERNAME>@<IP_ADDRESS>
```

##### ��� 2. ���������� docker �� ������:
������� �������:
```bash
sudo apt install docker.io 
```

##### ��� 3. ���������� docker-compose �� ������:
������� �������:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

##### ��� 4. ���������� �������������� �����:
���������� �������������� ����� `docker-compose.yaml` � `nginx/default.conf` �� ������ ������� �� ������ � `home/<���_username>/docker-compose.yaml` � `home/<���_username>/nginx/default.conf` ��������������.
������� ������� �� �������� ����� �������:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp -r nginx/ <username>@<host>:/home/<username>/
```

##### ��� 5. �������� Secrets:
��� ������ � Workflow �������� � Secrets GitHub ���������� ��������� ��� ������:
```bash
SECRET_KEY=<SECRET_KEY>
DEBUG=<True/False>
ALLOWED_HOSTS=<hosts>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<������ DockerHub>
DOCKER_USERNAME=<��� ������������ DockerHub>

USER=<username ��� ����������� � �������>
HOST=<IP �������>
PASSPHRASE=<������ ��� �������, ���� �� ����������>
SSH_KEY=<��� SSH ���� (��� ��������� �������: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID ������ ��������-��������>
TELEGRAM_TOKEN=<����� ������ ����>
```

##### ��� 6. ����� ��������� ������:
������� �� ������ ������ � ��������� ������� (������ ����� ������� ������):
###### ������� � ��������� ��������:
```bash
sudo docker-compose exec web python manage.py makemigrations --noinput
sudo docker-compose exec web python manage.py migrate --noinput
```
###### ���������� �������
```bash
sudo docker-compose exec web python manage.py collectstatic --no-input 
```
###### ��������� ���� ������:
```bash
sudo docker-compose exec web python3 manage.py loaddata fixtures.json
```
###### ������� ����������������� Django:
```bash
sudo docker-compose exec web python manage.py createsuperuser
```

##### ��� 7. ������ �������
������ ����� �������� �� ������ IP-������.

������ �������� �� ������: http://51.250.106.201/api/v1/

����� �� DockerHub: https://hub.docker.com/repository/docker/nrudaov/yamdb_final


## **������������ API YaMDb**

������������ �������� �� ���������: http://localhost/redoc/
