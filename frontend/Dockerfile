FROM nginx:alpine

# Copy the HTML file to nginx default location
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
