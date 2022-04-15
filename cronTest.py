import mysql.connector
import re
import os
import requests
import datetime
import time
import detailsExtractor
from bs4 import BeautifulSoup
import linkLists

print("success! " + format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))