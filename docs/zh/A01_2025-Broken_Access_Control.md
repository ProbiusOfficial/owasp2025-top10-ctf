# A01:2025 失效的访问控制 ![icon](../assets/TOP_10_Icons_Final_Broken_Access_Control.png){: style="height:80px;width:80px" align="right"}

## 背景

在 Top Ten 中保持第 1 的位置，100% 的被测应用程序都被发现存在某种形式的失效访问控制。值得注意的 CWE 包括 *CWE-200：向未授权参与者暴露敏感信息*、*CWE-201：通过发送数据暴露敏感信息*、*CWE-918 服务器端请求伪造（SSRF）* 以及 *CWE-352：跨站请求伪造（CSRF）*。该类别在贡献数据中的出现次数最多，相关 CVE 数量排名第二。

## 评分表

<table>
  <tr>
   <td>映射的 CWE
   </td>
   <td>最大发生率
   </td>
   <td>平均发生率
   </td>
   <td>最大覆盖率
   </td>
   <td>平均覆盖率
   </td>
   <td>平均加权可利用性
   </td>
   <td>平均加权影响
   </td>
   <td>总出现次数
   </td>
   <td>总 CVE 数
   </td>
  </tr>
  <tr>
   <td>40
   </td>
   <td>20.15%
   </td>
   <td>3.74%
   </td>
   <td>100.00%
   </td>
   <td>42.93%
   </td>
   <td>7.04
   </td>
   <td>3.84
   </td>
   <td>1,839,701
   </td>
   <td>32,654
   </td>
  </tr>
</table>

## 描述

访问控制强制执行策略，使用户不能在其预期权限之外行事。失效通常会导致未经授权的信息披露、修改或销毁所有数据，或执行超出用户限制的业务功能。常见的访问控制漏洞包括：

* 违反最小权限原则，通常称为默认拒绝，即访问应仅授予特定功能、角色或用户，但却对任何人开放。
* 通过修改 URL（参数篡改或强制浏览）、内部应用程序状态或 HTML 页面，或使用修改 API 请求的攻击工具来绕过访问控制检查。
* 通过提供唯一标识符允许查看或编辑他人的账户（不安全的直接对象引用）
* 可访问的 API 缺少对 POST、PUT 和 DELETE 的访问控制。
* 权限提升。在未登录的情况下充当用户，或获得超出登录用户预期权限的权限（例如管理员访问权限）。
* 元数据操纵，例如重放或篡改 JSON Web Token（JWT）访问控制令牌、被操纵以提升权限的 cookie 或隐藏字段，或滥用 JWT 失效机制。
* CORS 错误配置允许来自未授权或不可信来源的 API 访问。
* 强制浏览（猜测 URL）以未认证用户身份访问认证页面，或以标准用户身份访问特权页面。

## 如何预防

访问控制只有在可信的服务器端代码或无服务器 API 中实施时才有效，攻击者无法修改访问控制检查或元数据。

* 除公共资源外，默认拒绝。
* 一次性实现访问控制机制，并在整个应用程序中重用它们，包括最小化跨域资源共享（CORS）的使用。
* 模型访问控制应强制执行记录所有权，而不是允许用户创建、读取、更新或删除任何记录。
* 独特的应用程序业务限制需求应由领域模型强制执行。
* 禁用 Web 服务器目录列表，并确保文件元数据（例如 .git）和备份文件不存在于 Web 根目录中。
* 记录访问控制失效，在适当时向管理员发出告警（例如重复失效）。
* 对 API 和控制器访问实施速率限制，以最小化自动化攻击工具造成的危害。
* 有状态会话标识符应在注销后在服务器上失效。无状态 JWT 令牌应是短寿命的，以最小化攻击者的机会窗口。对于寿命较长的 JWT，请考虑使用刷新令牌并遵循 OAuth 标准来撤销访问权限。
* 使用提供简单、声明式访问控制的成熟工具包或模式。

开发人员和 QA 人员应在单元测试和集成测试中包含功能性访问控制。

## 攻击场景示例

**场景 #1：** 应用程序在访问账户信息的 SQL 调用中使用未经验证的数据：

```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery( );
```

攻击者可以简单地修改浏览器的 'acct' 参数以发送任何所需的账户号码。如果未正确验证，攻击者可以访问任何用户的账户。

```
https://example.com/app/accountInfo?acct=notmyacct
```

**场景 #2：** 攻击者简单地强制浏览器访问目标 URL。访问管理页面需要管理员权限。

```
https://example.com/app/getappInfo
https://example.com/app/admin_getappInfo
```

如果未认证用户可以访问任一页面，这就是一个缺陷。如果非管理员可以访问管理页面，这也是一个缺陷。

**场景 #3：** 应用程序将所有访问控制放在其前端。虽然攻击者由于浏览器中运行的 JavaScript 代码无法访问 `https://example.com/app/admin_getappInfo`，但他们可以简单地执行：

```
$ curl https://example.com/app/admin_getappInfo
```

从命令行执行。

## 参考

