# TweetTrends


### 1. AWS configure
* aws_access_key_id = YOUR_ACCESS_KEY 
* aws_secret_access_key = YOUR_SECRET_KEY
* or we can just do that through program

### 2. Running Streamming Server
* `cd` into `streaming`
* Input the keys for Twitter in Streaming&Sending to SQS.py.
* Run `pip install -r requirements.txt` to install the needed packages
* Run `python Streaming&Sending to SQS.py`

### 3. Backend
* `cd` into `nodejs`, and run `npm install` to install the needed packages
* Modify the Elasticsearch endpoint in `app.js`
* Run `node app.js`

### 4. Elasticsearch & Worker
* `cd` into `worker`
* Run `python Create Standard Domain.py` to create a elasticsearch domain
* Change the access policy for this domain
* Input the endpoint for this domain in Worker+Pool.py
* Run `pip install -r requirements.txt` to install the needed packages
* Run `Worker+Pool.py &`
