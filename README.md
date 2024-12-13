# translation-mcp-server
多語言翻譯的 MCP 伺服器實作。

## 安裝需求
Python >= 3.12
uv - Python 套件安裝工具

## 安裝
使用 uv 安裝專案:
```bash
uv venv
uv pip install .
```

## 執行
安裝完成後，可使用以下指令啟動伺服器，確認是否能正常執行:
```bash
uv run mcp-translation-server
```

修改 claude_desktop_config.json 
```json
{
  "mcpServers": {
    "translation-flow": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "C:\\Users\\[here your user name]\\[here the project path]",
        "mcp-translation-server"
      ]
    }
  }
}
```