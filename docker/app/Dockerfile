FROM node:22 AS base

ARG NODE_ENV=""
ARG TZ="Asia/Tokyo"

ENV NODE_ENV=${NODE_ENV}
ENV TZ=${TZ}
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

# ビルドだけ
FROM base AS build

RUN mkdir -p /app/.next

WORKDIR /app
COPY --chown=node:node /sns-dark-history ./sns-dark-history
COPY --from=base --chown=node:node /app/sns-dark-history/node_modules /app/sns-dark-history/node_modules
WORKDIR /app/sns-dark-history

RUN npm run build

# 本番環境
FROM base AS production

USER node
WORKDIR /app/sns-dark-history

ARG NODE_ENV=production
COPY --chown=node:node --from=build /app/sns-dark-history/.next ./.next
COPY --chown=node:node --from=build /app/sns-dark-history/public ./public
COPY --chown=node:node --from=build /app/sns-dark-history/next.config.ts ./next.config.ts
COPY --chown=node:node --from=build /app/sns-dark-history/package.json ./package.json
COPY --chown=node:node --from=build /app/sns-dark-history/node_modules ./node_modules
CMD ["npm", "start"]
