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

    def Get_jobs(self,jobname):
        jobs = self.server.get_jobs()
        for news in jobs:
            if news['name'] == jobname:
                return True
            else:
                continue
    def Generate_variables(self,ymlfilepath):
        '''
            导入yaml文件，生成变量，使用config/defaults.yml
        '''
        with open(ymlfilepath,'r') as f:
            temp = yaml.load(f.read())
        return temp

    def Generate_job_config(self,ymlfilepath,jobtype):
        '''
            生成job的 xml格式配置文件，以job名为key，xml内容为值
        '''
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

    def Create_jobs(self,jobheader,ymlfilepath,jobtype):
        configs = self.Generate_job_config(ymlfilepath,jobtype)
        for jobname,config in configs.items():
            self.server.create_job(jobname,config)

    def Generate_view_config(self,ymlfilepath,jobtype):
        '''
            生成view的 xml格式配置文件，以view名为key，xml内容为值
        '''
        configs = {}
        msg = self.Generate_variables(ymlfilepath)
        j2_env = Environment(loader=FileSystemLoader('config'),
                             trim_blocks=True)
        template = j2_env.get_template('view_config.xml')
        for i in msg[jobtype]:
            viewname = i['viewname']
            rendered_file = template.render(i)
            configs[viewname] = rendered_file
        return configs

    def Create_view(self,ymlfilepath,jobtype):
        '''
            使用view时，通过编辑view的配置中的Regular expression项设置正则匹配表达式自动关联job，因此，直接使用新的模板即可
        '''
        configs = self.Generate_view_config(ymlfilepath,jobtype)
        for viewname,config in configs.items():
           # print(viewname,config)
            self.server.create_view(viewname,config)
        

    def Delete_jobs(self,jobname):
        self.server.delete_job(jobname)
    
    def Get_view_config(self,viewname):
        config =  self.server.get_view_config(viewname)
        print(config)

jm = (Jenkins_Manage())
temp = jm.Create_jobs('config/defaults.yml','multibranch_job')
#temp = jm.Create_view('test','config/view_config.xml','view_template')
temp = jm.Create_view('config/defaults.yml','view_template')
temp = jm.Get_version()
print(temp)