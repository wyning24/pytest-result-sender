from datetime import datetime, timedelta
import pytest


data = {


}


def pytest_configure():
    # 配置加载完毕之后执行，测试用例执行之前执行
    data['start_time'] = datetime.now()
    print(f"{datetime.now()} pytest开始执行")


def pytest_unconfigure():
    # 在配置卸载之后执行，所有测试用例执行后执行
    data['end_time'] = datetime.now()
    print(f"{datetime.now()} pytest结束执行")


    data['duration'] = data['end_time'] - data['start_time']
    print(data)
    assert timedelta(seconds=3) >= data['duration'] >= timedelta(seconds=2.5)
    assert data['total'] == 3