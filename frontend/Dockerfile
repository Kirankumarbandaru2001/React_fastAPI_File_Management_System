FROM node:16

WORKDIR /app

COPY ./src /app/src
COPY ./public /app/public
COPY ./package.json /app/package.json

RUN npm install

CMD ["npm", "start"]
