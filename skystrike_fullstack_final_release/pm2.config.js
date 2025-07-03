module.exports = {
  apps: [
    {
      name: "skystrike-backend",
      script: "main.py",
      cwd: "./backend",
      interpreter: "python3",
      env: {
        ENV: "production",
        PORT: 8000
      }
    },
    {
      name: "skystrike-frontend",
      script: "npx",
      args: "serve -s dist -l 5173",
      cwd: "./frontend",
      env: {
        NODE_ENV: "production"
      }
    }
  ]
}