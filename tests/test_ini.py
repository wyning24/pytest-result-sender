from pathlib import Path

import pytest

from pytest_result_sender import plugin

pytest_plugins = "pytester"  # 我是测试开发


# 创建一个fixture，把用力变得干净。因为在测试中发现，通过的用例为3，为6，通过率为300%，600%，
# 这是不对的，实际原本只有一个测试用例
@pytest.fixture(autouse=True)
def mock():
    bak_data = plugin.data
    plugin.data = data = {"failed": 0, "passed": 0}
    # 测试之前，创建一个干净的测试环境
    yield
    # 恢复测试环境
    plugin.data = bak_data


@pytest.mark.parametrize("send_when", ["every", "on_fail"])
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path: Path):
    """

    :param send_when: 针对两个不同的的发送时间
    :param pytester: 这个用来测试自己
    :param tmp_path: 这个用来生成和保存临时的配置文件
    :return:
    """
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when = {send_when}
send_api = https://baidu.com   
    """
    )
    # """
    # 断言： 配置加载成功
    # """
    config = pytester.parseconfig(config_path)
    # 让pytester加载配置文件config_path，将配置结果保存在config。
    # 断言 配置文件中的内容，是否进入pytest的配置文件
    assert config.getini("send_when") == send_when  # 说明pytest得到的配置是准确定
    # """
    # 开始写测试用例,让pytester去执行
    # """
    pytester.makepyfile(  # 构造场景：用例全部测试通过
        """
        def test_pass():
            ...
        """
    )
    pytester.runpytest("-c", str(config_path))

    # 如何断言，插件有没有发送结果
    print(plugin.data)
    if send_when == "every":
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None


@pytest.mark.parametrize("send_api", ["https://baidu.com", ""])
def test_send_api(send_api, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when = every
send_api = {send_api}   
        """
    )
    # """
    # 断言： 配置加载成功
    # """
    config = pytester.parseconfig(config_path)
    # 让pytester加载配置文件config_path，将配置结果保存在config。
    # 断言 配置文件中的内容，是否进入pytest的配置文件
    assert config.getini("send_api") == send_api  # 说明pytest得到的配置是准确定
    # """
    # 开始写测试用例,让pytester去执行
    # """
    pytester.makepyfile(  # 构造场景：用例全部测试通过
        """
        def test_pass():
            ...
        """
    )
    pytester.runpytest("-c", str(config_path))

    # 如何断言，插件有没有发送结果
    print(plugin.data)
    if send_api:
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None
