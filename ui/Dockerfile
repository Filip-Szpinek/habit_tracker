# syntax=docker/dockerfile:1

ARG NODE_VERSION=22.20.0
FROM node:${NODE_VERSION}-alpine

# Use development environment
ENV NODE_ENV=development

WORKDIR /usr/src/app

# Install dependencies with cache mounts
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --include=dev

# Install nodemon (optional, for extra hot reload scripts)
RUN npm install -g nodemon

# Copy all files
COPY ../svelteUI .

# Non-root user
RUN chown -R node /usr/src/app
USER node

# Expose Vite dev server port
EXPOSE 5173

# Run SvelteKit dev server accessible from outside container
CMD ["npm", "run", "dev", "--", "--host"]
