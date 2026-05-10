import sys
from pathlib import Path

from asgiref.wsgi import WsgiToAsgi

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import main

app = WsgiToAsgi(main.app)
