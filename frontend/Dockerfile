# Step 1: Build the Vue app
FROM node:20 AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

ARG VITE_API_BASE_URL
ARG VITE_BASE_URL

RUN echo "VITE_API_BASE_URL=${VITE_API_BASE_URL}" > .env && \
    echo "VITE_BASE_URL=${VITE_BASE_URL}" >> .env && \
    npm run build

FROM nginx:latest

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80