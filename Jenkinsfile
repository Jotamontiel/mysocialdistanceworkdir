def remote = [:]
remote.name = "www.socialdistance.cl"
remote.host = "167.172.149.133"
remote.allowAnyHosts = true

node {
    withCredentials([sshUserPrivateKey(credentialsId: 'the-real-user-for-webserver-1', keyFileVariable: 'WEBSERVER_KEYFILE', passphraseVariable: '', usernameVariable: 'WEBSERVER_USER')]) {
        remote.user = WEBSERVER_USER
        remote.identityFile = WEBSERVER_KEYFILE
        stage("Stage 1: Stop Processes") {
            echo "---------------------------------------------------------------------"
            echo "---------------- Stop Processes Starting ----------------------------"
            echo "---------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            echo "**********************************************"
            echo "****** Stop Celery Service *******************"
            echo "**********************************************"
            sudo systemctl stop celery.service
            echo "**********************************************"
            echo "****** Stop Celery Beat Service **************"
            echo "**********************************************"
            sudo systemctl stop celerybeat.service
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Stopped Processes -----------------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 2: Reset & Update Master Branch") {
            echo "---------------------------------------------------------------------"
            echo "---------------- Reset & Update Master Branch Starting --------------"
            echo "---------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkdir
            git reset --hard
            git pull origin main
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Master Branch Reset and Updated ---------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 3: Create Media Files Backup") {
            echo "---------------------------------------------------------------------"
            echo "---------------- Create Media Files Backup --------------------------"
            echo "---------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkpackage
            cd prod_mediafiles_bkp
            sudo rm -r media
            """
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkdir
            sudo cp -R media /home/jorge/mysocialdistanceworkpackage/prod_mediafiles_bkp/
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Media Files Backup Created --------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 4: Create Prod Tables & Full Database Backups") {
            echo "---------------------------------------------------------------------"
            echo "---------------- Create Prod Tables & Full Database Backups ---------"
            echo "---------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkpackage
            sudo rm -r prod_tables_bkp
            sudo rm -r full_database_bkp
            sudo mkdir prod_tables_bkp
            sudo mkdir full_database_bkp
            """
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkpackage
            cd trigger_queries
            sudo ./prod_tables_bkp_script
            sudo ./full_database_bkp_script
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Prod Tables & Full Database Backups Created ---------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 5: Clear Static Files") {
            echo "---------------------------------------------------------------------"
            echo "---------------- Clear Static Files Starting ------------------------"
            echo "---------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkdir
            sudo rm -r static
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Directory cleaned -----------------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 6: Create Virtual Environment") {
            echo "----------------------------------------------------------------------"
            echo "---------------- Environment Creation Starting -----------------------"
            echo "----------------------------------------------------------------------"
            try {
                sshCommand remote: remote, command: """
                cd mysocialdistanceworkdir
                rm -r mysocialdistanceworkenv
                virtualenv mysocialdistanceworkenv
                source mysocialdistanceworkenv/bin/activate
                pip install -r requirements.txt
                """
            } catch (err) {
                echo "Caught: ${err}"
            }
            echo "----------------------------------------------------------------------"
            echo "---------------- Environment Created ---------------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 7: Database Reset") {
            echo "----------------------------------------------------------------------"
            echo "---------------- Database Reset Starting -----------------------------"
            echo "----------------------------------------------------------------------"
            sshCommand remote: remote, command: """
                cd mysocialdistanceworkpackage
                cd trigger_queries
                sudo -h 167.172.149.133 -u postgres bash -c "psql -f db_reset_query.sql"
                """
            echo "----------------------------------------------------------------------"
            echo "---------------- Database Built --------------------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 8: Build Migrations & Migrate") {
            echo "----------------------------------------------------------------------"
            echo "---------------- Build Migrations & Migrate Starting -----------------"
            echo "----------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkdir
            source mysocialdistanceworkenv/bin/activate
            python manage.py makemigrations
            python manage.py migrate
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Built & Migrated Migrations -------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 9: Static Files Collection"){
            echo "----------------------------------------------------------------------"
            echo "---------------- Static Files Collection Starting --------------------"
            echo "----------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkdir
            source mysocialdistanceworkenv/bin/activate
            python manage.py collectstatic --noinput
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Static Files Collected ------------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 10: Create Superuser"){
            withCredentials([usernamePassword(credentialsId: 'the-real-user-password-for-BD-webserver-1', passwordVariable: 'JENKINS_BD_PASS', usernameVariable: 'JENKINS_BD_USER')]) {
                echo "----------------------------------------------------------------------"
                echo "---------------- Superuser Creation Starting -------------------------"
                echo "----------------------------------------------------------------------"
                sshCommand remote: remote, command: """
                cd mysocialdistanceworkdir
                source mysocialdistanceworkenv/bin/activate
                echo "from django.contrib.auth.models import User; User.objects.create_superuser('$JENKINS_BD_USER', 'jorgemontielmontiel@gmail.com', '$JENKINS_BD_PASS')" | python manage.py shell 
                """
                echo "----------------------------------------------------------------------"
                echo "---------------- Superuser created -----------------------------------"
                echo "----------------------------------------------------------------------"
            }
        }
        stage("Stage 11: Database Repopulate") {
            echo "---------------------------------------------------------------------"
            echo "---------------- Database Repopulate --------------------------------"
            echo "---------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            cd mysocialdistanceworkpackage
            cd trigger_queries
            sudo ./repopulate_database_script
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Database Repopulated --------------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 12: Restart Services"){
            echo "----------------------------------------------------------------------"
            echo "---------------- Restart Services Starting ---------------------------"
            echo "----------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            echo "**************************************************"
            echo "****** Daemon Reload *****************************"
            echo "**************************************************"
            sudo systemctl daemon-reload
            echo "**************************************************"
            echo "****** Restart Gunicorn **************************"
            echo "**************************************************"
            sudo systemctl restart gunicorn
            echo "**************************************************"
            echo "****** Restart Nginx *****************************"
            echo "**************************************************"
            sudo systemctl restart nginx
            echo "**************************************************"
            echo "****** Restart Celery ****************************"
            echo "**************************************************"
            sudo systemctl restart celery.service
            echo "**************************************************"
            echo "****** Restart Celery Beat ***********************"
            echo "**************************************************"
            sudo systemctl restart celerybeat.service
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Services Restarted ----------------------------------"
            echo "----------------------------------------------------------------------"
        }
    }
}

