from jenkins_api import *
from jinja2 import PackageLoader,Environment,FileSystemLoader
import yaml
import re


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
        configs = {}
        msg = self.Generate_variables(ymlfilepath)
        j2_env = Environment(loader=FileSystemLoader('config'),
                             trim_blocks=True)
        template = j2_env.get_template('multibranch_config.xml')
        for i in msg[jobtype]:
            # 通过giturl地址，截取项目名称，以此命名jenkins job
            jobname = re.split(r'[\/,\.]',i['giturl'])[-2]
            rendered_file = template.render(i)
            configs[jobname] = rendered_file
        return configs

    def Create_jobs(self,ymlfilepath,jobtype):
        configs = self.Generate_config(ymlfilepath,jobtype)
        for jobname,config in configs.items():
           # print (config)
            self.server.create_job(jobname,config)
        
    def Delete_jobs(self,jobname):
        self.server.delete_job(jobname)

jm = (Jenkins_Manage())
#temp = jm.Generate_variables('config/defaults.yml')
temp = jm.Create_jobs('config/defaults.yml','multibranch_job')
print(temp)