* [OWASP 主动控制：C1：实施访问控制](https://top10proactive.owasp.org/archive/2024/the-top-10/c1-accesscontrol/)
* [OWASP 应用程序安全验证标准：V8 授权](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md)
* [OWASP 测试指南：授权测试](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/README)
* [OWASP 速查表：授权](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
* [PortSwigger：利用 CORS 错误配置](https://portswigger.net/blog/exploiting-cors-misconfigurations-for-bitcoins-and-bounties)
* [OAuth：撤销访问](https://www.oauth.com/oauth2-servers/listing-authorizations/revoking-access/)

## 映射的 CWE 列表

* [CWE-22 对受限目录的路径名限制不当（'路径遍历'）](https://cwe.mitre.org/data/definitions/22.html)

* [CWE-23 相对路径遍历](https://cwe.mitre.org/data/definitions/23.html)

* [CWE-36 绝对路径遍历](https://cwe.mitre.org/data/definitions/36.html)

* [CWE-59 文件访问前链接解析不当（'链接跟随'）](https://cwe.mitre.org/data/definitions/59.html)

* [CWE-61 UNIX 符号链接（Symlink）跟随](https://cwe.mitre.org/data/definitions/61.html)

* [CWE-65 Windows 硬链接](https://cwe.mitre.org/data/definitions/65.html)

* [CWE-200 向未授权参与者暴露敏感信息](https://cwe.mitre.org/data/definitions/200.html)

* [CWE-201 通过发送数据暴露敏感信息](https://cwe.mitre.org/data/definitions/201.html)

* [CWE-219 在 Web 根目录下存储包含敏感数据的文件](https://cwe.mitre.org/data/definitions/219.html)

* [CWE-276 不正确的默认权限](https://cwe.mitre.org/data/definitions/276.html)

* [CWE-281 权限的不当保留](https://cwe.mitre.org/data/definitions/281.html)

* [CWE-282 所有权管理不当](https://cwe.mitre.org/data/definitions/282.html)

* [CWE-283 未验证的所有权](https://cwe.mitre.org/data/definitions/283.html)

* [CWE-284 访问控制不当](https://cwe.mitre.org/data/definitions/284.html)

* [CWE-285 授权不当](https://cwe.mitre.org/data/definitions/285.html)

* [CWE-352 跨站请求伪造（CSRF）](https://cwe.mitre.org/data/definitions/352.html)

* [CWE-359 向未授权参与者暴露私人个人信息](https://cwe.mitre.org/data/definitions/359.html)

* [CWE-377 不安全的临时文件](https://cwe.mitre.org/data/definitions/377.html)

* [CWE-379 在权限不安全的目录中创建临时文件](https://cwe.mitre.org/data/definitions/379.html)

* [CWE-402 将私人资源传输到新领域（'资源泄漏'）](https://cwe.mitre.org/data/definitions/402.html)

* [CWE-424 替代路径的不当保护](https://cwe.mitre.org/data/definitions/424.html)

* [CWE-425 直接请求（'强制浏览'）](https://cwe.mitre.org/data/definitions/425.html)

* [CWE-441 非预期的代理或中介（'混淆副手'）](https://cwe.mitre.org/data/definitions/441.html)

* [CWE-497 向未授权控制领域暴露敏感系统信息](https://cwe.mitre.org/data/definitions/497.html)

* [CWE-538 将敏感信息插入外部可访问的文件或目录](https://cwe.mitre.org/data/definitions/538.html)

* [CWE-540 源代码中包含敏感信息](https://cwe.mitre.org/data/definitions/540.html)

* [CWE-548 通过目录列表暴露信息](https://cwe.mitre.org/data/definitions/548.html)

* [CWE-552 文件或目录可被外部方访问](https://cwe.mitre.org/data/definitions/552.html)

* [CWE-566 通过用户控制的 SQL 主键绕过授权](https://cwe.mitre.org/data/definitions/566.html)

* [CWE-601 URL 重定向到不可信站点（'开放重定向'）](https://cwe.mitre.org/data/definitions/601.html)

* [CWE-615 源代码注释中包含敏感信息](https://cwe.mitre.org/data/definitions/615.html)

* [CWE-639 通过用户控制的密钥绕过授权](https://cwe.mitre.org/data/definitions/639.html)

* [CWE-668 将资源暴露给错误领域](https://cwe.mitre.org/data/definitions/668.html)

* [CWE-732 关键资源的不正确权限分配](https://cwe.mitre.org/data/definitions/732.html)

* [CWE-749 暴露危险方法或函数](https://cwe.mitre.org/data/definitions/749.html)

* [CWE-862 缺少授权](https://cwe.mitre.org/data/definitions/862.html)

* [CWE-863 不正确的授权](https://cwe.mitre.org/data/definitions/863.html)

* [CWE-918 服务器端请求伪造（SSRF）](https://cwe.mitre.org/data/definitions/918.html)

* [CWE-922 敏感信息的不安全存储](https://cwe.mitre.org/data/definitions/922.html)

* [CWE-1275 具有不正确 SameSite 属性的敏感 Cookie](https://cwe.mitre.org/data/definitions/1275.html)
