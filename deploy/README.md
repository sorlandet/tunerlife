automobile
==========

======== Installing lxml [3.1.1] ===============================================

http://lxml.de/installation.html

yum install -y libxml2 libxml2-devel
yum install -y libxslt libxslt-devel

pip install lxml



======== Installing pycurl [7.19.0] ============================================

http://pycurl.sourceforge.net/
http://stackoverflow.com/questions/7391638/pycurl-installed-but-not-found

pycurl.so to be built and copied to the site-packages

yum install -y libcurl, libcurl-devel

pip install pycurl


======== Gunicorn issues =======================================================

mkdir /var/run/{projectname}
chown wwwpub:wwwpub /var/run/{projectname}


======== info@wheel-size.com ===================================================
http://mail.yandex.ru/for/wheel-size.com/
имя:
пароль: