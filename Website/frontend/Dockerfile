FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci --no-audit --no-fund

COPY . .
RUN npm run build

FROM nginx:1-alpine-slim

RUN apk add --no-cache gettext openssl

COPY nginx.conf /etc/printnet/nginx.conf.template
COPY runtime-config.template.js /etc/printnet/runtime-config.js.template
COPY docker-entrypoint.d/30-printnet-runtime.sh /docker-entrypoint.d/30-printnet-runtime.sh
COPY --from=build /app/dist /usr/share/nginx/html
RUN chmod +x /docker-entrypoint.d/30-printnet-runtime.sh

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
