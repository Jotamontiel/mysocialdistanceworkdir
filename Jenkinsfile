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
        stage("Stage 2: Create Virtual Environment") {
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
        stage("Stage 3: Database Reset") {
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
        stage("Stage 4: Build Migrations & Migrate") {
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
        stage("Stage 5: Static Files Collection"){
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
        stage("Stage 6: Create Superuser"){
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
        stage("Stage 7: Restart Services"){
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