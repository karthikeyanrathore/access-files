# access-files (RBAC)


## How to setup?
```
(env) cf:~/access-files$ python3 access_files/manage.py collectstatic

164 static files copied to '/home/vagrant/access-files/access_files/static'.

(env) cf:~/access-files$ mv access_files/static/ .
(env) cf:~/access-files$ ls
access_files  docker-compose.yml  Dockerfile  env  nginx  README.md  requirements.txt  static  wait-for.sh

(env) cf:~/access-files$ docker-compose down -v
[+] Running 1/0
 ✔ Volume access-files_access_files-db_data  Removed                                                                                                                           0.0s 
(env) cf:~/access-files$ docker-compose build
[+] Building 1.7s (14/14) FINISHED  


(env) cf:~/access-files$ docker-compose up
[+] Running 5/5
 ✔ Network access-files_access_files-net       Created                                                                                                                         0.1s 
 ✔ Volume "access-files_access_files-db_data"  Created                                                                                                                         0.0s 
 ✔ Container nginx_reverse-proxy               Created                                                                                                                         0.1s 
 ✔ Container access_files-api                  Created                                                                                                                         0.1s 
 ✔ Container access_files-db                   Created 


access_files-api     | postgres is up!
access_files-api     | Operations to perform:
access_files-api     |   Apply all migrations: admin, auth, contenttypes, file_system, sessions
access_files-api     | Running migrations:
access_files-api     |   Applying contenttypes.0001_initial... OK
access_files-api     |   Applying auth.0001_initial... OK
access_files-api     |   Applying admin.0001_initial... OK
access_files-api     |   Applying admin.0002_logentry_remove_auto_add... OK
access_files-api     |   Applying admin.0003_logentry_add_action_flag_choices... OK
access_files-api     |   Applying contenttypes.0002_remove_content_type_name... OK
access_files-api     |   Applying auth.0002_alter_permission_name_max_length... OK
access_files-api     |   Applying auth.0003_alter_user_email_max_length... OK
access_files-api     |   Applying auth.0004_alter_user_username_opts... OK
access_files-api     |   Applying auth.0005_alter_user_last_login_null... OK
access_files-api     |   Applying auth.0006_require_contenttypes_0002... OK
access_files-api     |   Applying auth.0007_alter_validators_add_error_messages... OK
access_files-api     |   Applying auth.0008_alter_user_username_max_length... OK
access_files-api     |   Applying auth.0009_alter_user_last_name_max_length... OK
access_files-api     |   Applying auth.0010_alter_group_name_max_length... OK
access_files-api     |   Applying auth.0011_update_proxy_permissions... OK
access_files-api     |   Applying auth.0012_alter_user_first_name_max_length... OK
access_files-api     |   Applying file_system.0001_initial... OK
access_files-api     |   Applying file_system.0002_project_users... OK
access_files-api     |   Applying file_system.0003_alter_project_project_name... OK
access_files-api     |   Applying file_system.0004_file... OK
access_files-api     |   Applying file_system.0005_alter_file_author... OK
access_files-api     |   Applying file_system.0006_alter_file_file_bytes... OK
access_files-api     |   Applying file_system.0007_alter_file_file_bytes... OK
access_files-api     |   Applying sessions.0001_initial... OK
access_files-api     | [2024-07-24 11:40:08 +0000] [25] [INFO] Starting gunicorn 21.2.0
access_files-api     | [2024-07-24 11:40:08 +0000] [25] [INFO] Listening at: http://0.0.0.0:8000 (25)
access_files-api     | [2024-07-24 11:40:08 +0000] [25] [INFO] Using worker: sync
access_files-api     | [2024-07-24 11:40:08 +0000] [28] [INFO] Booting worker with pid: 28

```
