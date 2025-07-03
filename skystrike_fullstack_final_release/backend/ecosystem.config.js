module.exports = {
  apps: [
    {
      name: "skystrike-api",
      script: "uvicorn",
      args: "main:app --host 0.0.0.0 --port 8000",
      interpreter: "./venv/bin/python3",
      cwd: "/home/ubuntu/skystrike_fullstack_final_release/backend",
      env: {
        PYTHONPATH: ".",
      },
    },
  ],
};
