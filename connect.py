import os
import requests
requests.packages.urllib3.disable_warnings()
redshift_endpoint = 'redditcluster.czkbdecget38.us-west-2.redshift.amazonaws.com'
redshift_user = os.getenv("REDSHIFT_USERNAME")
redshift_pass = os.getenv("REDSHIFT_PASSWORD")
port = 5439
dbname = 'dev'
from sqlalchemy import create_engine
engine_string = "postgresql+psycopg2://%s:%s@%s:%d/%s" \
% (redshift_user, redshift_pass, redshift_endpoint, port, dbname)
engine = create_engine(engine_string)