FROM node:16-alpine
RUN npm install -g http-server
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install -g --unsafe-perm=true --allow-root
RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache
RUN mkdir -p node_modules/.vite && chmod -R 777 node_modules/.vite
COPY ./ /usr/src/app/
