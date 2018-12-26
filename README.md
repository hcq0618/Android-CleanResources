# Android-CleanResources

当项目越来越大时，无用资源可能会越来越多
如果每个都是手动删除，不但可能删错，查找和删除文件也很麻烦，
所以需要一个脚本工具来批量删除lint分析的无用资源

As the project gets bigger, there may be more and more unused resources,
If each is manually deleted, not only might it be wrong to delete, but also to find and delete files is very troublesome,
Therefore, a script tool is needed to batch remove lint analysis of unused resources

- - -

python2.7

- - -

**clean_res.py**

1. 使用前先clean工程，确保工程bin下重新生成dex，以便lint进行分析。
	At first clean your project
1. 修改配置文件clean_lint_config.ini中的路径即可使用，其中：

	Modify the content of 'clean_lint_config.ini' file，including:

    **projectPath**：项目路径

    **lintPath**：Android SDK目录中lint命令行的路径，一般为Android SDK目录下tools目录中

    **filterKeys**：过滤的关键字集合，默认过滤Android项目中values和layout目录下的资源，
    支持自定义添加，格式为：关键字1|关键字2，即以‘|’分割

    **projectPath**：your project directory path

    **lintPath**：the lint comand file path in Android SDK directory，and generally, it is in the tools directory under the Android SDK directory

    **filterKeys**: By default, the resources under values and layout directories in the Android project are filtered,Support custom add, and the format is: keyword 1| keyword 2 is divided by '|'

- - -

说明：
- 可利用cxFreeze、py2exe、pyInstaller等工具将py文件打包转成exe执行文件

	You can use cxFreeze, py2exe, pyInstaller and other tools to package py files and turn them into exe executables
- 如果清除资源后，工程缺少文件而报错（极少情况），尝试通过svn/git恢复该文件即可

	If the project reports an error (in rare cases) due to a lack of files after clearing resources, try to restore the file through SVN /Git
- 也可以选择在Android Studio中使用 Menu > Refactor > Remove Unused Resources

	Alternatively, you can also use Menu > Refactor > Remove Unused Resources in Android Studio
- 也可以选择在gradle中配置

	You can also add the configuration in gradle

```
buildTypes {
    release {
        minifyEnabled true
        shrinkResources true
    }
```


## License

MIT License

Copyright (c) 2017 Hcq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
