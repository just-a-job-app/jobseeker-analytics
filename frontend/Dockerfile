# Dockerfile
FROM node:20 AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Clean npm cache and install with exact versions
RUN npm cache clean --force
RUN npm install

# Copy source files
COPY . .

# Accept build arguments for Next.js environment variables
# In production / non-local environments, ARGS are overwritten in action.yaml from GitHub secrets
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ARG NEXT_PUBLIC_APP_URL=http://localhost:3000

# Set build-time environment variables
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV NEXT_PUBLIC_APP_URL=${NEXT_PUBLIC_APP_URL}

RUN npm run build

# Production image
FROM node:20-slim

WORKDIR /app

# Copy standalone output and required files
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

ENV NODE_ENV=production
EXPOSE 3000

# Change the start command to use the standalone server
CMD ["node", "server.js"]