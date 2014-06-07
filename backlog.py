'''
Usage:
python3 backlog.py issues.csv

Reference: http://www.backlog.jp/api/
'''

BACKLOG_USER = ''
BACKLOG_PASS = ''
BACKLOG_HOST = '' # Ex: abc.backlog.jp
DEBUG = False

import sys
import csv
from xmlrpc.client import ServerProxy

class BacklogAPI:
    client = None
    
    def __init__(self, user, passwd, host):
        url = 'https://{0}:{1}@{2}/XML-RPC'.format(user, passwd, host)
        self.client = ServerProxy(url, verbose=DEBUG)
    
    def import_issue(self, csv_path):
        with open(csv_path) as f:
            reader = csv.reader(f)
            for row in reader:
                self._add_issue(row)
                print(row)
                
    def _add_issue(self, detail):
        (no,project,summary,description,parent_id,due_date,assigner,priority) = detail
        arg = dict()
        arg['projectId'] = self.get_projectid(project)
        arg['summary'] = summary
        arg['description'] = description
        if (parent_id):
            arg['parent_issue_id'] = parent_id
        if (due_date):
            arg['due_date'] = due_date
        if (assigner):
            arg['assignerId'] = self.get_userid(assigner)
        if (priority):
            arg['priorityId'] = priority
        
        self.call('backlog.createIssue', arg)
        
    def get_userid(self, name):
        ''' name should be the login id'''
        response = self.call('backlog.getUser', name)
        return response.id
        
    def get_projectid(self, name):
        ''' project name is slug of project '''
        response = self.call('backlog.getProject', name)
        return response.id
        
    def call(self, key, *args):
        func = getattr(self.client, key)
        return func(*args)
    
if __name__ == "__main__":
    csv_path = None
    try:
        csv_path = sys.argv[1]
        api = BacklogAPI(BACKLOG_USER, BACKLOG_PASS)
        api.import_issue(csv_path)
    except IndexError:
        print("Please specify issues in CSV format")
        sys.exit(2)
    