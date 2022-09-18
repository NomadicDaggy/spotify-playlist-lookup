# Build step #1: build the React front end
FROM node:16-alpine as build-step
WORKDIR /usr/src/app
ENV PATH /node_modules/.bin:$PATH
COPY package.json yarn.lock /usr/src/app/
COPY ./src /usr/src/app/src
COPY ./public /usr/src/app/public
RUN yarn install

# RUN yarn build
# For production
# Build step #2: build an nginx container
#FROM nginx:stable-alpine
#COPY --from=build-step /usr/src/app/build /usr/share/nginx/html
#COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf