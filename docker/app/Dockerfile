FROM node:22 AS base

ARG NODE_ENV=""
ARG TZ="Asia/Tokyo"
ARG S3_ACCESS_KEY_ID=""
ARG S3_SECRET_ACCESS_KEY=""
ARG S3_BUCKET_NAME=""
ARG S3_BUCKET_URL=""
ARG S3_API_ENDPOINT=""

ENV NODE_ENV=${NODE_ENV}
ENV TZ=${TZ}
ENV S3_ACCESS_KEY_ID=${S3_ACCESS_KEY_ID}
ENV S3_SECRET_ACCESS_KEY=${S3_SECRET_ACCESS_KEY}
ENV S3_BUCKET_NAME=${S3_BUCKET_NAME}
ENV S3_BUCKET_URL=${S3_BUCKET_URL}
ENV S3_API_ENDPOINT=${S3_API_ENDPOINT}

USER node
WORKDIR /app

RUN mkdir -p /app/sns-dark-history
COPY --chown=node:node ./sns-dark-history/package.json ./sns-dark-history/

WORKDIR /app/sns-dark-history
RUN npm install

# 開発環境
FROM base AS development

USER node
WORKDIR /app

COPY --chown=node:node /sns-dark-history ./sns-dark-history
COPY --from=base --chown=node:node /app/sns-dark-history/node_modules ./sns-dark-history
WORKDIR /app/sns-dark-history

CMD ["npm", "run", "dev"]

# 本番環境
FROM base AS production

USER node
WORKDIR /app/sns-dark-history

COPY --chown=node:node /sns-dark-history ./sns-dark-history
COPY --from=base --chown=node:node /app/sns-dark-history/node_modules ./sns-dark-history
RUN npm run build
CMD ["npm", "start"]
