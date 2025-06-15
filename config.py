import os
import sys
import yaml
from typing import Dict

def load_config() -> Dict:
    """
    从配置文件加载邮箱配置
    :return: 配置信息字典
    """
    # 获取可执行文件的实际路径
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        executable_path = sys.executable
        config_path = os.path.join(os.path.dirname(executable_path), 'config.yaml')
    else:
        # 如果是直接运行 Python 脚本
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    
    if not os.path.exists(config_path):
        raise Exception("配置文件不存在，请先创建 config.yaml 文件")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    if not config or 'email' not in config:
        raise ValueError("配置文件格式错误")
    
    if not config['email']['address'] or not config['email']['password']:
        raise ValueError("请在配置文件中填写邮箱地址和授权码")
    
    return config 