# Use official nginx image
FROM nginx:stable-alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy our custom nginx config
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy static website into nginx html folder
COPY static/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start nginx (default command from base image is fine)
CMD ["nginx", "-g", "daemon off;"]
