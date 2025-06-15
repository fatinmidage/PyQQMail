# PyQQMail

一个用于处理 QQ 邮箱的 Python 工具。

## 功能特点

- 自动处理 QQ 邮箱邮件
- 支持邮件过滤和分类
- 提供便捷的邮件管理功能

## 安装说明

1. 克隆仓库
```bash
git clone https://github.com/yourusername/PyQQMail.git
cd PyQQMail
```

2. 安装 uv（推荐）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/macOS
```

# 安装依赖
uv sync
source .venv/bin/activate
```

或者使用传统的 pip（不推荐）：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 配置说明

1. 复制配置文件模板
```bash
cp config.yaml.template config.yaml
```

2. 编辑 `config.yaml` 文件，填入你的实际配置信息：
   - QQ 邮箱账号
   - 授权码（不是 QQ 密码）
   - 其他相关配置

3. 确保 `config.yaml` 不会被提交到 Git：
   - 检查 `.gitignore` 文件中是否包含 `config.yaml`
   - 如果已提交，请参考下面的"安全说明"部分

## 安全说明

⚠️ 重要：请勿将包含真实账号密码的 `config.yaml` 文件提交到 Git 仓库！

如果已经提交了敏感信息：
1. 立即更改所有泄露的密码和授权码
2. 使用以下命令从 Git 历史中删除敏感文件：
```bash
git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch config.yaml" \
--prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```

## 使用说明

1. 确保已完成配置
2. 运行主程序：
```bash
python main.py
```

## 注意事项

- 请妥善保管你的配置文件
- 定期更新授权码
- 建议使用环境变量存储敏感信息
- 推荐使用 uv 进行包管理，它比传统的 pip 更快、更可靠

## 许可证

MIT License
