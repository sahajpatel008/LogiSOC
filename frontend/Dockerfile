FROM node:18.20.5-alpine AS build

WORKDIR /app

ARG VITE_BASE_URL
ARG VITE_CLERK_PUBLISHABLE_KEY

ENV VITE_BASE_URL=$VITE_BASE_URL
ENV VITE_CLERK_PUBLISHABLE_KEY=$VITE_CLERK_PUBLISHABLE_KEY

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./

RUN npm run build


FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
