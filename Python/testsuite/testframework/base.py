# -*- coding: utf-8 -*-
import logging
import time
import os

from testconfig import config
from unittest import TestCase
import requests
import json

class BaseTest(TestCase):


    logger = logging.getLogger('api_testsuite')
    if not os.path.exists('logs/api_testsuite.log'):os.mkdir('logs')
    handler = logging.FileHandler('logs/api_testsuite.log')
    formatter = logging.Formatter('%(asctime)s [%(testid)s] [%(levelname)s] %(message)s',
                                  '%d/%m/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.url = config['main']['url']


    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('api_testsuite'),
                                             {'testid': self.shortDescription().split(':')[0] or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.session = requests.Session()


    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        self.session.close()
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s Execution Time is %s sec.' % (self._testID, executionTime))


    def lg(self, msg):
        self._logger.info(msg)
        
        
    def get_request_response(self, uri, headers=None, payload=None):
        if headers == None: 
            headers = {"Content-Type": "application/json"}
        self.lg('GET %s' % self.url + uri)
        return self.session.get(self.url + uri, params=payload, headers=headers, timeout=30, allow_redirects=False)     


    def post_request_response(self, uri, data, headers=None):  
        if headers == None: 
            headers = {"Content-Type": "application/json"}
        self.lg('POST %s' % self.url + uri)
        return self.session.post(self.url + uri, data=json.dumps(data), headers=headers, timeout=30, allow_redirects=False)    


    def put_request_response(self, uri, data, headers=None):  
        if headers == None: 
            headers = {"Content-Type": "application/json"}
        self.lg('PUT %s' % self.url + uri)
        return self.session.put(self.url + uri, data=json.dumps(data), headers=headers, timeout=30, allow_redirects=False)        


    def delete_request_response(self, uri, headers=None):      
        if headers == None: 
            headers = {"Content-Type": "application/json"}
        self.lg('DELETE %s' % self.url + uri)
        return self.session.delete(self.url + uri, headers=headers, timeout=30, allow_redirects=False)