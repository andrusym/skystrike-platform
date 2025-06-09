module.exports = {
  apps: [
    {
      name: 'skystrike-backend',
      script: './backend/server.js',
      watch: true,
      env: {
        PORT: 3001,
        TRADIER_TOKEN: 'your_token_here',
        TRADIER_BASE_URL: 'https://sandbox.tradier.com/v1/markets',
        ACCOUNT_MODE: 'paper'
      }
    }
  ]
};