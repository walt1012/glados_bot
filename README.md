# GLaDOS Check-in

使用 GitHub Actions 定时执行 GLaDOS 签到，并在 Actions 日志中输出签到结果和剩余天数。

## 使用方式

1. Fork 本仓库。
2. 在仓库的 `Settings > Secrets and variables > Actions` 中添加 secret：`COOKIE`：GLaDOS 登录后的 cookie。
3. 在 `Actions` 页面启用工作流。
4. 手动运行 `GLaDOS Check-in`，或等待定时任务自动触发。

## 本地运行

```bash
python -m pip install -r requirements.txt
COOKIE="your-cookie" python checkin.py
```

## 开发检查

```bash
python -m pip install -r requirements-dev.txt
ruff check .
ruff format .
```

## 工作流

默认触发方式：

- 手动触发：`workflow_dispatch`
- 推送到 `main` 分支
- 向 `main` 分支提交 Pull Request
- 每天 UTC 09:45 和 23:45 定时执行
