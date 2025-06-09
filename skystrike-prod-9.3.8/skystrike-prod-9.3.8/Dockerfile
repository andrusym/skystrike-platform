# SkyStrike Frontend Build (corrected for frontend folder)
FROM node:18

WORKDIR /app

COPY frontend/ /app/

RUN npm install
RUN npm run build

RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "8501"]
