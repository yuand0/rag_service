# W12（10.17 – 10.23）计划

## 目标
将 W10 冻结的 C++ `.so` 手动导入 RAG 项目，验证 ABI 兼容性。

## 待办
- [ ] 复制 `cpp_core.so` 到 `rag_service/cpp_lib/`
- [ ] 编写 `app/services/cpp_bridge.py` 封装调用
- [ ] 用 C++ 分词器替换默认分词
- [ ] 用 C++ 余弦相似度替换 Chroma 默认相似度
- [ ] 模拟 RAG 向量比对，记录耗时
- [ ] 排查 ABI 兼容性问题

## 风险
- C++ `.so` 依赖的 Python 版本与当前不一致
- GLIBC 版本不匹配
- 编译时未加 `-fPIC`
