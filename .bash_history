unzip dashboard_main_v6_1.zip -o
unzip core_app_full_v3.zip -o
unzip utils_config_full_v3.zip -o
unzip ui_assets_full_v3.zip -o
unzip data_and_logs_full_v3.zip -o
unzip auth_system_full_v6_1.zip -o
unzip tradier_executor_full_v6_1.zip -o
unzip dashboard_main_v6_1.zip -o
unzip login_ui_full_v6_1_1.zip -o
pwd
ls *.zip
unzip core_app_full_v3.zip -o
unzip utils_config_full_v3.zip -o
unzip ui_assets_full_v3.zip -o
unzip data_and_logs_full_v3.zip -o
unzip auth_system_full_v6_1.zip -o
unzip tradier_executor_full_v6_1.zip -o
unzip dashboard_main_v6_1.zip -o
unzip login_ui_full_v6_1_1.zip -o
unzip core_app_full_v3.zip -o
unzip -o core_app_full_v3.zip
unzip -o utils_config_full_v3.zip
unzip -o ui_assets_full_v3.zip
unzip -o data_and_logs_full_v3.zip
unzip -o auth_system_full_v6_1.zip
unzip -o tradier_executor_full_v6_1.zip
unzip -o dashboard_main_v6_1.zip
unzip -o login_ui_full_v6_1_1.zip
streamlit run main.py
pip install streamlit
streamlit run main.py
cd ~/skystrike-phase1
ls
unzip -o dashboard_main_v6_1.zip
ls theme.css skystrike_logo.png dashboard_layout.md
unzip -o ui_assets_full_v3.zip
streamlit run main.py
bash deploy_skystrike.sh
cd ~/skystrike-phase1
git add ml.py
git commit -m "Backup: Local edits to ml.py before merge"
#!/bin/bash
cd ~/skystrike-phase1
echo "🔄 Unzipping latest modules..."
unzip -o core_app_full_v3.zip
unzip -o utils_config_full_v3.zip
unzip -o ui_assets_full_v3.zip
unzip -o data_and_logs_full_v3.zip
unzip -o auth_system_full_v6_1.zip
unzip -o tradier_executor_full_v6_1.zip
unzip -o dashboard_main_v6_1.zip
unzip -o login_ui_full_v6_1_1.zip
echo "📦 Installing dependencies..."
pip install -r requirements.txt || pip install streamlit pandas numpy requests altair
echo "🚀 Launching SkyStrike with modern UI..."
streamlit run main.py
chmod +x deploy_skystrike.sh
./deploy_skystrike.sh
cd ~/skystrike-phase1
git fetch origin
git reset --hard origin/main
./deploy_skystrike.sh
nano deploy_skystrike.sh
chmod +x deploy_skystrike.sh
./deploy_skystrike.sh
docker ps
docker ps -a
docker logs skystrike-prod
docker build -t skystrike-app .
docker rm skystrike-prod
docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app
docker ps
docker exec -it skystrike-prod bash
docker logs skystrike-prod
docker rm -f skystrike-prod
docker build -t skystrike-app .
docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app
cd ~/skystrike-phase1
# Optional: Backup your current state
mkdir ../skystrike_backup
cp -r * ../skystrike_backup/
# Clean up all previous code, zips, and failed runs
rm -rf *.zip __pycache__ *.py *.json *.csv *.txt *.md *.css *.png utils auth *.log .env venv docker-compose.yml
# Remove any stopped or exited containers
docker rm -f $(docker ps -aq)
# Remove old images if needed (optional)
docker image prune -a -f
unzip -o skystrike_v6_1_2_core.zip
docker rm -f skystrike-prod
docker rmi skystrike-app
docker build -t skystrike-app .
docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app
cat <<EOF > .env
TRADIER_API_TOKEN=your_tradier_token_here
MODE=paper
USERNAME_PASSWORD_SECRET=replace_with_strong_key
DEPLOY_ENV=prod
EOF

docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app
unzip skystrike_v7_full_release.zip
cd skystrike-v7/
cd backend/
pip install -r requirements.txt  # if not yet done
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fastapi
uvicorn
python-dotenv
numpy
echo -e "fastapi\nuvicorn\npython-dotenv\nnumpy" > requirements.txt
pip install -r requirements.txt
pip install uvicorn
# or if using apt:
sudo apt install uvicorn
sudo apt autoremove -y
sudo apt clean
sudo apt autoclean
pip cache purge
du -sh * | sort -h
unzip -o skystrike_v7_full_release.zip -d skystrike-v7
cd skystrike-v7/
cd ..
ls -lh skystrike_v7_full_release.zip
unzip -o skystrike_v7_full_release.zip -d skystrike-v7
cd skystrike-v7/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
cd ..
ls -lh skystrike_v7_full_release.zip
~/skystrike-phase1/
cd ~/skystrike-phase1
ls -lh skystrike_v7_full_release.zip
unzip -o skystrike_v7_full_release.zip -d skystrike-v7
cd skystrike-v7/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
mkdir -p backend/utils
mv backend/option_chain.py backend/utils/
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
ModuleNotFoundError: No module named 'utils'
backend/option_chain.py
from utils.option_chain import get_option_chain
ls -l option_chain.py
nano strategy_engine.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
nano strategy_engine.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
cd ~/skystrike-phase1/skystrike-v7/frontend
npm install
sh ../deploy/deploy_frontend.sh
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
cd ~/skystrike-phase1/skystrike-v7/frontend
sh ../deploy/deploy_frontend.sh
cd ../deploy
npm install
cd ~/skystrike-phase1/skystrike-v7/frontend
ls
cd ~/skystrike-phase1/skystrike-v7/frontend
npm install
npm run dev
cd ~/skystrike-phase1/skystrike-v7/
unzip -o /mnt/data/skystrike_frontend_v7_rebuild.zip -d frontend/
cd frontend
npm install
npm run dev
cp /mnt/data/skystrike_frontend_v7_rebuild.zip ./ && unzip -o skystrike_frontend_v7_rebuild.zip -d .
npm error path /home/ubuntu/skystrike-phase1/skystrike-v7/frontend/package.json
find ~/skystrike-phase1/skystrike-v7 -name package.json
~/skystrike-phase1/skystrike-v7/frontend/skystrike-ui/package.json
mv ~/skystrike-phase1/skystrike-v7/frontend/skystrike-ui/* ~/skystrike-phase1/skystrike-v7/frontend/
cd ~/skystrike-phase1/skystrike-v7/frontend
rm -rf *
unzip /mnt/data/skystrike_frontend_v7_rebuild.zip -d .
ls
npm install
cd ~/skystrike-phase1/skystrike-v7/frontend
rm -rf *
unzip /mnt/data/skystrike_frontend_v7_rebuild.zip -d .
ls
npm install
cp /mnt/data/skystrike_frontend_v7_rebuild.zip ~/skystrike-phase1/skystrike-v7/frontend/
npm install
npm run dev
cd ~/skystrike-phase1/skystrike-v7/frontend
unzip -o skystrike_frontend_v7_rebuild.zip -d .
find ~/skystrike-phase1/skystrike-v7 -name "skystrike_frontend_v7_rebuild.zip"
mv /mnt/data/skystrike_frontend_v7_rebuild.zip ~/skystrike-phase1/skystrike-v7/frontend/
cd ~/skystrike-phase1/skystrike-v7/frontend
unzip -o skystrike_frontend_v7_rebuild.zip -d .
npm install
npm run dev
cd ~/skystrike-phase1/skystrike-v7/frontend
npm install
curl -o package.json https://sandbox.openai.com/sandbox/skystrike_v7_frontend_fixes/package.json
ls -l package.json
~/skystrike-phase1/skystrike-v7/frontend/
cd ~/skystrike-phase1/skystrike-v7/frontend
npm install
npm run dev
cp /mnt/data/package.json ~/skystrike-phase1/skystrike-v7/frontend/
ls -l ~/skystrike-phase1/skystrike-v7/frontend/package.json
mv ~/Downloads/package.json ~/skystrike-phase1/skystrike-v7/frontend/
cd ~/skystrike-phase1/skystrike-v7/frontend
npm install
npm run dev
cp /mnt/data/package.json ~/skystrike-phase1/skystrike-v7/frontend/
ls -l ~/skystrike-phase1/skystrike-v7/frontend/package.json
cd ~/skystrike-phase1/skystrike-v7/frontend
npm install
npm run dev
scp /path/to/package.json ubuntu@<your-server-ip>:~/skystrike-phase1/skystrike-v7/frontend/
cd ~/skystrike-phase1/skystrike-v7/frontend
wget https://sandbox.openai.com/attachments/34a4ed2c-39f1-41c2-88d4-8163d3b1c64b/package.json
ls -l ~/skystrike-phase1/skystrike-v7/frontend/package.json
scp /path/to/package.json ubuntu@<YOUR_SERVER_IP>:~/skystrike-phase1/skystrike-v7/frontend/
cd ~
mkdir skystrike-deploy && cd skystrike-deploy
# Upload ZIP here
unzip skystrike_v7_full.zip
chmod +x install.sh
./install.sh
cd ~
mkdir -p skystrike-v7
cd skystrike-v7
~/skystrike-v7/skystrike_v7_lightsail_full.zip
cd ~/skystrike-phase1
unzip skystrike_v7_lightsail_full.zip -d .
chmod +x start.sh
./start.sh
ls -l ~/skystrike-phase1/frontend
cd ~/skystrike-phase1/frontend
npm install
npm run dev
VITE vX.X.X  ready in Xs
npm uninstall next
cat package.json
npm run dev
nano package.json
rm -rf node_modules package-lock.json
npm install
npm run dev
npm install --save-dev @vitejs/plugin-react
npm run dev
npm run dev -- --host
npm install -g pm2
npm run build
pm2 start npm --name skystrike-frontend -- start
http://<your-lightsail-public-ip>:3000/
cd ~/skystrike-phase1/backend
pm2 start main.py --interpreter python3 --name skystrike-backend
pm2 startup
pm2 save
sudo npm install -g pm2
cd ~/skystrike-phase1/frontend
npm run build
pm2 start npm --name skystrike-frontend -- start
pm2 list
cd ~/skystrike-phase1/backend
pm2 start main.py --interpreter python3 --name skystrike-backend
pm2 startup
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u ubuntu --hp /home/ubuntu
pm2 save
pm2 delete skystrike-frontend
{   "name": "skystrike-frontend",;   "version": "1.0.0",;   "scripts": {;     "dev": "vite",;     "build": "vite build",;     "preview": "vite preview";   },;   "dependencies": {;     "react": "^18.2.0",;     "react-dom": "^18.2.0";   },;   "devDependencies": {;     "vite": "^5.0.0",;     "@vitejs/plugin-react": "^4.0.0";   }
}
npm install vite @vitejs/plugin-react --save-dev
npm run build
npm run preview
pm2 start npm --name skystrike-frontend -- run preview
cd ~/skystrike-phase1/frontend
npm install
npm run build
cd ~/skystrike-phase1
rm -rf frontend
npx create-vite@latest frontend --template react
cd frontend
npm install
{   "name": "skystrike-frontend",;   "version": "1.0.0",;   "private": true,;   "scripts": {;     "dev": "vite",;     "build": "vite build",;     "preview": "vite preview";   },;   "dependencies": {;     "react": "^18.2.0",;     "react-dom": "^18.2.0";   },;   "devDependencies": {;     "@vitejs/plugin-react": "^4.0.0",;     "vite": "^5.0.0";   }
}
npm run build
npm run preview
npm run preview -- --host
npm run preview -- --host 0.0.0.0
~/skystrike-phase1/frontend/src/
npm run build
npm run preview -- --host 0.0.0.0
pm2 delete skystrike-frontend
pm2 start npm --name skystrike-frontend -- run preview -- --host 0.0.0.0
pm2 save
http://3.149.137.243:8000/docs
cd ~/skystrike-phase1/backend
pm2 delete skystrike-backend
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --interpreter python3 --name skystrike-backend
pm2 save
cd ~/skystrike-phase1/frontend
npm run build
pm2 delete skystrike-frontend
pm2 start npm --name skystrike-frontend -- run preview -- --host 0.0.0.0
pm2 save
pm2 list
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --interpreter python3 --name skystrike-backend
cd ~/skystrike-phase1/backend
pm2 delete skystrike-backend
# ✅ Correct way to run uvicorn via PM2
pm2 start uvicorn --name skystrike-backend --interpreter python3 --   main:app --host 0.0.0.0 --port 8000
pm2 save
pm2 list
pm2 logs skystrike-backend
uvicorn main:app
nano ~/skystrike-phase1/backend/main.py
uvicorn main:app --host 0.0.0.0 --port 8000
pm2 list
pm2 delete skystrike-backend
pm2 start uvicorn --name skystrike-backend --interpreter python3 --cwd $(pwd) --   main:app --host 0.0.0.0 --port 8000
pm2 save
pm2 list
pm2 logs skystrike-backend
nano ~/skystrike-phase1/backend/main.py
pm2 restart skystrike-backend
pm2 logs skystrike-backend
cd ~/skystrike-phase1/frontend/src
ls -l
cd ~/skystrike-phase1
unzip skystrike_frontend_regenerated.zip -d frontend
cd frontend
npm install
npm run build
npm run preview -- --host
lsof -i :4173
kill -9 <PID>
pm2 delete skystrike-frontend
pm2 start npm --name skystrike-frontend -- run preview -- --host 0.0.0.0 --port 4173
pm2 save
unzip /home/ubuntu/skystrike-phase1/frontend/skystrike_real_frontend_ui.zip -d /home/ubuntu/skystrike-phase1/frontend/
cd /home/ubuntu/skystrike-phase1/frontend
rm -rf node_modules package-lock.json
npm install
npm run build
pm2 start npm --name skystrike-frontend -- run preview -- --host 0.0.0.0 --port 4173
pm2 save
cd ~/skystrike-phase1
unzip -o skystrike_real_frontend_ui.zip -d frontend/
cd frontend
rm -rf node_modules package-lock.json dist
npm install
npm run build
pm2 delete skystrike-frontend
pm2 start npm --name skystrike-frontend -- run preview -- --host 0.0.0.0 --port 4173
pm2 save
cd ~/skystrike-phase1/frontend
unzip skystrike_v7_frontend_ui_final.zip -d .
rm -rf node_modules package-lock.json
npm install
npm run build
pm2 delete skystrike-frontend
pm2 start npm --name skystrike-frontend -- run preview -- --host 0.0.0.0 --port 4173
pm2 save
unzip -o skystrike_v7_frontend_ui_final.zip -d .
pm2 delete skystrike-frontend
rm -rf dist
npm run build
pm2 start npm --name skystrike-frontend -- run preview -- --host 0.0.0.0 --port 4173
pm2 save
#!/bin/bash
echo "🔧 Stopping and removing existing SkyStrike containers..."
docker ps -a | grep skystrike | awk '{print $1}' | xargs -r docker stop
docker ps -a | grep skystrike | awk '{print $1}' | xargs -r docker rm
echo "🧼 Removing old SkyStrike Docker images (optional)..."
docker images | grep skystrike | awk '{print $3}' | xargs -r docker rmi -f
echo "🗑️  Cleaning up old deployment directories..."
rm -rf /home/ubuntu/skystrike
mkdir -p /home/ubuntu/skystrike
chown ubuntu:ubuntu /home/ubuntu/skystrike
echo "✅ SkyStrike Phase 1 cleaned. Ready for v8.3 upload."
# List folders & files by size, newest first
ls -lhtr /home/ubuntu
# Check old docker containers/images
docker ps -a
docker images
#!/bin/bash
echo "🗑️ Removing old SkyStrike build folders and cache..."
rm -rf /home/ubuntu/skystrike_phase1_build_v1.0.1.zip
rm -rf /home/ubuntu/__pycache__
rm -rf /home/ubuntu/skystrike_backup
rm -rf /home/ubuntu/skystrike-deploy
rm -rf /home/ubuntu/skystrike-v7
rm -rf /home/ubuntu/skystrike-phase1
rm -rf /home/ubuntu/skystrike
echo "✅ Old Phase 1

mkdir -p /home/ubuntu/skystrike-v8.3
cd /home/ubuntu/skystrike-v8.3

mkdir -p /home/ubuntu/skystrike-v8.3
cd /home/ubuntu/skystrike-v8.3
mv /home/ubuntu/skystrike_v8.2_final_fixed.zip /home/ubuntu/skystrike-v8.3/
cd /home/ubuntu/skystrike-v8.3
unzip skystrike_v8.2_final_fixed.zip
# Move env to correct place
mv /home/ubuntu/skystrike-v8.3/backend/.env /home/ubuntu/skystrike-v8.3/.env
# Edit and insert your token
nano /home/ubuntu/skystrike-v8.3/.env
# (insert TRADIER_API_TOKEN=VA70062258)
# Start system
cd /home/ubuntu/skystrike-v8.3
docker-compose down
docker-compose up -d --build
# Start system
cd /home/ubuntu/skystrike-v8.3
docker-compose down
docker-compose up -d --build
env file /home/ubuntu/.env not found: stat /home/ubuntu/.env: no such file or directory
ubuntu@ip-172-26-1-2:~/skystrike-v8.3$
sudo rm /home/ubuntu/.env
cd /home/ubuntu/skystrike-v8.3
nano .env
docker-compose down
docker-compose up -d --build
mv /home/ubuntu/skystrike-v8.3/backend/.env /home/ubuntu/skystrike-v8.3/.env
rm -rf /home/ubuntu/skystrike-v8.3
mkdir -p /home/ubuntu/skystrike-v8.3
cd /home/ubuntu/skystrike-v8.3
# 1. Clean and re-extract
rm -rf backend frontend deploy
unzip skystrike_v8.2_final_fixed.zip
# 2. Create a clean .env file
nano .env
docker-compose down
docker-compose up -d --build
cd /home/ubuntu/skystrike-v8.3
unzip skystrike_v8.2_final_fixed.zip
nano .env
ls -l .env
-rw-r--r-- 1 ubuntu ubuntu ... .env
docker-compose down
docker-compose up -d --build
nano docker-compose.yml
# (Paste the full content above)
CTRL+O, ENTER, CTRL+X
docker-compose down
docker-compose up -d --build
ls -l
unzip skystrike_v8.2_final_fixed.zip
skystrike_v8.2_final_fixed.zip
cd /home/ubuntu/skystrike-v8.3
unzip skystrike_v8.2_final_fixed.zip
docker-compose down
docker-compose up -d --build
unzip skystrike_v8.2_final_fixed.zip
Archive:  skystrike_v8.2_final_fixed.zip
ubuntu@ip-172-26-1-2:~/skystrike-v8.3$ docker-compose down
docker-compose up -d --build
[+] Building 0.1s (2/2) FINISHED                                 docker:default
failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory
ubuntu@ip-172-26-1-2:~/skystrike-v8.3$
y
mv ../skystrike_v8.2_final_fixed.zip .
mv /home/ubuntu/skystrike_v8.2_final_fixed.zip /home/ubuntu/skystrike-v8.3/
cd /home/ubuntu/skystrike-v8.3
unzip skystrike_v8.2_final_fixed.zip
a
unzip -o skystrike_v8.2_final_fixed.zip
mv Dockerfile.backend backend/Dockerfile
mv Dockerfile.frontend frontend/Dockerfile
mv /home/ubuntu/skystrike-v8.3/backend/Dockerfile.backend /home/ubuntu/skystrike-v8.3/backend/Dockerfile
mv /home/ubuntu/skystrike-v8.3/frontend/Dockerfile.frontend /home/ubuntu/skystrike-v8.3/frontend/Dockerfile
cd /home/ubuntu/skystrike-v8.3
docker-compose down
docker-compose up -d --build
nano .env
docker ps
ls -l frontend
unzip skystrike_v8.3_final_fixed.zip -o
nano frontend/package.json
# Paste the content above, then:
# CTRL+O → ENTER → CTRL+X
docker-compose down
docker-compose up -d --build
nano package.json
nano vite.config.js
docker build -t skystrike-frontend .
nano Dockerfile
docker build -t skystrike-frontend .
cp public/index.html .
cp src/index.html .
ls index.html
docker build -t skystrike-frontend .
cd ~/skystrike-v8.3/frontend
npm install
ls public/index.html
ls src/App.jsx
npm run build
~/skystrike-v8.3/frontend/public/index.html
ls ~/skystrike-v8.3/frontend/public/index.html
curl -o ~/skystrike-v8.3/frontend/public/index.html https://raw.githubusercontent.com/andrusym/skystrike-phase1/main/frontend/public/index.html
cd ~/skystrike-v8.3/frontend
npm run build
cd ~/skystrike-v8.3/frontend
npm run build
~/skystrike-v8.3/frontend/public/index.html
ls -l ~/skystrike-v8.3/frontend/public/index.html
cd ~/skystrike-v8.3/frontend
npm run build
ls public/index.html
ls src/App.jsx
npm run build
cp public/index.html ./index.html
npm run build
const res = await axios.get(\`\${API_BASE}/dashboard\`);
const res = await axios.get(`${API_BASE}/dashboard`);
npm run build
nano src/App.jsx
npm run build
npm install axios
npm run build
unzip /mnt/data/skystrike_components_bundle.zip -d .
nano src/App.jsx
cd ~/skystrike-v8.3/frontend
docker build -t skystrike-ui .
docker run -d -p 3000:80 --name skystrike-ui-prod skystrike-ui
nano Dockerfile
nano nginx.conf
docker build -t skystrike-ui .
docker run -d -p 3000:80 --name skystrike-ui-prod skystrike-ui
export default {
};
npm run build
docker build -t skystrike-ui .
docker stop skystrike-ui-prod && docker rm skystrike-ui-prod
docker run -d -p 3000:80 --name skystrike-ui-prod skystrike-ui
Run `npm audit` for details.
npm notice
npm notice New major version of npm available! 10.8.2 -> 11.4.1
npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.4.1
npm notice To update run: npm install -g npm@11.4.1
npm notice
Step 5/10 : RUN npm run build
> skystrike-frontend@1.0.0 build
> vite build
vite v4.5.14 building for production...
transforming...
✓ 66 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                0.32 kB │ gzip: 0.24 kB
dist/assets/index-6ed53d3d.js  8.24 kB │ gzip: 3.12 kB
✓ built in 666ms
Step 6/10 : FROM nginx:alpine
Step 7/10 : COPY --from=builder /app/dist /usr/share/nginx/html
Step 8/10 : COPY nginx.conf /etc/nginx/conf.d/default.conf
Step 9/10 : EXPOSE 80
Step 10/10 : CMD ["nginx", "-g", "daemon off;"]
Successfully built 2f1c86995d88
Successfully tagged skystrike-ui:latest
skystrike-ui-prod
24cc5c36cdb645904db7c3d4c780795211ae0f774e4f1832756cf47a636d1600
ubuntu@ip-172-26-1-2:~/skystrike-v8.3/frontend$
npm install
npm run build
docker build -t skystrike-ui .
docker run -d -p 3000:80 --name skystrike-ui-prod skystrike-ui
# Stop and remove the old container
docker stop skystrike-ui-prod
docker rm skystrike-ui-prod
# Now run your new container
docker run -d -p 3000:80 --name skystrike-ui-prod skystrike-ui
# Example if using FastAPI
uvicorn main:app --host 0.0.0.0 --port 8501
curl http://localhost:8501/dashboard
pip install fastapi uvicorn[standard]
uvicorn main:app --host 0.0.0.0 --port 8501
curl http://localhost:8501/dashboard
nano main.py
uvicorn main:app --host 0.0.0.0 --port 8501
curl http://localhost:8501/dashboard
uvicorn main:app --host 0.0.0.0 --port 8501
curl http://localhost:8501/dashboard
uvicorn main:app --host 0.0.0.0 --port 8501
curl http://localhost:8501/dashboard
uvicorn main:app --host 0.0.0.0 --port 8501
curl http://localhost:8501/dashboard
npm run build
cd ~/skystrike-v8.3/frontend
npm install           # only needed once if not done yet
npm run build
cp -r dist/ ~/skystrike-v8.3/backend/app/static
mkdir -p ~/skystrike-v8.3/backend/app/static
uvicorn main:app --host 0.0.0.0 --port 8501
mv ~/skystrike-v8.3/main.py ~/skystrike-v8.3/frontend/main.py
cd ~/skystrike-v8.3/frontend
uvicorn main:app --host 0.0.0.0 --port 8501
nano ~/skystrike-v8.3/frontend/main.py
cd ~/skystrike-v8.3/frontend
uvicorn main:app --host 0.0.0.0 --port 8501
npm install
npm run build
~/skystrike-v8.3/frontend/main.py
chmod +r ~/skystrike-v8.3/frontend/main.py
cd ~/skystrike-v8.3/frontend
uvicorn main:app --host 0.0.0.0 --port 8501
sudo lsof -i :8501
uvicorn main:app --host 0.0.0.0 --port 8501
kill -9 48733
sudo lsof -i :8501
uvicorn main:app --host 0.0.0.0 --port 8501
ps aux | grep uvicorn
unzip skystrike_ui_final_bundle.zip -d skystrike_ui
cd skystrike_ui
ip:  cannot find or open skystrike_ui_final_b
/home/ubuntu/skystrike-v8.3/
├── frontend/
├── backend/
├── ...
├── skystrike_ui_final_bundle.zip   ← (uploaded here)
└── skystrike_ui/                   ← unzip creates this
cd ~/skystrike-v8.3
unzip skystrike_ui_final_bundle.zip -d skystrike_ui
cd skystrike_ui
uvicorn main:app --host 0.0.0.0 --port 8501
cd ~/skystrike-v8.3
mkdir skystrike_ui
mkdir skystrike_ui/dist
cd /home/ubuntu/skystrike-v8.3/skystrike_ui
uvicorn main:app --host 0.0.0.0 --port 8501
/home/ubuntu/skystrike-v8.3/skystrike_ui/
cd ~/skystrike-v8.3/skystrike_ui
unzip -o skystrike_ui_final_bundle.zip -d .
uvicorn main:app --host 0.0.0.0 --port 8501
cd ~/skystrike-v8.3/skystrike_ui
unzip -o skystrike_ui_final_bundle.zip -d .
uvicorn main:app --host 0.0.0.0 --port 8501
nano .env.production
VITE_API_URL=http://3.149.137.243:8501
echo "VITE_API_URL=http://3.149.137.243:8501" > .env.production
cd ~/skystrike-v8.3/frontend
npm run build
cd ~/skystrike-v8.3/frontend
# Build production files (if not already done)
npm run build
# Start the Vite preview server
npx vite preview --host
npm install -g http-server
sudo npm install -g http-server
cd ~/skystrike-v8.3/frontend/dist
http-server -p 4173 --cors
cd ~/skystrike-v8.3/frontend
npx vite preview --host
curl http://localhost:4174
cd ~/skystrike-v8.3/frontend
# Rebuild if needed
npm run build
# Kill any stuck preview server
pkill -f "vite preview"
# Start fresh Vite preview server
npx vite preview --host
curl http://localhost:4173/assets/index-c9d68e47.js
curl http://localhost:4173
cd ~/skystrike-v8.3/frontend
# Kill any stuck preview
pkill -f "vite preview"
# Start Vite with public origin
npx vite preview --host 0.0.0.0 --port 4173 --strictPort
cd ~/skystrike-v8.3
mkdir -p ui_temp
unzip skystrike_v8.2_final_fixed.zip -d ui_temp
ls -l ~/skystrike-v8.3/
cd ~/skystrike-v8.3/ui_temp/frontend/src
find . -type f
cp ~/skystrike-v8.3/ui_temp/frontend/src/* ~/skystrike-v8.3/frontend/src/
cp ~/skystrike-v8.3/ui_temp/frontend/public/*.png ~/skystrike-v8.3/frontend/public/
cd ~/skystrike-v8.3/frontend
npm install        # Only needed once (safe to rerun)
npm run build
nano ~/skystrike-v8.3/frontend/src/App.jsx
cd ~/skystrike-v8.3/frontend
npm run build
npx vite preview --host 0.0.0.0 --port 4173 --strictPort
curl http://checkip.amazonaws.com
cd ~/skystrike-v8.3/frontend
docker build -t skystrike-ui .
docker run -d --name skystrike-ui-prod -p 80:80 skystrike-ui
sudo systemctl stop nginx
docker stop skystrike-ui-prod
docker rm skystrike-ui-prod
docker run -d --name skystrike-ui-prod -p 80:80 skystrike-ui
cd ~/skystrike-v8.3/frontend
rm -rf dist
npm run build
docker stop skystrike-ui-prod
docker rm skystrike-ui-prod
docker build -t skystrike-ui .
docker run -d --name skystrike-ui-prod -p 80:80 skystrike-ui
npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
docker ps
docker stop skystrike-ui-prod
docker rm skystrike-ui-prod
docker run -d --name ui-final -p 80:80 skystrike-ui-final
docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
docker container prune
cd ~/skystrike-v8.3/backend
uvicorn app:app --host 0.0.0.0 --port 8501
from backend.utils.option_chain import get_option_chain
nano strategy_engine.py
uvicorn app:app --host 0.0.0.0 --port 8501
nano app.py
uvicorn app:app --host 0.0.0.0 --port 8501
npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
cd ~/skystrike-v8.3/frontend
npm install
npm run build
cd ~/skystrike-v8.3/frontend
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
VITE_API_BASE="http://3.149.137.243:8501" npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
cd ~/skystrike-v8.3/backend
uvicorn app:app --host 0.0.0.0 --port 8501
cd ~/skystrike-v8.3/frontend
VITE_API_BASE="http://3.149.137.243:8501" npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
cd ~/skystrike-v8.3/frontend
VITE_API_BASE="http://3.149.137.243:8501" npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
VITE_API_BASE="http://3.149.137.243:8501" npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
# Step 1: Move the zip file into the frontend directory
mv /path/to/skystrike-ui-final.zip ~/skystrike-v8.3/frontend/
# Step 2: Go into the frontend directory
cd ~/skystrike-v8.3/frontend/
# Step 3: Unzip and overwrite all files
unzip -o skystrike-ui-final.zip
# Step 4: Install fresh dependencies
npm install
# Step 5: Run the dev server or build again
npm run build
npx vite preview --host 0.0.0.0 --port 4173
curl http://localhost:4173
ps aux | grep vite
npx vite preview --host 0.0.0.0 --port 4173 --strictPort
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
# Step 1: Rebuild Docker
docker build -t skystrike-ui-final .
# Step 2: Stop/remove any stale container
docker stop ui-final && docker rm ui-final
# Step 3: Run production container on port 80
docker run -d --name ui-final -p 80:80 skystrike-ui-final
VITE_API_BASE=http://3.149.137.243:8501 npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
# 💥 Remove any old dist or cached config
rm -rf dist node_modules
# ✅ Set the correct backend address inline (critical)
VITE_API_BASE=http://3.149.137.243:8501 npm install && VITE_API_BASE=http://3.149.137.243:8501 npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
rm -rf dist node_modules .vite
npm install
VITE_API_BASE=http://3.149.137.243:8501 npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
docker ps
cd ~/skystrike-v8.3/backend
# Run the backend server manually (for now):
uvicorn app:app --host 0.0.0.0 --port 8501
VITE_API_BASE=http://3.149.137.243:8501 npm run build
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
cat src/Dashboard.jsx | grep "🟢 DASHBOARD DATA"
cd ~/skystrike-v8.3/frontend/src
nano Dashboard.jsx
cd ~/skystrike-v8.3/frontend
VITE_API_BASE=http://3.149.137.243:8501 npm run build
docker build --no-cache -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
cd ~/skystrike-v8.3/backend
uvicorn app:app --host 0.0.0.0 --port 8501
cat ~/skystrike-v8.3/frontend/src/Dashboard.jsx | grep DASHBOARD
cd ~/skystrike-v8.3/frontend
rm -rf dist node_modules .vite
npm install
VITE_API_BASE=http://3.149.137.243:8501 npm run build
docker build --no-cache -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
cd ~/skystrike-v8.3/backend
uvicorn app:app --host 0.0.0.0 --port 8501
cd ~/skystrike-v8.3/frontend
rm -rf dist node_modules .vite
npm install
# Rebuild with correct API endpoint
VITE_API_BASE=http://3.149.137.243:8501 npm run build
# Force full Docker rebuild
docker stop ui-final && docker rm ui-final
docker build --no-cache -t skystrike-ui-final .
docker run -d --name ui-final -p 80:80 skystrike-ui-final
docker exec -it ui-final sh
cd ~/skystrike-v8.3/frontend
rm -rf dist node_modules .vite
npm install
VITE_API_BASE=http://3.149.137.243:8501 npm run build
docker stop ui-final && docker rm ui-final
docker build --no-cache -t skystrike-ui-final .
docker run -d --name ui-final -p 80:80 skystrike-ui-final
docker exec -it ui-final sh
~/skystrike-v8.3/frontend/.env.production
VITE_API_BASE=http://3.149.137.243:8501
cd ~/skystrike-v8.3/frontend
rm -rf dist node_modules .vite
npm install
npm run build
docker stop ui-final && docker rm ui-final
docker build --no-cache -t skystrike-ui-final .
docker run -d --name ui-final -p 80:80 skystrike-ui-final
docker exec -it ui-final sh
/frontend/.env.production
cd ~/skystrike-v8.3/frontend
echo 'VITE_API_BASE=http://3.149.137.243:8501' > .env.production
cat .env.production
rm -rf dist node_modules .vite
npm install
VITE_API_BASE=http://3.149.137.243:8501 npm run build
# Stop and remove the old container
docker stop ui-final && docker rm ui-final
# Build the new Docker image with updated frontend code
docker build -t skystrike-ui-final .
# Run the new container on port 80
docker run -d --name ui-final -p 80:80 skystrike-ui-final
curl http://localhost:8501/dashboard
cd ~/skystrike-v8.3/backend
uvicorn app:app --host 0.0.0.0 --port 8501
curl http://localhost:8501/dashboard
cd ~/skystrike-v8.3/backend
nohup uvicorn app:app --host 0.0.0.0 --port 8501 > backend.log 2>&1 &
curl http://localhost:8501/dashboard
cd ~/skystrike-v8.3/frontend
npm run build
npm install react-router-dom
npm run build
docker stop ui-final && docker rm ui-final
docker build -t skystrike-ui-final .
docker run -d --name ui-final -p 80:80 skystrike-ui-final
npm install --save connect-history-api-fallback
docker stop ui-final && docker rm ui-final
docker build -t skystrike-ui-final .
docker run -d --name ui-final -p 80:80 skystrike-ui-final
cd ~/skystrike-v8.3/frontend
npm run build
ls dist/
docker stop ui-final && docker rm ui-final
docker build --no-cache -t skystrike-ui-final .
docker run -d --name ui-final -p 80:80 skystrike-ui-final
cat /etc/nginx/conf.d/default.conf
ls /usr/share/nginx/html/
server {
}
docker build -t skystrike-ui-final .
docker stop ui-final && docker rm ui-final
docker build --no-cache -t skystrike-ui-final .
docker run -d --name ui-final -p 80:80 skystrike-ui-final
docker stop ui-final && docker rm ui-final
docker run -d --name ui-final -p 80:80 skystrike-ui-final
nano ~/skystrike-v8.3/frontend/src/LoginPage.jsx
npm run build
docker stop ui-final && docker rm ui-final
docker build -t skystrike-ui-final .
docker run -d --name ui-final -p 80:80 skystrike-ui-final
touch ~/skystrike-v8.3/frontend/src/LoginPage.css
cd /path/to/your/skystrike-frontend
npm install
npm run dev
npm run dev -- --host
cd ~/skystrike-v8.3/frontend
npm run build
npm install -g serve
sudo npm install -g serve
serve -s dist -l 3000
serve -s dist -l tcp://0.0.0.0:3000
npm run build
serve -s dist -l tcp://0.0.0.0:3000
npm run build
serve -s dist -l tcp://0.0.0.0:3000
sudo npm install -g pm2
pm2 serve dist 3000 --name skystrike-frontend
pm2 save
pm2 delete skystrike-frontend
pm2 serve dist 3000 --name skystrike-frontend
pm2 save
pm2 update
pm2 delete skystrike-frontend
pm2 serve dist 3000 --spa --name skystrike-frontend
pm2 save
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build && pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
npm run build
pm2 restart skystrike-frontend
pm2 restart skystrike-backend
npm run build
curl http://localhost:8000/api/dashboard
pm2 list
cd ~/skystrike-v8.3/backend
uvicorn main:app --host 0.0.0.0 --port 8000
cd ~/skystrike-v8.3/backend
uvicorn main:app --host 0.0.0.0 --port 8000
cd ~/skystrike-v8.3/backend
uvicorn main:app --host 0.0.0.0 --port 8000
rm frontend/main.py
npm run build
cd ~/skystrike-v8.3/frontend
npm run build
cd ~/skystrike-v8.3/frontend
npm run build
pm2 restart skystrike-frontend
cd ~/skystrike-v8.3/backend
uvicorn main:app --host 0.0.0.0 --port 8000
npm run dev
cd ~/skystrike-v8.3/frontend
npm run dev
mv src/AuthContext.js src/AuthContext.jsx
npm run dev
mv src/AuthContext.js src/AuthContext.jsx
mv: cannot stat 'src/AuthContext.js': No such file or directory
grep -r "AuthContext" src/
sed -i 's|from .*/AuthContext[\'\"]|from "./AuthContext.jsx|g' src/*.jsx src/**/*.jsx

sed -i 's|from .*/AuthContext[\'\"]|from "../AuthContext.jsx|g' src/**/*.jsx

rm -rf node_modules/.vite dist
npm run dev

sed -i 's|from .*/AuthContext[\'\"]|from "./AuthContext.jsx|g' src/*.jsx src/**/*.jsx

sed -i 's|from .*/AuthContext[\'\"]|from "../AuthContext.jsx|g' src/**/*.jsx

rm -rf node_modules/.vite dist
npm run dev

mv src/AuthContext.jsx src/AuthContext.jsx  # just confirms it's there
# Fix import paths for AuthContext
find src -type f -name "*.jsx" -exec sed -i 's|from ["'\''"]\(\.\./\)*AuthContext["'\''"]|from "\1AuthContext.jsx"|g' {} +
# Remove old build artifacts
rm -rf dist node_modules/.vite
# Restart Vite
npm run dev
curl http://localhost:8501/dashboard
rm -rf dist node_modules/.vite
npm run dev
npm run dev -- --host
npm run dev
rm -rf dist node_modules/.vite
npm run dev
npm install
npm create vite@latest skystrike-frontend -- --template react
cd skystrike-frontend
npm install
npm init -y
npm run dev
npm run dev -- --host
pkill -f vite   # kill any old Vite process (safe)
npm run dev -- --host
~/skystrike-v8.3/frontend/skystrike-frontend
cd ~/skystrike-v8.3/frontend/skystrike-frontend
npm run dev -- --host
cd ~/skystrike-v8.3/frontend/skystrike-frontend
npm run dev -- --host
cd ~/skystrike-v8.3/frontend/skystrike-frontend
npm run dev -- --host
npm run build
npm run preview -- --host
skystrike-frontend/index.html
npm run dev -- --host
cd ~/skystrike-v8.3/frontend/skystrike-frontend
nano index.html
npm run dev -- --host
ps aux | grep vite
cd ~/skystrike-v8.3/frontend/skystrike-frontend
ls src/main.jsx
nano src/main.jsx
npm run dev -- --host
➜ Local: http://localhost:4173/
➜ Network: http://3.149.137.243:4173/
curl http://localhost:4173
mkdir ~/skystrike-v8.6
unzip ~/skystrike-v8.3/skystrike-v8.6-recovery.zip -d ~/skystrike-v8.6
cd ~/skystrike-v8.6
npm install react react-dom
npm install --save-dev vite @vitejs/plugin-react
npm run dev -- --host
nano package.json
npm install
npm run dev -- --host
npm install react-router-dom
npm run dev -- --host
nano src/App.css
npm run dev -- --host
http://3.149.137.243:4173
npm run build
npm run preview -- --host
unzip skystrike-ui-fallback-patch.zip -d ~/skystrike-v8.6
unzip /mnt/data/skystrike-ui-fallback-patch.zip -d ~/skystrike-v8.6
unzip skystrike-ui-fallback-patch.zip -d ./frontend
unzip /home/ubuntu/skystrike-v8.3/skystrike-ui-fallback-patch.zip -d ~/skystrike-v8.6
A
unzip /home/ubuntu/skystrike-v8.3/skystrike-ui-fallback-patch.zip -d ~/skystrike-v8.6
cd ~/skystrike-v8.6
npm run dev -- --host
cd ~/skystrike-v8.6
unzip skystrike-frontend-bootstrap.zip
chmod +x install.sh
./install.sh
npm run dev -- --host
unzip /home/ubuntu/skystrike-v8.3/skystrike-ui-router-patch.zip -d ~/skystrike-v8.6/src
cd ~/skystrike-v8.6
mv /mnt/data/skystrike-ui-router-patch.zip ./
unzip skystrike-ui-router-patch.zip -d ./src
npm run dev -- --host
cp /mnt/data/skystrike-ui-router-patch.zip ~/skystrike-v8.6/
cd ~/skystrike-v8.6
unzip -o skystrike-ui-router-patch.zip -d ./src
npm run dev -- --host
ls -l src/main.jsx
head -n 10 src/main.jsx
unzip -o skystrike-ui-router-patch.zip -d src
head -n 5 src/main.jsx
mv src/src/* src/
cp -r src/src/* src/
rm -r src/src
pkill -f vite
npm run dev -- --host
#!/bin/bash
echo "🛑 Stopping and removing SkyStrike Docker containers..."
docker stop skystrike-prod 2>/dev/null || true
docker rm skystrike-prod 2>/dev/null || true
echo "🧼 Removing SkyStrike Docker image..."
docker rmi skystrike-app 2>/dev/null || true
echo "🗑️ Deleting old project folders and files..."
rm -rf ~/skystrike-v8.8 ~/skystrike-v8.6 ~/skystrike-v8.3 ~/skystrike-phase1 ~/skystrike-prod
echo "🧪 Deleting leftover zip files and scripts..."
rm -f ~/skystrike-*.zip ~/deploy_skystrike.sh ~/cleanup_skystrike.sh ~/uninstall_skystrike.sh
echo "🧽 Pruning unused Docker volumes and networks..."
docker volume prune -f
docker network prune -f
echo "✅ SkyStrike has been uninstalled from this server."
chmod +x uninstall_skystrike.sh
#!/bin/bash
echo "Cleaning up SkyStrike old directories and scripts..."
# Define files and directories to delete
delete_dirs=( "skystrike-v8.3" "skystrike-v8.6" "__pycache__" "tests" )
delete_files=(    "clean_skystrike_phase1_remnants.sh"   "clean_skystrike_server.sh"   "deploy_skystrike.sh"   "docker-compose.yml"   "main.py"   "README.md"   "relocate_to_sandbox.py"   "routes.py"   "env" )
# Remove old directories
for dir in "${delete_dirs[@]}"; do   if [ -d "$HOME/$dir" ]; then     echo "Removing directory: $dir";     rm -rf "$HOME/$dir";   fi; done
# Remove files
for file in "${delete_files[@]}"; do   if [ -f "$HOME/$file" ]; then     echo "Removing file: $file";     rm "$HOME/$file";   fi; done
# Optionally remove venv if not needed
read -p "Do you want to remove the Python venv folder? (y/n): " confirm
if [[ "$confirm" == "y" ]]; then   rm -rf "$HOME/venv";   echo "Removed virtual environment."; fi
echo "Cleanup complete. Remaining contents in /home/ubuntu:"
ls -lh "$HOME"
bash deploy_skystrike_v8.8.sh
bash deploy_skystrike_v8.8_fresh.sh
git checkout main
git reset --hard HEAD~1           # Or further back if needed
# OR to wipe all history:
# git checkout --orphan new-main
# git add .
# git commit -m "Clean SkyStrike v8.8 baseline"
# git branch -M main
git push origin main --force
chmod +x deploy_skystrike_v8.8_baseline.sh
./deploy_skystrike_v8.8_baseline.sh
chmod +x deploy_skystrike_v8.8_final.sh
./deploy_skystrike_v8.8_final.sh
sudo lsof -i :8501
docker ps
docker stop <container_id_using_8501>
sudo kill -9 <PID>
sudo kill -9 59490
docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app
ls skystrike-v8.8/.env
cd skystrike-v8.8
docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app
docker rm skystrike-prod
docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app
rm -rf skystrike-v8.8
unzip skystrike-v8.8-ui-release.zip
cd skystrike-v8.8
unzip skystrike-v8.8-ui-release.zip
cd skystrike-v8.8
cd ..
ls
unzip skystrike-v8.8-ui-release.zip
cd skystrike-v8.8
A
~/skystrike-v8.8
mv skystrike-v8.8 skystrike-v8.8-prod
cd ..
mv skystrike-v8.8 skystrike-v8.8-prod
cd skystrike-v8.8-prod
cd ~/skystrike-v8.8-prod
ls deploy_skystrike_v8.8_ui_release.sh
cp ~/deploy_skystrike_v8.8_ui_release.sh ~/skystrike-v8.8-prod/
cd ~/skystrike-v8.8-prod
bash deploy_skystrike_v8.8_ui_release.sh
# From inside ~/skystrike-v8.8-prod
docker build -t skystrike-app .
docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app
docker stop skystrike-prod || true
docker rm skystrike-prod || true
docker rmi skystrike-app || true
#!/bin/bash
echo "🧼 Cleaning up all SkyStrike deployments..."
docker stop skystrike-prod 2>/dev/null || true
docker rm skystrike-prod 2>/dev/null || true
docker rmi skystrike-app 2>/dev/null || true
echo "🗑️ Removing any leftover folders..."
rm -rf ~/skystrike-v8.8 ~/skystrike-v8.8-prod ~/skystrike-ui* ~/skystrike-frontend* ~/skystrike-phase1
echo "🧽 Cleaning up unused Docker volumes and networks..."
docker volume prune -f
docker network prune -f
echo "✅ SkyStrike environment cleaned."
bash deploy_skystrike_v8.8_clean.sh
cd ~
ls deploy_skystrike_v8.8_clean.sh
scp deploy_skystrike_v8.8_clean.sh ubuntu@<your-ip>:~
/home/ubuntu/deploy_skystrike_v8.8_clean.sh
chmod +x deploy_skystrike_v8.8_clean.sh
./deploy_skystrike_v8.8_clean.sh
docker stop skystrike-prod || true
docker rm skystrike-prod || true
docker rmi skystrike-app || true
rm -rf skystrike-app
#!/bin/bash
# === SkyStrike v8.9 Deployment Script ===
echo "🔄 Unzipping project..."
unzip -o skystrike-v8.9-ui-final.zip -d skystrike-app
cd skystrike-app || { echo "❌ Failed to enter project directory"; exit 1; }
# === Step 1: Frontend Setup ===
echo "📁 Entering frontend directory..."
cd frontend || { echo "❌ 'frontend' directory not found"; exit 1; }
echo "📦 Installing npm packages..."
npm install --legacy-peer-deps
echo "🛠 Building frontend..."
npm run build || { echo "❌ Frontend build failed"; exit 1; }
cd ..
# === Step 2: Docker Build ===
echo "🐳 Building Docker image 'skystrike-app'..."
docker build -t skystrike-app .
# === Step 3: Container Reset ===
echo "🛑 Stopping previous container (if any)..."
docker stop skystrike-prod 2>/dev/null || true
docker rm skystrike-prod 2>/dev/null || true
# === Step 4: Run Container ===
echo "🚀 Running new SkyStrike container on port 4173..."
docker run -d   --name skystrike-prod   -p 4173:4173   --env-file .env   skystrike-app
echo "✅ SkyStrike deployed successfully at: http://localhost:4173"
CMD ["serve", "-s", "dist", "-l", "4173"]
CMD ["serve", "-s", "dist", "-l", "8501"]
nano Dockerfile
docker build -t skystrike-app .
docker stop skystrike-prod || true
docker rm skystrike-prod || true
docker run -d   --name skystrike-prod   -p 4173:4173   --env-file .env   skystrike-app
docker restart skystrike-prod
docker ps
``>
Expected output should include something like:
docker exec -it skystrike-prod /bin/sh
mkdir -p ~/.ssh
echo "ssh-rsa AAAAB3Nza..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
mkdir -p ~/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9Y0yO18+lQiLIlgwRqBvownUkazxbI11SfL8HRuiiKf1GG4F+gtgPRbU9oQil0PbNhIbGOoQLKrzDBSUr21JfSK9uJ/RL003TbpqkLCrA5CCvPzFEXyohh4ymn3jVvHgLuy7CAe5nDBCEo84d1RZCAknQNCSZ/ziwr9ZTmwzEIGlse5187HbXlQhlzdeFk7xEgDh7ZVUMVpQGKUVgOtGxKPrY9YK1FYLmJeKB7rNMcqoc45x3ZenTGbBYQSLa/4KmDwS0haZPh8eTC8GboLgBwBksgFV7DG50BSkJybpAwrEghdxjZlct2igHKXnlbk2g0Vc+aAcScz3xJVSvSWfd skystrike-key" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
ls -la ~/.ssh
docker container stop $(docker ps -aq)
docker container rm $(docker ps -aq)
docker image rm $(docker images -q)
rm -rf ~/skystrike-* ~/frontend ~/backend
sudo apt autoremove -y && sudo apt autoclean
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y
sudo nano /etc/nginx/sites-available/skystrike
sudo ln -sf /etc/nginx/sites-available/skystrike /etc/nginx/sites-enabled/skystrike
sudo nginx -t
sudo systemctl restart nginx
npm run dev -- --host
cd ~/skystrike-stackblitz-9.3.5/frontend
cd ~
cd /home/ubuntu
# Backup just in case
mkdir -p ~/backup-$(date +%s)
mv deploy dist public sandbox src *.sh *.yml *.js *.py *.html *.config.js *.zip ~/backup-*/ 2>/dev/null
# OR if you're sure, force delete:
rm -rf deploy dist public sandbox src *.sh *.yml *.js *.py *.html *.config.js *.zip
ssh-keygen -t ed25519 -C "skystrike-deploy"
# Press ENTER through prompts (path: /home/ubuntu/.ssh/id_ed25519)
ssh-keygen -t ed25519 -C "skystrike-deploy"
# Press ENTER through prompts (path: /home/ubuntu/.ssh/id_ed25519)
/home/ubuntu/.ssh/id_skystrike
ssh-keygen -t ed25519 -C "skystrike-deploy"
/home/ubuntu/.ssh/id_skystrike
ssh-keygen -t ed25519 -C "skystrike-deploy"
cat ~/.ssh/id_skystrike.pub
ssh -T git@github.com
cd ~
git clone git@github.com:andrusym/skystrike-phase1.git
# Backup everything just in case
timestamp=$(date +%s)
mkdir -p ~/backup-$timestamp
mv ~/deploy ~/dist ~/public ~/sandbox ~/src ~/*.sh ~/*.yml ~/*.js ~/*.py ~/*.html ~/*.config.js ~/*.zip ~/backup-$timestamp/ 2>/dev/null
ls -la ~
git clone git@github.com:andrusym/skystrike-stackblitz.git
cd skystrike-stackblitz
git checkout 9.3.6
cd backend
pip install -r requirements.txt
cd ../frontend
npm install
ls ~/skystrike-stackblitz/backend
nano ~/skystrike-stackblitz/backend/requirements.txt
cd ~/skystrike-stackblitz
git add backend/requirements.txt
git commit -m "Add backend requirements.txt for Phase 1 dependencies"
git push origin main
cd ~
git clone git@github.com:andrusym/skystrike-stackblitz.git
cd skystrike-stackblitz
cd ~/skystrike-stackblitz
rm -rf ~/skystrike-stackblitz
git clone git@github.com:andrusym/skystrike-stackblitz.git
cd skystrike-stackblitz
cd ~
rm -rf skystrike-stackblitz
git clone git@github.com:andrusym/skystrike-stackblitz.git
cd skystrike-stackblitz
pip install -r requirements.txt
cd backend  # or whatever folder contains your Python backend
pip freeze > requirements.txt
pip install -r requirements.txt
python3 main.py
ls -la
cd backend
ls -la
python3 main.py
cd ~
rm -rf skystrike-stackblitz
git clone git@github.com:andrusym/skystrike-phase1.git
cd skystrike-phase1
cd ~
rm -rf skystrike-stackblitz
git clone git@github.com:andrusym/skystrike-phase1.git
cd skystrike-phase1
cd ~
rm -rf skystrike-phase1
git clone git@github.com:andrusym/skystrike-phase1.git
cd skystrike-phase1
ls
pip install -r requirements.txt
python3 main.py
mkdir -p utils
nano utils/pricing.py
python3 main.py
nano utils/ml.py
python3 main.py
mkdir -p engine
nano engine/exit_rules.py
python3 main.py
nano engine/order_executor.py
python3 main.py
def place_spread_order(ticker, quantity, leg1, leg2):
nano engine/order_executor.py
python3 main.py
nano engine/order_executor.py
python3 main.py
nano utils/scanner.py
python3 main.py
nano utils/stats.py
python3 main.py
nano utils/ml.py
python3 main.py
nano utils/pricing.py
python3 main.py
nano utils/pricing.py
python3 main.py
nano utils/pricing.py
python3 main.py
nano utils/pricing.py
python3 main.py
cd ~/skystrike-phase1
nano strategy_ironcondor.py
python3 main.py
nano strategy_ironcondor.py
python3 main.py
nano option_chain.py
python3 main.py
nano utils/pricing.py
python3 main.py
cd ~/skystrike-phase1
unzip /path/to/skystrike_phase1_allfiles.zip
scp "C:\Users\andru\Downloads\skystrike_phase1_allfiles.zip" ubuntu@<your-server-ip>:/home/ubuntu/
ubuntu@ip-172-26-1-2:~/skystrike-phase1$ scp "C:\Users\andru\Downloads\skystrike_phase1_allfiles.zip" ubuntu@<your-server-ip>:/home/ubuntu/
-bash: your-server-ip: No such file or directory
ubuntu@ip-172-26-1-2:~/skystrike-phase1$
scp "C:\Users\andru\Downloads\skystrike_phase1_allfiles.zip" 3.149.137.243:/home/ubuntu/
cd /home/ubuntu
cp skystrike_phase1_allfiles/*.py skystrike-phase1/
cp -r skystrike_phase1_allfiles/utils/* skystrike-phase1/utils/
cd ~/skystrike-phase1
export TRADIER_API_KEY="your_real_tradier_token"
python3 main.py
nano strategy_kingcondor.py
export TRADIER_API_KEY="your_real_tradier_token"
python3 main.py
nano utils/pricing.py
export TRADIER_API_KEY="your_real_tradier_token"
python3 main.py
nano strategy_spread.py
export TRADIER_API_KEY="your_real_tradier_token"
python3 main.py
cd ~/skystrike-phase1
# Stage the new/updated files
git add utils/pricing.py utils/ml.py engine/exit_rules.py
# Commit with a clear message
git commit -m "Add missing modules: pricing.py, ml.py, and exit_rules.py"
git push origin main
git status
pip install GitPython
cd ~/skystrike-stackblitz
#!/bin/bash
cd ~
rm -rf skystrike-stackblitz
git clone https://github.com/andrusym/skystrike-stackblitz.git
cd skystrike-stackblitz
# Checkout and branch
git checkout 9.3.6
git checkout -b 9.3.7
# Extract and apply fixed files
unzip ~/Downloads/skystrike_fixed_imports.zip -d temp_fix
cp -r temp_fix/* .
rm -r temp_fix
# Commit and push
git add .
git commit -m "Fix: import cleanup from 9.3.6 to 9.3.7 with stable strategy files"
git push origin 9.3.7
# From inside your skystrike-stackblitz repo on branch 9.3.7
# 1. Unzip using correct path
unzip ~/skystrike_fixed_imports.zip -d temp_fix
# 2. Copy fixed files into place
cp -r temp_fix/* .
rm -r temp_fix
# 3. Commit and push again
git add .
git commit -m "Fix: import cleanup from 9.3.6 to 9.3.7 with stable strategy files"
git push origin 9.3.7
mv /home/ubuntu/Downloads/skystrike_fixed_imports.zip ~/skystrike_fixed_imports.zip
# Extract the fixed files
unzip ~/skystrike_fixed_imports.zip -d temp_fix
# Copy them into the project directory
cp -r temp_fix/* .
# Clean up the temporary folder
rm -r temp_fix
# Commit and push to branch 9.3.7
git add .
git commit -m "Fix: import cleanup from 9.3.6 to 9.3.7 with stable strategy files"
git push origin 9.3.7
# Start fresh
cd ~
rm -rf skystrike-prod
git clone git@github.com:andrusym/skystrike-stackblitz.git skystrike-prod
cd skystrike-prod
# Checkout the baseline branch
git checkout 9.3.6
# Rename it to main and set upstream
git checkout -b main
git remote set-url origin git@github.com:andrusym/skystrike-prod.git
# Push main to skystrike-prod
git push --force --set-upstream origin main
# Tag and push v9.3.6
git tag v9.3.6
git push origin v9.3.6
# 1. Force main to match 9.3.6
git checkout 9.3.6
git branch -f main
# 2. Push main to overwrite the GitHub version
git push --force origin main
# 3. (Re-confirm tag just in case)
git tag -f v9.3.6
git push --force origin v9.3.6
cd ~/skystrike-prod
git checkout -b 9.3.8
unzip ~/Downloads/skystrike_9.3.8.zip -d temp_938
cp -r temp_938/* .
rm -r temp_938
git add .
git commit -m "Release: version 9.3.8 full production platform with backend, UI, HTTPS, and ML prep"
git push origin 9.3.8
/home/ubuntu/skystrike_9.3.8.zip
scp "C:\Users\andru\Downloads\skystrike_9.3.8.zip" ubuntu@<YOUR_EC2_IP>:/home/ubuntu/
cd ~/skystrike-prod
git checkout -b 9.3.9
scp "C:\Users\andru\Downloads\skystrike_9.3.9_flat.zip" ubuntu@<YOUR_SERVER_IP>:/home/ubuntu/
/mnt/data/skystrike_9_3_9_cleaned/skystrike-prod-9.3.8/
cd ~/skystrike-prod
git checkout -b 9.3.9
unzip ~/skystrike_9.3.9_flat.zip -o
git add .
git commit -m "Release: 9.3.9 cleaned production build (flattened, HTTPS, ML-ready)"
git push origin 9.3.9
git pull --rebase origin 9.3.9
git push origin 9.3.9
unzip ~/skystrike_9.3.9_flat.zip -o
git add .
git commit -m "Apply ZIP contents to 9.3.9 after syncing with origin"
git push origin 9.3.9
cd ~/skystrike-prod
unzip -o ~/skystrike_9.3.9_flat.zip
git add .
git commit -m "Apply ZIP contents to 9.3.9 after syncing with origin"
git push origin 9.3.9
/home/ubuntu/skystrike-prod
docker stop skystrike-prod 2>/dev/null && docker rm skystrike-prod 2>/dev/null
docker build -t skystrike-prod .
npm install react-router-dom
cd frontend
npm install react-router-dom
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 80:80 --env-file .env.production skystrike-prod
cd /home/ubuntu/skystrike-prod/
docker build -t skystrike-prod -f frontend/Dockerfile .
#!/bin/bash
echo "=== SkyStrike v9.3.10 Deployment Starting ==="
# Set working directory
cd /home/ubuntu || exit
# Step 1: Unzip the new release
unzip -o skystrike_release_9.3.10.zip -d skystrike_9.3.10
# Step 2: Navigate to the project directory
cd skystrike_9.3.10 || exit
# Step 3: Build Docker image
docker build -t skystrike-app .
# Step 4: Stop and remove old container if exists
docker stop skystrike-prod 2>/dev/null || true
docker rm skystrike-prod 2>/dev/null || true
# Step 5: Run new container
docker run -d   --name skystrike-prod   --env-file .env.production   -p 80:4173   skystrike-app
echo "=== SkyStrike v9.3.10 is now deployed and live at http://<YOUR_PUBLIC_IP> ==="
# 1. Stop and remove any existing containers
docker ps -a
docker stop skystrike-prod || true
docker rm skystrike-prod || true
# 2. Prune all unused Docker objects (optional but clean)
docker system prune -f
# 3. Delete old app directory (if applicable)
cd ~
rm -rf skystrike_9.3.10
rm -rf skystrike-prod-9.3.8
rm -rf temp_fix
rm -rf temp_938
rm -rf __MACOSX
# 4. Remove any previous zip or extraction folders
rm -f skystrike_*.zip
rm -rf skystrike_*
# 5. Confirm clean slate
ls -al ~
#!/bin/bash
echo "=== 🚀 Deploying SkyStrike v9.3.10 ==="
# 1. Prep
cd /home/ubuntu || exit
rm -rf skystrike_9.3.10
unzip -o skystrike_9.3.10_final.zip -d skystrike_9.3.10
cd skystrike_9.3.10 || exit
cd /home/ubuntu
# 1. Clean any old containers
docker stop skystrike-prod 2>/dev/null || true
docker rm skystrike-prod 2>/dev/null || true
# 2. Remove old project folder if it exists
rm -rf skystrike_9.3.10
# 3. Unzip the new release
unzip -o skystrike_9.3.10_final.zip -d skystrike_9.3.10
cd skystrike_9.3.10 || exit
# 4. Create fallback .env if missing
if [ ! -f .env.production ]; then   echo "TRADIER_API_KEY=your-api-key" > .env.production;   echo "TRADING_MODE=paper" >> .env.production; fi
# 5. Build the Docker image
docker build -t skystrike-prod .
# 6. Run the container
docker run -d   --name skystrike-prod   --env-file .env.production   -p 80:4173   skystrike-prod
echo "✅ SkyStrike v9.3.10 is now live at http://<your-server-ip>"
npm install react-router-dom
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
cd /path/to/skystrike_9.3.10/frontend
npm install
npm list react-router-dom
~/skystrike_9.3.10
nano Dockerfile
docker build -t skystrike-prod .
/skystrike_9.3.10/frontend/
ls -la ~/skystrike_9.3.10
nano Dockerfile
docker rm -f skystrike-prod 2>/dev/null
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
docker rm -f skystrike-prod 2>/dev/null
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
mkdir -p src
nano src/main.jsx
nano src/App.jsx
nano index.html
docker rm -f skystrike-prod 2>/dev/null
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
/skystrike_9.3.10/App.css
mv App.css src/App.css
mv app.css src/App.css
docker rm -f skystrike-prod 2>/dev/null
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
docker ps
cp -r /mnt/data/skystrike-prod-9.3.8/src ~/skystrike_9.3.10/
cp -r ~/skystrike-prod-9.3.8/src ~/skystrike_9.3.10/
find ~/skystrike-prod-9.3.8 -type d -name src
/home/ubuntu/skystrike-prod-9.3.8/skystrike-prod-9.3.8/frontend/src
cp -r /home/ubuntu/skystrike-prod-9.3.8/skystrike-prod-9.3.8/frontend/src ~/skystrike_9.3.10/
cd ~/skystrike_9.3.10
docker rm -f skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
ls ~/skystrike_9.3.10/src/App.css
nano ~/skystrike_9.3.10/src/main.jsx
cd ~/skystrike_9.3.10
# Clean any previous container and image
docker rm -f skystrike-prod
docker rmi skystrike-prod
# Rebuild from scratch
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
cat ~/skystrike_9.3.10/index.html
nano ~/skystrike_9.3.10/vite.config.js
nano ~/skystrike_9.3.10/index.html
cd ~/skystrike_9.3.10
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
CMD ["npx", "vite", "preview", "--host"]
nano ~/skystrike_9.3.10/Dockerfile
cd ~/skystrike_9.3.10
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
docker ps
0.0.0.0:4173->4173/tcp
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
docker rm -f skystrike-prod 2>/dev/null
docker rmi skystrike-prod 2>/dev/null
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Build the frontend
RUN npm run build
# Install static server
RUN npm install -g serve
# Serve the build output
EXPOSE 4173
CMD ["serve", "-s", "dist", "-l", "4173"]
nano Dockerfile
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
rm index.html
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
nano ~/skystrike_9.3.10/index.html
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
});
nano ~/skystrike_9.3.10/vite.config.js
nano ~/skystrike_9.3.10/index.html
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
docker exec -it skystrike-prod /bin/sh
nano ~/skystrike_9.3.10/vite.config.js
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
nano ~/skystrike_9.3.10/vite.config.js
cd ~/skystrike_9.3.10
rm -rf dist node_modules
npm install
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
cat ~/skystrike_9.3.10/dist/index.html
nano ~/skystrike_9.3.10/vite.config.js
cd ~/skystrike_9.3.10
rm -rf dist node_modules
npm install
npm run build
ls dist
nano Dockerfile
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
cd ~/skystrike_9.3.10
# Move dist/ somewhere safe
mv dist dist-final
# Remove all old source folders (don't worry, they're already built into dist)
rm -rf src frontend public node_modules
nano Dockerfile
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
cat dist-final/index.html
npx serve -s dist-final -l 4173
docker ps
docker stop <container_id_using_4173>
docker rm <container_id_using_4173>
lsof -i :4173
kill -9 <PID>
docker stop skystrike-prod
docker rm skystrike-prod
CMD ["serve", "-s", "dist", "-l", "4173"]
nano Dockerfile
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
ls -l ~/skystrike_9.3.10/dist-final
nano Dockerfile
docker rm -f skystrike-prod
docker rmi skystrike-prod
docker build -t skystrike-prod .
docker run -d --name skystrike-prod -p 4173:4173 skystrike-prod
ssh ubuntu@<your-ec2-ip>
cd ~/skystrike_9.3.10
git init
git remote add origin https://github.com/andrusym/skystrike-prod.git
git remote set-url origin https://github.com/andrusym/skystrike-prod.git
git checkout -b final-prod-9.3.10
echo "node_modules/" >> .gitignore
echo "dist/" >> .gitignore
echo "dist-final/" >> .gitignore
git add .
git commit -m "SkyStrike v9.3.10 production release from EC2"
git push origin final-prod-9.3.10
git remote -v
git remote set-url origin git@github.com:andrusym/skystrike-prod.git
cd ~/skystrike_9.3.10
git init
git add .
git commit -m "Final prod release 9.3.10"
git checkout -b final-prod-9.3.10
git push -u origin final-prod-9.3.10
npm install
npm run build
npm install
npm run build
cd ~/skystrike_9.3.10/frontend
npm install
npm run build
FROM node:18
WORKDIR /app
COPY dist ./dist
RUN npm install -g serve
EXPOSE 4173
CMD ["serve", "-s", "dist", "-l", "4173", "--single"]
cd ~/skystrike_9.3.10/frontend
nano Dockerfile
docker build -t skystrike-ui-prod .
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
docker ps
docker stop skystrike-prod
docker rm skystrike-prod
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
docker rm -f skystrike-ui-prod
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
ls dist
ls dist/assets
nano ~/skystrike_9.3.10/frontend/src/LoginPage.jsx
cd ~/skystrike_9.3.10/frontend
npm run build
docker rm -f skystrike-ui-prod
docker build -t skystrike-ui-prod .
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
http://3.149.137.243:4173/login
cd ~/skystrike_9.3.10/frontend
npm run build
docker rm -f skystrike-ui-prod
docker build -t skystrike-ui-prod .
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
npm run build
docker rm -f skystrike-ui-prod
docker build -t skystrike-ui-prod .
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
npm run build
docker rm -f skystrike-ui-prod
docker build -t skystrike-ui-prod .
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
---> Running in 07cd9965d45d
npm run build
docker rm -f skystrike-ui-prod
docker build -t skystrike-ui-prod .
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
npm run build
docker rm -f skystrike-ui-prod
docker build -t skystrike-ui-prod .
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
nano ~/skystrike_9.3.10/frontend/src/Sidebar.jsx
npm run build
docker rm -f skystrike-ui-prod
docker build -t skystrike-ui-prod .
docker run -d --name skystrike-ui-prod -p 4173:4173 skystrike-ui-prod
nano ~/skystrike_9.3.10/frontend/src/AppRouter.jsx
cd ~/skystrike_9.3.10/frontend
git init
git remote add origin git@github.com:andrusym/skystrike-prod.git
cd ~/skystrike_9.3.10
git init
git remote add origin git@github.com:andrusym/skystrike-prod.git
git checkout -b release-9.3.11
git commit -m "Full SkyStrike v9.3.11 release: frontend + backend, login, dashboard, dark mode, Tradier integration"
git add .
git commit -m "Full SkyStrike v9.3.11 release: backend + frontend"
git push -u origin release-9.3.11
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
nslookup staging.skystrike.ai
nslookup staging.skystrike.me
dig staging.skystrike.me @1.1.1.1
nslookup staging.skystrike.me
sudo certbot --nginx -d staging.skystrike.me
sudo nano /etc/nginx/sites-available/skystrike
sudo nginx -t
sudo systemctl reload nginx
sudo certbot install --cert-name staging.skystrike.me
sudo nano /etc/nginx/sites-available/skystrike
sudo ln -s /etc/nginx/sites-available/skystrike /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo ufw allow 443
sudo certbot certificates
sudo systemctl restart nginx
cd ~/skystrike_9.3.10
# Initialize Git if not already
git init
# Add remote (if missing or broken, overwrite)
git remote remove origin 2>/dev/null
git remote add origin https://github.com/andrusym/skystrike-prod.git
# Checkout target branch and reset to local
git checkout -B release-9.3.11
# Stage all files forcefully
git add .
# Commit with overwrite message
git commit -m "Force push current AWS files to release-9.3.11"
# Force push to GitHub branch
git push -f origin release-9.3.11
cd ~/skystrike_9.3.10
git add -f frontend/
ls -la frontend/
rm -rf frontend/.git
cd ~/skystrike_9.3.10
git add frontend/
git commit -m "Add full frontend directory to release-9.3.11"
git push origin release-9.3.11
git push https://andrusym:<YOUR_TOKEN>@github.com/andrusym/skystrike-prod.git release-9.3.11
git push https://andrusym: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@github.com/andrusym/skystrike-prod.git release-9.3.11
cd ~/skystrike_9.3.10
# Extract and overwrite updated components from the ZIP
unzip -o skystrike_recovery_bundle.zip
# Rebuild frontend if needed
cd frontend
npm install
npm run build
# Restart services (Docker)
cd ~/skystrike_9.3.10
docker-compose down
docker-compose up -d --build
sudo lsof -i :4173
docker ps
0.0.0.0:4173->4173/tcp
docker stop skystrike-ui-prod
docker rm skystrike-ui-prod
cd ~/skystrike_9.3.10
docker-compose up -d --build
docker ps
docker stop skystrike-ui-prod
docker rm skystrike-ui-prod
nano ~/skystrike_9.3.10/docker-compose.yml
npm run build
npm run preview
cd ~/skystrike_9.3.10/frontend
npm install
npm run build
npm run preview -- --port 4173
cd ~/skystrike_9.3.10
docker-compose down
cd ~/skystrike_9.3.10/frontend
npm run preview -- --port 4173 --host
sudo nginx -t
sudo systemctl reload nginx
sudo lsof -i :4173
sudo kill -9 <PID_FROM_ABOVE>
cd ~/skystrike_9.3.10/frontend
npm run preview -- --port 4173 --host 0.0.0.0
nano ~/skystrike_9.3.10/frontend/vite.config.js
cd ~/skystrike_9.3.10/frontend
npm run preview -- --port 4173 --host 0.0.0.0
sudo lsof -i :4173
sudo kill -9 <PID>   # from the command above
sudo kill -9 17409
npm run preview -- --port 4173 --host 0.0.0.0
nano ~/skystrike_9.3.10/frontend/vite.config.js
# Kill old Vite if running
sudo lsof -i :4173
sudo kill -9 <PID>
# Restart
cd ~/skystrike_9.3.10/frontend
npm run preview -- --port 4173 --host 0.0.0.0
cd ~/skystrike_9.3.10/frontend
npm run build
sudo nano /etc/nginx/sites-available/skystrike
sudo nginx -t
sudo systemctl reload nginx
frontend/dist/assets/
cd ~/skystrike_9.3.10/frontend
mv dist-final dist
mv ../dist-final ./dist
/home/ubuntu/skystrike_9.3.10/dist-final
→ to →
/home/ubuntu/skystrike_9.3.10/frontend/dist
sudo nginx -t
sudo systemctl reload nginx
cd ~/skystrike_9.3.10/frontend
npm run build
ls -l ~/skystrike_9.3.10/frontend/dist/assets
sudo nginx -t
sudo systemctl reload nginx
npm run build
ls -l ~/skystrike_9.3.10/frontend/dist/assets/
cat ~/skystrike_9.3.10/frontend/dist/index.html | grep css
nano ~/skystrike_9.3.10/frontend/dist/index.html
<script type="module" crossorigin src="/assets/index-DGFKJK4H.js"></script>
nano ~/skystrike_9.3.10/frontend/dist/index.html
npm run build
server {
}
sudo nano /etc/nginx/sites-available/default
sudo nginx -t
sudo systemctl reload nginx
ls -l ~/skystrike_9.3.10/frontend/dist/assets
cat /etc/nginx/sites-available/default
sudo nginx -t && sudo systemctl reload nginx
cd ~/skystrike_9.3.10/frontend
unzip -o skystrike_recovery_bundle.zip
rm -rf dist
npm run build
sudo nginx -t
sudo systemctl reload nginx
const AppRouter = () => (
);
npm run build
sudo nginx -t && sudo systemctl reload nginx
cd ~/skystrike_9.3.10  # Or wherever your full project root is
# Step 1: Initialize if not already
git init
# Step 2: Add GitHub remote (only if not already set)
git remote add origin https://github.com/andrusym/skystrike-prod.git
# Step 3: Create new branch for this release
git checkout -b release-9.3.12
# Step 4: Add all files and commit
git add .
git commit -m "SkyStrike v9.3.12 full build"
# Step 5: Push to GitHub
git push origin release-9.3.12
# Make sure you're on the correct branch
git checkout release-9.3.12
# Add and commit anything new (if needed)
git add .
git commit -m "Retry push for SkyStrike v9.3.12 full build"
# Force push to ensure GitHub gets the full release
git push origin release-9.3.12 --force
git push https://andrusym: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@github.com/andrusym/skystrike-prod.git release-9.3.12
cd frontend
npm run build
sudo systemctl reload nginx
cd frontend
npm run build
sudo systemctl reload nginx
mv frontend/src/Sidebar.jsx frontend/src/components/Sidebar.jsx
mv src/Sidebar.jsx src/components/Sidebar.jsx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
npm run build
sudo systemctl reload nginx
git push https://andrusym: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@github.com/andrusym/skystrike-prod.git release-9.3.12
# 1. Make sure you're in your project directory
cd ~/skystrike_9.3.10/frontend
# 2. Checkout a new branch from current state
git checkout -b release-9.3.13
# 3. Stage all updated files
git add .
# 4. Commit your changes
git commit -m "Release 9.3.13 - Theme toggle fix and layout refinements"
# 5. Push the new release branch to GitHub
git push -u https://andrusym:YOUR_TOKEN@github.com/andrusym/skystrike-prod.git release-9.3.13
git push https://andrusym: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@github.com/andrusym/skystrike-prod.git release-9.3.13
npm run build
