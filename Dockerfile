# Multi-stage build for wedding save-the-date website
# Stage 1: Node.js for processing/compression if needed
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files if they exist (for future npm dependencies)
# COPY package*.json ./
# RUN npm ci --only=production || true

# Copy all source files
COPY . .

# If you need to run the compression script during build, uncomment:
# RUN node compress-images.js || true

# Stage 2: Nginx for serving static content
FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy custom nginx configuration
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index save-the-date.html index.html; \
    \
    location / { \
        try_files $uri $uri/ /save-the-date.html; \
        add_header Cache-Control "public, max-age=3600"; \
    } \
    \
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ { \
        expires 7d; \
        add_header Cache-Control "public, immutable"; \
    } \
    \
    gzip on; \
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript; \
    gzip_min_length 1000; \
}' > /etc/nginx/conf.d/default.conf

# Copy static files from builder
COPY --from=builder /app/save-the-date.html /usr/share/nginx/html/
COPY --from=builder /app/save-the-date.html /usr/share/nginx/html/index.html
COPY --from=builder /app/*.jpg /usr/share/nginx/html/
COPY --from=builder /app/originals_backup /usr/share/nginx/html/originals_backup/

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]