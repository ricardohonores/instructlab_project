FROM nginx:alpine

# Copiar archivo HTML
COPY index.html /usr/share/nginx/html/

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto
EXPOSE 80

# Nginx inicia automáticamente