// Recommendations before running the pipeline:
//
// *****************************************************
// ********** MODULE 1: "Website Preparation" **********
// *****************************************************
//
// 1°) Installing the Packages from the Ubuntu Repositories, If you are using Django with Python 3, type:
//  sudo apt update
//  sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl 
// 2°) Virtualenv Global Installation:
//  sudo -H pip3 install --upgrade pip
//  sudo -H pip3 install virtualenv
// 3°) Creating the PostgreSQL User.
//  sudo -u postgres psql
//  CREATE USER myprojectuser WITH PASSWORD 'password';
//  ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
//  ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
//  ALTER ROLE myprojectuser SET timezone TO 'UTC';
//  \q
// 4°) Prepare the onetime git clone project, the project must be in the root path: home/jorge/ with the name "myprojectdir"
// 5°) Make sure to add manually the settings.py file (Production Version) in the next path: home/jorge/miprojectdir/myproject/
// 6°) Prepare the queries.sql file to reset the database, the file must be in the root path: home/jorge/
// 7°) Creating systemd Socket and Service Files for Gunicorn:
//
//  COMMAND: sudo nano /etc/systemd/system/gunicorn.socket
//
// ********** /etc/systemd/system/gunicorn.socket **********
// [Unit]
// Description=gunicorn socket
//
// [Socket]
// ListenStream=/run/gunicorn.sock
//
// [Install]
// WantedBy=sockets.target
//
//  COMMAND: sudo nano /etc/systemd/system/gunicorn.service
//
// ********** /etc/systemd/system/gunicorn.service **********
// [Unit]
// Description=gunicorn daemon
// Requires=gunicorn.socket
// After=network.target
//
// [Service]
// User=sammy
// Group=www-data
// WorkingDirectory=/home/sammy/myprojectdir
// ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
//           --access-logfile - \
//           --workers 3 \
//           --bind unix:/run/gunicorn.sock \
//           myproject.wsgi:application
//
// [Install]
// WantedBy=multi-user.target
//
//  COMMAND: sudo systemctl start gunicorn.socket
//  COMMAND: sudo systemctl enable gunicorn.socket
//
// 8°) Checking for the Gunicorn Socket File:
//
//  COMMAND: sudo systemctl status gunicorn.socket
//  COMMAND: file /run/gunicorn.sock
// Output
// /run/gunicorn.sock: socket
//
// 9°) Testing Socket Activation:
//
//  COMMAND: sudo systemctl status gunicorn
// Output
// ● gunicorn.service - gunicorn daemon
//    Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
//    Active: inactive (dead)
//
//  COMMAND: curl --unix-socket /run/gunicorn.sock localhost
//  COMMAND: sudo systemctl status gunicorn
// Output
// ● gunicorn.service - gunicorn daemon
//    Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
//    Active: active (running) since Mon 2018-07-09 20:00:40 UTC; 4s ago
//  Main PID: 1157 (gunicorn)
//     Tasks: 4 (limit: 1153)
//    CGroup: /system.slice/gunicorn.service
//            ├─1157 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
//            ├─1178 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
//            ├─1180 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
//            └─1181 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
// Jul 09 20:00:40 django1 systemd[1]: Started gunicorn daemon.
// Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1157] [INFO] Starting gunicorn 19.9.0
// Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1157] [INFO] Listening at: unix:/run/gunicorn.sock (1157)
// Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1157] [INFO] Using worker: sync
// Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1178] [INFO] Booting worker with pid: 1178
// Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1180] [INFO] Booting worker with pid: 1180
// Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1181] [INFO] Booting worker with pid: 1181
// Jul 09 20:00:41 django1 gunicorn[1157]:  - - [09/Jul/2018:20:00:41 +0000] "GET / HTTP/1.1" 200 16348 "-" "curl/7.58.0"
//
//  COMMAND: sudo systemctl daemon-reload
//  COMMAND: sudo systemctl restart gunicorn
//
// 10°) Configure Nginx to Proxy Pass to Gunicorn:
//
//  COMMAND: sudo nano /etc/nginx/sites-available/myproject
//
// ********** /etc/nginx/sites-available/myproject **********
// server {
//     listen 80;
//     server_name server_domain_or_IP;
//
//     location = /favicon.ico { access_log off; log_not_found off; }
//     location /static/ {
//         root /home/sammy/myprojectdir;
//     }
//
//     location / {
//         include proxy_params;
//         proxy_pass http://unix:/run/gunicorn.sock;
//     }
// }
//
//  COMMAND: sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
//  COMMAND: sudo nginx -t
//  COMMAND: sudo systemctl restart nginx
//  COMMAND: sudo ufw delete allow 8000
//  COMMAND: sudo ufw allow 'Nginx Full'
//
// *****************************************************
// ********** MODULE 2: "Celery Preparation" ***********
// *****************************************************
//
// 1°) Installing the Packages from the Ubuntu Repositories:
//
//  COMMAND: sudo apt-get update
//  COMMAND: sudo apt-get upgrade
//  COMMAND: sudo apt-get install redis-server
//  COMMAND: sudo service redis-server restart
//
// 2°) Others commands por redis broker:
//
//  COMMAND: sudo service redis-server stop
//  COMMAND: sudo service redis-server start
//  COMMAND: sudo service redis-server restart
// 
// 3°) This command take the celery workers activation:
//
//  COMMAND: celery -A nombre_proyecto worker --loglevel=INFO       #Windows Version
//  COMMAND: celery -A nombre_proyecto worker --pool=solo -l info   #Linux   Version
//
// 4°) This command take the celery beat activation:
//
//  COMMAND: celery -A nombre_proyecto beat                                                                       #Original Version
//  COMMAND: celery -A nombre_proyecto beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler   #Django   Version
//
// 5°) This command take the celery flower activation:
//
//  COMMAND: celery -A nombre_proyecto flower                                                                     #Original Version
//
// NOTE: Take a look for "http://localhost:5555" to see the results
// NOTE 2: Take a look for Celery Director for better workflows views in the browser
//
// 6°) Celery Workers and beat Demonization using systemd:
//
// 6.1) Make you sure to add the nexts code lines in the "settings.py" django project in the file end:
//
//  COMMAND: sudo nano /home/jorge/mysocialdistanceworkdir/socialdistancework/settings.py
//
// ********** /home/jorge/mysocialdistanceworkdir/socialdistancework/settings.py **********
// # project name : socialdistancework
// # project directory : /home/jorge/mysocialdistanceworkdir/
// # project env : /home/jorge/mysocialdistanceworkdir/mysocialdistanceworkenv/
//
// # Celeryd Configuration
// CELERY_APP="socialdistancework"
// CELERY_BIN="/home/jorge/mysocialdistanceworkdir/mysocialdistanceworkenv/bin/celery"
// CELERYD_NODES="worker"
// #CELERYD_OPTS=
// CELERYD_CHDIR="/home/jorge/mysocialdistanceworkdir"
// CELERYD_PID_FILE="/var/run/celery/%n.pid"
// CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
// CELERYD_LOG_LEVEL="INFO"
// CELERYD_USER="celery"
// CELERYD_GROUP="celery"
// CELERY_CREATE_DIRS=1
// #CELERY_CREATE_RUNDIR=
// #CELERY_CREATE_LOGDIR=
//
// # Celerybeat Configuration
// CELERYBEAT_OPTS="--scheduler django_celery_beat.schedulers:DatabaseScheduler"
// CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
// CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"
// CELERYBEAT_LOG_LEVEL="INFO"
// CELERYBEAT_USER="celery"
// CELERYBEAT_GROUP="celery"
// CELERYBEAT_CHDIR="/home/jorge/mysocialdistanceworkdir"
//
//
// 6.2) (OPTIONAL) Now we can create the "celery" user to use the services, later add the user to "sudo" permission list in the end of sudoers file:
//
//  COMMAND: sudo adduser celery
//  COMMAND: nano etc/sudoers
//  ADD_LINE: celery ALL=(ALL) NOPASSWD: ALL
//
// NOTE: Remmember use secure password !!
//
//
// 6.3) Now we need create the logs directories and grant to "celery" user the owner level:
//
//  COMMAND: sudo mkdir /var/log/celery
//  COMMAND: sudo mkdir /var/run/celery
//  COMMAND: sudo chown -R celery: /var/log/celery
//  COMMAND: sudo chown -R celery: /var/run/celery
//
//
// 6.4) Now we can create the "celery.service":
//
//  COMMAND: sudo nano /etc/systemd/system/celery.service
//
// ********** /etc/systemd/system/celery.service **********
// [Unit]
// Description=Celery Service
// After=network.target
//
// [Service]
// Type=simple
// User=celery
// Group=celery
// EnvironmentFile=/home/jorge/mysocialdistanceworkdir/socialdistancework/settings.py
// WorkingDirectory=/home/jorge/mysocialdistanceworkdir
// ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} ${CELERYD_NODES} --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
// Restart=on-failure
//
// [Install]
// WantedBy=multi-user.target
//
//  COMMAND: sudo systemctl daemon-reload
//  COMMAND: sudo systemctl enable celery.service
//  COMMAND: sudo systemctl restart celery.service
//
//
// 6.5) Now we can create the "celerybeat.service":
//
//  COMMAND: sudo nano /etc/systemd/system/celerybeat.service
//
// ********** /etc/systemd/system/celerybeat.service **********
// [Unit]
// Description=Celery Beat Service
// After=network.target
//
// [Service]
// Type=simple
// User=celery
// Group=celery
// EnvironmentFile=/home/jorge/mysocialdistanceworkdir/socialdistancework/settings.py
// WorkingDirectory=/home/jorge/mysocialdistanceworkdir
// ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat --pidfile=${CELERYBEAT_PID_FILE} --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYBEAT_LOG_LEVEL} ${CELERYBEAT_OPTS}'
// Restart=on-failure
//
// [Install]
// WantedBy=multi-user.target
//
//  COMMAND: sudo systemctl daemon-reload
//  COMMAND: sudo systemctl enable celerybeat.service
//  COMMAND: sudo systemctl restart celerybeat.service