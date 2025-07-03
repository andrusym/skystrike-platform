module.exports = {
  apps: [
    {
      name: "skystrike-api",
      script: "uvicorn",
      args: "main:app --host 0.0.0.0 --port 8000",
      interpreter: "none",
      cwd: "./backend",
      watch: false
    },
    {
      name: "skystrike-frontend",
      script: "node_modules/vite/bin/vite.js",
      args: "preview --port 4173",
      cwd: "./frontend",
      interpreter: "node",
      watch: false
    }
  ]
};
