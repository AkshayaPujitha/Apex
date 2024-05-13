virtualenv demoenv -p python3
source demoenv/bin/activate
pip install -r requirements.txt
python utils/server.py