cd dash_websocket || exit
source venv/bin/activate
npm run build
python setup.py sdist
deactivate
cd ..
source venv/bin/activate
pip install dash_websocket/dist/dash_websocket-*.tar.gz