# Use an official Nginx runtime as a parent image
FROM nginx:1.21.3

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Add our custom Nginx configuration file
ADD nginx.conf /etc/nginx/conf.d/
