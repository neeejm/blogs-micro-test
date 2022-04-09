FROM node:16.14-alpine

WORKDIR /app

RUN npm install yarn
COPY package.json .
COPY yarn.lock .
RUN yarn install --forzen-lockfile
COPY . .

CMD ["yarn", "start"]