FROM nginx:alpine

# Копирование конфигурации nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копирование скрипта ожидания
COPY wait-for-web.sh /wait-for-web.sh
RUN chmod +x /wait-for-web.sh

# Указание entrypoint
ENTRYPOINT ["/wait-for-web.sh"]
CMD ["nginx", "-g", "daemon off;"]