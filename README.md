Android-CleanResource
==================

批量删除lint提示的无用资源 Batch remove unused resources of  lint hint 


#################################################
环境: win + python2.7

Author: changqiang

Email: hcq0618@163.com

说明：

1、使用前先clean工程，确保工程bin下重新生成dex，以便lint进行分析。

2、如果清除资源后，工程缺少文件而报错（极少情况），尝试通过svn恢复该文件即可。

3、修改配置文件clean_lint_config.ini中的路径即可使用，其中：

projectPath：项目路径

lintPath：Android SDK目录中lint.bat的路径 一般为Android SDK目录下tools目录中

4、配置文件中filterkeys为过滤的关键字集合 默认过滤Android项目中values和layout目录下的资源

支持自定义添加 格式为：关键字1|关键字2 即以|分割

5、可利用cxFreeze、py2exe、pyInstaller等工具将py文件打包转成exe执行文件

#################################################

