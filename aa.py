import requests

url = "https://tongyi.aliyun.com/?st=null&sessionId=938bb4fc62f34a7497f7e884f306ac01"

# url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c1d0282b-6994-9e0a-0378dcbf2514'
content = """
pytest自动化测试结果<br>
测试时间：xxxx-xxx<br> 
用例数量：100<br>
执行时长：5s<br>
测试通过数量：<font color='blue'>2</font> <br>
测试失败数量：<font color='red'>1</font> <br>
测试通过率：66.67%<br>
测试报告地址：http://baidu.com
"""
requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
