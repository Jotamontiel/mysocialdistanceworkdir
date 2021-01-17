def remote = [:]
remote.name = "www.socialdistance.cl"
remote.host = "167.172.149.133"
remote.allowAnyHosts = true

node {
    withCredentials([sshUserPrivateKey(credentialsId: 'the-real-user-for-webserver-1', keyFileVariable: 'WEBSERVER_KEYFILE', passphraseVariable: '', usernameVariable: 'WEBSERVER_USER')]) {
        remote.user = WEBSERVER_USER
        remote.identityFile = WEBSERVER_KEYFILE
        stage("Stage 1: Reset & Update Master Branch") {
            echo "---------------------------------------------------------------------"
            echo "---------------- Reset & Update Master Branch Starting --------------"
            echo "---------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            echo "**********************************************"
            echo "****** Show Base Directory *******************"
            echo "**********************************************"
            pwd
            ls -al
            echo "**********************************************"
            echo "****** Show Project Sub Directory ************"
            echo "**********************************************"
            cd mysocialdistanceworkdir
            pwd
            ls -al
            git reset --hard
            git pull origin main
            pwd
            ls -al
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Master Branch Reset and Updated ---------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 2: Clear Static & Media Files") {
            echo "---------------------------------------------------------------------"
            echo "---------------- Clear Static & Media Files Starting ----------------"
            echo "---------------------------------------------------------------------"
            sshCommand remote: remote, command: """
            echo "**********************************************"
            echo "****** Show Base Directory *******************"
            echo "**********************************************"
            pwd
            ls -al
            echo "**********************************************"
            echo "****** Show Project Sub Directory ************"
            echo "**********************************************"
            cd mysocialdistanceworkdir
            pwd
            ls -al
            sudo rm -r media
            sudo rm -r static
            sudo rm -r sent_emails
            """
            echo "----------------------------------------------------------------------"
            echo "---------------- Directory cleaned -----------------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 3: Create Virtual Environment") {
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
        stage("Stage 4: Database Reset") {
            echo "----------------------------------------------------------------------"
            echo "---------------- Database Reset Starting -----------------------------"
            echo "----------------------------------------------------------------------"
            sshCommand remote: remote, command: """
                sudo -h 167.172.149.133 -u postgres bash -c "psql -f queries.sql"
                """
            echo "----------------------------------------------------------------------"
            echo "---------------- Database Built --------------------------------------"
            echo "----------------------------------------------------------------------"
        }
        stage("Stage 5: Build Migrations & Migrate") {
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
        stage("Stage 6: Static Files Collection"){
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
        stage("Stage 7: Create Superuser"){
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
        stage("Stage 8: Restart Services"){
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
//  COMMAND: sudo nano /etc/systemd/system/celery.service
//
// ********** /etc/systemd/system/celery.service **********
// [Unit]
// Description=Celery Service
// After=network.target
//
// [Service]
// Type=forking
// User=celery
// Group=celery
// EnvironmentFile=/etc/conf.d/celery
// WorkingDirectory=/opt/celery
// ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
//     --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
//     --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
// ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
//     --pidfile=${CELERYD_PID_FILE} --loglevel="${CELERYD_LOG_LEVEL}"'
// ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
//     --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
//     --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
// Restart=always
//
// [Install]
// WantedBy=multi-user.target
//
//  COMMAND: sudo systemctl daemon-reload
//  COMMAND: sudo systemctl enable celery.service
//
//  ATTENTION 1: To configure user, group, chdir change settings: User, Group, and WorkingDirectory defined in /etc/systemd/system/celery.service.
//  ATTENTION 2: You can also use systemd-tmpfiles in order to create working directories (for logs and pid):
// file: /etc/tmpfiles.d/celery.conf
//  d /var/run/celery 0755 celery celery -
//  d /var/log/celery 0755 celery celery -
//
//  COMMAND: sudo nano /etc/conf.d/celery
//
// ********** /etc/conf.d/celery **********
// # Name of nodes to start
// # here we have a single node
// CELERYD_NODES="w1"
// # or we could have three nodes:
// #CELERYD_NODES="w1 w2 w3"
//
// # Absolute or relative path to the 'celery' command:
// CELERY_BIN="/usr/local/bin/celery"
// #CELERY_BIN="/virtualenvs/def/bin/celery"
//
// # App instance to use
// # comment out this line if you don't use an app
// CELERY_APP="proj"
// # or fully qualified:
// #CELERY_APP="proj.tasks:app"
//
// # How to call manage.py
// CELERYD_MULTI="multi"
//
// # Extra command-line arguments to the worker
// CELERYD_OPTS="--time-limit=300 --concurrency=8"
//
// # - %n will be replaced with the first part of the nodename.
// # - %I will be replaced with the current child process index
// #   and is important when using the prefork pool to avoid race conditions.
// CELERYD_PID_FILE="/var/run/celery/%n.pid"
// CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
// CELERYD_LOG_LEVEL="INFO"
//
// # you may wish to add these options for Celery Beat
// CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
// CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"
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
// EnvironmentFile=/etc/conf.d/celery
// WorkingDirectory=/opt/celery
// ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat  \
//     --pidfile=${CELERYBEAT_PID_FILE} \
//     --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
// Restart=always
//
// [Install]
// WantedBy=multi-user.target
//
//  COMMAND: sudo systemctl daemon-reload
//  COMMAND: sudo systemctl enable celerybeat.service
//