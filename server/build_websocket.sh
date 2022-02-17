cd dash_websocket || exit
rm dist/dash_websocket-*.tar.gz
npm install
pip3 install -r requirements.txt
npm run build
python3 setup.py sdist
cd ..
pip3 install dash_websocket/dist/dash_websocket-*.tar.gz