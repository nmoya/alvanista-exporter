alvanista-exporter
==================

Python3 application to export your public game list from http://alvanista.com

This may serve as backup or the input to another software that load your game library to another game tracker website

### Usage
- Clone this repository
- Create a virtual environment `python3 -m venv venv`
- Activate it: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run: `python app.py <alvanista_username> <finished|have|want>`
- `alvanista_username.txt` and `alvanista_username.json` files will be created
