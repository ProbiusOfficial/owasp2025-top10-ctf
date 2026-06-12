# A02:2025 安全配置错误 ![icon](../assets/TOP_10_Icons_Final_Security_Misconfiguration.png){: style="height:80px;width:80px" align="right"}

## 背景

从上一版的第 5 位上升，100% 的被测应用程序都被发现存在某种形式的配置错误，平均发生率为 3.00%，该风险类别中通用缺陷枚举（CWE）的出现次数超过 719,000 次。随着越来越多地向高度可配置软件的转变，看到这一类别上升并不令人惊讶。值得注意的 CWE 包括 *CWE-16 配置* 和 *CWE-611 XML 外部实体引用限制不当（XXE）*。

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
   <td>16
   </td>
   <td>27.70%
   </td>
   <td>3.00%
   </td>
   <td>100.00%
   </td>
   <td>52.35%
   </td>
   <td>7.96
   </td>
   <td>3.97
   </td>
   <td>719,084
   </td>
   <td>1,375
   </td>
  </tr>
</table>

## 描述

安全配置错误是指系统、应用程序或云服务从安全角度设置不正确，从而产生漏洞。

如果出现以下情况，应用程序可能存在漏洞：

* 应用程序栈的任何部分缺少适当的安全加固，或云服务的权限配置不当。
* 启用了不必要的功能或安装了不必要的组件（例如，不必要的端口、服务、页面、账户、测试框架或权限）。
* 默认账户及其密码仍然启用且未更改。
* 缺少拦截过度错误消息的中心配置。错误处理向用户暴露堆栈跟踪或其他过于详细的错误消息。
* 对于升级后的系统，最新的安全功能被禁用或未安全配置。
* 过度优先考虑向后兼容性导致不安全的配置。
* 应用程序服务器、应用程序框架（例如 Struts、Spring、ASP.NET）、库、数据库等中的安全设置未设置为安全值。
* 服务器未发送安全头或指令，或未设置为安全值。

如果没有协调一致、可重复的应用程序安全配置加固流程，系统将面临更高的风险。

## 如何预防

应实施安全安装流程，包括：

* 可重复的加固流程，能够快速轻松地部署另一个经过适当锁定的环境。开发、QA 和生产环境应配置相同，但在每个环境中使用不同的凭证。此流程应自动化，以最小化设置新安全环境所需的工作量。
* 最小化平台，不包含任何不必要的功能、组件、文档或示例。删除或不安装未使用的功能和框架。
* 作为补丁管理流程的一部分，审查和更新适用于所有安全说明、更新和补丁的配置（参见 [A03 软件供应链失效](A03_2025-Software_Supply_Chain_Failures.md)）。审查云存储权限（例如，S3 存储桶权限）。
* 分段应用程序架构通过分段、容器化或云安全组（ACL）在组件或租户之间提供有效和安全的隔离。
* 向客户端发送安全指令，例如安全头。
* 自动化流程以验证所有环境中配置和设置的有效性。
* 主动添加中心配置以拦截过度错误消息作为备份。
* 如果这些验证未自动化，则至少应每年手动验证一次。
* 使用底层平台提供的身份联合、短期凭证或基于角色的访问机制，而不是在代码、配置文件或流水线中嵌入静态密钥或密钥。

## 攻击场景示例

**场景 #1：** 应用程序服务器自带的示例应用程序未从生产服务器中删除。这些示例应用程序具有已知的安全漏洞，攻击者利用这些漏洞来破坏服务器。假设其中一个应用程序是管理控制台，且默认账户未更改。在这种情况下，攻击者使用默认密码登录并接管服务器。

**场景 #2：** 服务器上未禁用目录列表。攻击者发现他们可以简单地列出目录。攻击者找到并下载编译后的 Java 类，对其进行反编译和逆向工程以查看代码。然后攻击者在应用程序中发现一个严重的访问控制缺陷。

**场景 #3：** 应用程序服务器的配置允许向用户返回详细的错误消息，例如堆栈跟踪。这可能暴露敏感信息或底层缺陷，例如已知存在漏洞的组件版本。

**场景 #4：** 云服务提供商（CSP）默认将共享权限开放给互联网。这允许访问存储在云存储中的敏感数据。

## 参考

* [OWASP 测试指南：配置管理](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/README)
* [OWASP 测试指南：错误代码测试](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/01-Testing_For_Improper_Error_Handling)
* [应用程序安全验证标准 V13 配置](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x22-V13-Configuration.md)
* [NIST 通用服务器加固指南](https://csrc.nist.gov/publications/detail/sp/800-123/final)
* [CIS 安全配置指南/基准](https://www.cisecurity.org/cis-benchmarks/)
* [Amazon S3 存储桶发现和枚举](https://blog.websecurify.com/2017/10/aws-s3-bucket-discovery.html)
* ScienceDirect：安全配置错误

## 映射的 CWE 列表

* [CWE-5 J2EE 配置错误：未加密传输数据](https://cwe.mitre.org/data/definitions/5.html)

* [CWE-11 ASP.NET 配置错误：创建调试二进制文件](https://cwe.mitre.org/data/definitions/11.html)

* [CWE-13 ASP.NET 配置错误：配置文件中的密码](https://cwe.mitre.org/data/definitions/13.html)

* [CWE-15 系统或配置设置的外部控制](https://cwe.mitre.org/data/definitions/15.html)

* [CWE-16 配置](https://cwe.mitre.org/data/definitions/16.html)

* [CWE-260 配置文件中的密码](https://cwe.mitre.org/data/definitions/260.html)

* [CWE-315 Cookie 中敏感信息的明文存储](https://cwe.mitre.org/data/definitions/315.html)

* [CWE-489 活动调试代码](https://cwe.mitre.org/data/definitions/489.html)

* [CWE-526 通过环境变量暴露敏感信息](https://cwe.mitre.org/data/definitions/526.html)

* [CWE-547 使用硬编码的安全相关常量](https://cwe.mitre.org/data/definitions/547.html)

* [CWE-611 XML 外部实体引用限制不当](https://cwe.mitre.org/data/definitions/611.html)

* [CWE-614 HTTPS 会话中敏感 Cookie 缺少 'Secure' 属性](https://cwe.mitre.org/data/definitions/614.html)

* [CWE-776 DTD 中递归实体引用限制不当（'XML 实体扩展'）](https://cwe.mitre.org/data/definitions/776.html)

* [CWE-942 与不可信域的宽松跨域策略](https://cwe.mitre.org/data/definitions/942.html)

* [CWE-1004 敏感 Cookie 缺少 'HttpOnly' 标志](https://cwe.mitre.org/data/definitions/1004.html)

* [CWE-1174 ASP.NET 配置错误：不正确的模型验证](https://cwe.mitre.org/data/definitions/1174.html)
