#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port 8000
export API_KEY="-_k7HtLtIyxUuh2HMj5mSVSvpFUxzYYkmD8asOniC3U"

#!/bin/bash
python3 encryption_utils.py --init
exec uvicorn main:app --host 0.0.0.0 --port 10000
