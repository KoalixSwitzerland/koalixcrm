FROM nginx:1.11

# Add start script
ADD ./projectsettings/services/webserver/config/start.sh /
RUN chmod +x start.sh

# Add nginx config file
ADD ./projectsettings/services/webserver/config/nginx.tmpl /

# Add SSL certs to location specified in nginx.conf
ADD ./projectsettings/services/webserver/config/*.crt /etc/ssl/certs/
ADD ./projectsettings/services/webserver/config/*.key /etc/ssl/private/

# Execute start script
CMD ["./start.sh"]
