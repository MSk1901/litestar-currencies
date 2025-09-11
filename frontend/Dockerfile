FROM node:20-alpine AS builder

WORKDIR /app

COPY nuxt-app/package*.json ./
COPY nuxt-app/ ./

RUN npm install
RUN npm run build

FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app ./

ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "run", "start"]