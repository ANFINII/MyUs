FROM node:20-alpine
RUN corepack enable
WORKDIR /frontend
COPY . .
RUN pnpm install --frozen-lockfile
RUN pnpm run build
