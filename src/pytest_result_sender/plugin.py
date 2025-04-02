from datetime import datetime

import pytest
import requests

data = {"failed": 0, "passed": 0}


def pytest_collection_finish(session: pytest.Session) -> None:
    # 这个钩子：用例加载完成之后执行，包含了全部的用例
    data["total"] = len(session.items)
    print(f"用例的总数为：{data['total']}")


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    # 这个钩子：在每个用例执行完成之后执行
    if report.when == "call":
        print("本次用例的执行结果是：", report.outcome)
        data[report.outcome] += 1


def pytest_configure():
    # 配置加载完毕之后执行，测试用例执行之前执行
    data["start_time"] = datetime.now()
    print(f"{datetime.now()} pytest开始执行")


def pytest_unconfigure():
    # 在配置卸载之后执行，所有测试用例执行后执行
    data["end_time"] = datetime.now()
    data["pass_ratio"] = data["passed"] / data["total"] * 100
    data["pass_ratio"] = f"{data['pass_ratio']:.2f}%"
    print(f"成功率：{data['pass_ratio']}")
    print(f"{datetime.now()} pytest结束执行")

    data["duration"] = data["end_time"] - data["start_time"]
    print(data)
    # 这一部分是单元测试
    # assert timedelta(seconds=3.2) >= data['duration'] >= timedelta(seconds=2.5)
    # assert data['total'] == 3
    # assert data['passed'] == 2
    # assert data['pass_ratio'] == '66.67%'

    url = (
        "https://tongyi.aliyun.com/?st=null&sessionId=938bb4fc62f34a7497f7e884f306ac01"
    )

    # url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c1d0282b-6994-9e0a-0378dcbf2514'
    content = f"""
    pytest自动化测试结果<br>
    测试时间：{data['end_time']} 
    用例数量：{data['total']}<br>
    执行时长：{data['duration']}s<br>
    测试通过数量：<font color='blue'>{data['passed']}</font> <br>
    测试失败数量：<font color='red'>{data['failed']}</font> <br>
    测试通过率：{data['pass_ratio']}<br>
    测试报告地址：http://baidu.com
    """
    requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
