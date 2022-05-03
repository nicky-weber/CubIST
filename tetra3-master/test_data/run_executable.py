import subprocess
import sys

result = subprocess.run([sys.executable])
"""sys.executable is the absolute path to the Python executable 
that your program was originally invoked with. 
For example, sys.executable might be a path like /usr/local/bin/python
"""