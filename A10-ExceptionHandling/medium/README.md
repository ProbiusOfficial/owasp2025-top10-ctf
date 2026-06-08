# A10-ExceptionHandling - Medium

## 题目名称
失败开放 (Fail Open)

## 题目描述

这是一个用户管理系统。管理员区域保存着重要的flag。

系统提示：认证检查模块正在升级中，遇到异常时会自动放行以避免用户体验受损。

你能利用这个设计获取flag吗？

## 访问方式

- Web: `http://<target>:<port>/`

## 提示

- 注意观察认证检查逻辑中的异常处理方式
- 不是所有输入都会被数据库正常处理
- 尝试给系统一些"意外"的输入

## 题目考点

- OWASP A10: Mishandling of Exceptional Conditions
- 异常处理导致的安全状态不一致（Fail Open）
- 防御性编程中的设计缺陷
