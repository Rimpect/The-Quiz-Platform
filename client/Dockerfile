FROM node:20-slim AS build

WORKDIR /app

# Только package.json (без lock-файла) — иначе всплывает баг npm с нативными
# бинарниками rollup (Cannot find module .../rollup/dist/native.js).
COPY package.json ./
RUN npm install

COPY . .
ARG VITE_BASE=/
RUN VITE_BASE=$VITE_BASE npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
