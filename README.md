R-verifier
==========
A Linux based verifier for the R language.  This project allows R code to be submitted to the web server via POST and allows the output to be verified and tested.  This project is intended for an open lab setting as a public computing appliance.

Installation Instructions
-------------------------
To install this project on Amazon's Elastic Computing Cloud (EC2), perform these steps:

1. Launch new Ubuntu 12.04 image
2. Connect via SSH using public/private keys
3. Install neccessary packages with: sudo apt-get install nginx r-base-core python-setuptools git-core
4. Install web.py python package: sudo easy_install web.py
5. Get latest assets: git clone git://github.com/jpelster/R-verifier.git
6. Copy config for nginx: sudo cp R-verifier/conf/nginx/default /etc/nginx/sites-available/default
7. Make working directory: mkdir /tmp/R-verifier
8. Update perms: chmod 777 /tmp/R-verifier
9. Change group: sudo chgrp www-data /tmp/R-verifier
10. Make sure group can always read: chmod g+s /tmp/R-verifier
11. Restart nginx: service nginx restart
12. Start R backend server: cd R-verifier; nohup python R-verifier.py > /tmp/R-verifier.log 2>&1 &
13. Load public URL in browser:  [example: http://ec2-aa-bb-ccc-ddd.compute-1.amazonaws.com]
14. Have fun!

Known Issues
------------

If left unchecked, the /tmp partition will get full.  A cron job that regularly deletes old files will be neccesary to prevent this problem.
