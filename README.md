#项目简介  

项目框架通过python+unittest+requests+Yaml+PyMysql+Utils工具类和数据驱动理念进行业务脚本的编写
目录结果分为 如下

      data（数据层）  
      log（日志文件）  
      run_main(运行主函数入口以系统为纬度)  
      public（业务公共方法，如登陆）  
      report（html报告存放）  
      testcases(系统业务层逻辑的编写)  
      utils(工具类拓展)  


##核心目录详细介绍  
data  

       通过yaml文件进行接口用例的数据维护  
       config_common.yaml:维护系统的域名，以及数据库链接信息  

test_cases  

    里面是以系统为纬度进行划分  
    每个系统下有对应case模块，通过继承unittest.Testcase基类进行业务层逻辑的方法编写以及调用  

    主要包含：  

        1、setup初始化进行yaml数据读取  

        2、业务层自定义方法  

        3、方法组装  

        
run_main  

    以系统为纬度划分，对应一个个py模块  

    通过Unittest.Testsuite()把业务层的方法导入加载到测试套件中执行  

    然后通过sys.argv方法进行环境区分执行py文件  

    获取测试结果html文件  

    bs4模块提取html关键标签信息,获取执行的结果  

    再执行企业微信消息获取报告之后进行消息反馈  

utils  

    工具包内部包含：  
        数据库链接操作  
        时间戳获取  
        读文件操作  
        企业微信机器人发送消息  
        log文件写入  
        根目录路径获取
        
        框架扩展的功能都在工具类中实现
    
##编写流程  
    新用户编写思路  

    前置条件：功能用例选择回归场景后梳理出涉及接口  

       1、data数据层通过yaml文件编写接口用例  
       
       2、test_cases，进行业务层方法编写   
    
       3、把业务层方法导入到run_main目录下对应的py文件，通过testsuite进行加载用例然后执行用例  

    
   
