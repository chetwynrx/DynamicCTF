FROM php:8.0-apache

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

RUN apt-get update && apt-get install -y python3-dev python3-pip
RUN apt-get update -y
RUN apt-get install nano
RUN apt-get install -y default-libmysqlclient-dev
RUN pip3 install pyyaml
RUN pip3 install requests
RUN pip3 install pypika 
RUN pip3 install mysqlclient
RUN pip3 install Faker
run pip3 install mysql-connector-python

COPY ./sql_gen.py /etc/test.py
COPY ./classicmodels.sql /var/www/html
COPY ./example.sql /var/www/html
RUN chmod 777 -R /var/www/html
#RUN chown 777 -R www-data:www-data /etc/test.py
RUN chmod +x /etc/test.py

#RUN sed -i 's/;html_errors = On/html_errors = On/g' /usr/local/etc/php/php.ini
#RUN sed -i 's/display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.ini
#RUN sed -i 's/;display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.ini

#COPY sql_gen.py /var/www/html/test.py
#RUN usermod -a -G www-data root
#RUN chown -R www-data:www-data /var/www/html
#RUN chown -R www-data:www-data /var/www/html/
#RUN chmod +x www-data:www-data /var/www/html/sql_gen.py
#RUN chown 777 -R /var/www/html/
#RUN chmod +x /var/www/html/sql_gen.pyRUN sed -i 's/;html_errors = On/html_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/;display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/;html_errors = On/html_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/;display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/;html_errors = On/html_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/;display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/;html_errors = On/html_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/;display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.iniRUN sed -i 's/;html_errors = On/html_errors = On/g' /usr/local/etc/php/php.ini
#RUN sed -i 's/;html_errors = On/html_errors = On/g' /usr/local/etc/php/php.ini
#RUN sed -i 's/display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.ini
