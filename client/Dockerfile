FROM node:19.3.0-alpine3.17
WORKDIR /app

COPY package*.json ./

RUN npm install --dev
RUN npm i d3 @turf/turf

COPY . .

EXPOSE 8000
CMD npm run dev