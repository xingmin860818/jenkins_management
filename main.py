from jenkins_api import *
from jinja2 import PackageLoader,Environment,FileSystemLoader
import yaml

class Jenkins_Manage(object):
    def __init__(self):
        "init jenkins connection"
        self.server = Jenkins("http://127.0.0.1:8080",username='wayne',password='123456')
    def Get_version(self):
        version = self.server.get_version()
        return version
    def Get_views(self,viewname):
        views = self.server.get_views()
        for news in views:
            if news['name'] == viewname:
                return True
            else:
                continue
    def Create_view(self,viewname):
        check_view = self.Get_views(viewname)
        if check_view == None:
            try:
                self.server.create_view(viewname,EMPTY_VIEW_CONFIG_XML)
                return True
            except Exception as e:
                return False
        else:
            return False
    def Get_jobs(self,jobname):
        jobs = self.server.get_jobs()
        for news in jobs:
            if news['name'] == jobname:
                return True
            else:
                continue
    def Generate_variables(self,ymlfilepath):
        with open(ymlfilepath,'r') as f:
            temp = yaml.load(f.read())
        return temp
    def Generate_config(self,ymlfilepath,jobtype):
        msg = self.Generate_variables(ymlfilepath)
        j2_env = Environment(loader=FileSystemLoader('config'),
                             trim_blocks=True)

        template = j2_env.get_template('multibranch_config.xml')
        length = len(msg[jobtype])
        for i in range(length):
            print(msg[jobtype][i])
            rendered_file = template.render(msg[jobtype][i])
            print('+++++++++++++++++++++++++++++++++++++++')
            print (rendered_file)
    def Create_jobs(self,jobname):
        check_job = self.Get_jobs(jobname)
        if check_job == None:
            try:
                self.server.create_job(jobname,EMPTY_CONFIG_XML)
                return True
            except Exception as e:
                return False
        else:
            return False
        
        
    def Delete_jobs(self,jobname):
        self.server.delete_job(jobname)

jm = (Jenkins_Manage())
temp = jm.Generate_config('config/defaults.yml','multibranch_job')
print(temp)