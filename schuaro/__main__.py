import uvicorn
from schuaro import app
import os

if __name__ == "__main__":
    uvicorn.run("schuaro:app", host="0.0.0.0", port=8000, log_level="info", reload=os.environ.get('schuaro_dev')=='True')