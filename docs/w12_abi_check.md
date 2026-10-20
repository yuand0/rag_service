# W12: C++ .so ABI 兼容性验证（2026.10.18）

## 环境
- Python 3.12.3
- WSL Ubuntu 24.04
- cpp_core.cpython-312-x86_64-linux-gnu.so

## 验证结果
- [x] `cpp_core.so` 可导入
- [x] Tokenizer 正常工作
- [x] Calculator 正常工作
- [x] 已接入 Chroma 检索链路

## 关键观察
- C++ 分词器在检索前对查询进行预处理
- 分词结果 `' '.join(tokens)` 提升中文检索效果
- 无 ABI 兼容性问题

## 日志示例
[C++]原始查询:什么是人工智能->分词后:什 么 是 人工智能