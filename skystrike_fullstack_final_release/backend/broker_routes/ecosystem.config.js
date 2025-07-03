module.exports = {
  apps: [
    {
      name: "skystrike-api",
      script: "uvicorn",
      args: "main:app --host 0.0.0.0 --port 8000",
      interpreter: "python3",
      env: {
        NODE_ENV: "production",
        TRADIER_ACCESS_TOKEN: process.env.TRADIER_ACCESS_TOKEN,
        ACCOUNT_ID: process.env.ACCOUNT_ID,
      },
    },
  ],
};
