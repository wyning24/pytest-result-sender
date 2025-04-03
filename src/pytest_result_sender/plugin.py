from datetime import datetime
from tkinter import getint

import pytest
import requests

data = {"failed": 0, "passed": 0}

def pytest_addoption(parser):
    # 用来添加配置
    parser.addini(
        'send_when',
        help="何时发送结果，每一次都发送every；或者 on_fail失败的时候发送"
    )
    parser.addini(
        'send_api',
        help="测试结果发往何处"
    )


def pytest_collection_finish(session: pytest.Session) -> None:
    # 这个钩子：用例加载完成之后执行，包含了全部的用例
    data["total"] = len(session.items)
    print(f"用例的总数为：{data['total']}")


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    # 这个钩子：在每个用例执行完成之后执行
    if report.when == "call":
        print("本次用例的执行结果是：", report.outcome)
        data[report.outcome] += 1


def pytest_configure(config:pytest.Config) -> None:
    # 当代码执行到这里，表示所有的配置项，已经加载完成.
    # 配置加载完毕之后执行，测试用例执行之前执行    ------说明可以读取到配置项目
    data["start_time"] = datetime.now()
    data['send_when'] = config.getini("send_when")
    data['send_api'] = config.getini("send_api") #这样就可以使用全局变量来获取
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
    send_result()

def send_result():
    if data['send_when'] == 'on_fail' and data['failed'] == 0:
        # 如果配置 只有测试失败才发送，但实际没有失败，则不发送
        return
    if not data['send_api']:
        # 如果没有配置api地址，则不发送测试结果
        return




    url = data['send_api'] #动态指定结果的发送位置
    content = f"""
    pytest自动化测试结果耶<br>
    测试时间：{data['end_time']} 
    用例数量：{data['total']}<br>
    执行时长：{data['duration']}s<br>
    测试通过数量：<font color='blue'>{data['passed']}</font> <br>
    测试失败数量：<font color='red'>{data['failed']}</font> <br>
    测试通过率：{data['pass_ratio']}<br>
    测试报告地址：https://baidu.com
    """
    try:
        requests.post(url, json={"msgtype": "markdown",
                                 "markdown": {"content": content}})
    except Exception:
        pass