# Build the React frontend from the repository root
FROM node:22-alpine AS frontend-build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY src ./src
COPY public ./public
COPY index.html ./
COPY vite.config.js ./
RUN npm run build

# Run the Python API
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NIGHT_HUNTER_RUNTIME=cloud

COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

COPY . ./
COPY --from=frontend-build /app/dist ./frontend/dist

EXPOSE 8000

CMD ["sh", "-c", "waitress-serve --listen=0.0.0.0:${PORT:-8000} api.server:app"]
