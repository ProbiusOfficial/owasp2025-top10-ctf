# A07:2025 认证失败（Authentication Failures） ![icon](../assets/TOP_10_Icons_Final_Identification_and_Authentication_Failures.png){: style="height:80px;width:80px" align="right"}


## 背景

认证失败保持在第7位，名称略有更改，以更准确地反映该类别中的36个CWE。尽管标准化框架带来了好处，但该类别仍保持了自2021年以来的第7名排名。值得注意的CWE包括 *CWE-259 使用硬编码密码*、*CWE-297：证书与主机不匹配验证不当*、*CWE-287：认证不当*、*CWE-384：会话固定*，以及 *CWE-798 使用硬编码凭证*。


## 评分表


<table>
  <tr>
   <td>映射的CWE数量
   </td>
   <td>最大发生率
   </td>
   <td>平均发生率
   </td>
   <td>最大覆盖率
   </td>
   <td>平均覆盖率
   </td>
   <td>平均加权利用难度
   </td>
   <td>平均加权影响
   </td>
   <td>总出现次数
   </td>
   <td>总CVE数量
   </td>
  </tr>
  <tr>
   <td>36
   </td>
   <td>15.80%
   </td>
   <td>2.92%
   </td>
   <td>100.00%
   </td>
   <td>37.14%
   </td>
   <td>7.69
   </td>
   <td>4.44
   </td>
   <td>1,120,673
   </td>
   <td>7,147
   </td>
  </tr>
</table>



## 描述

当攻击者能够欺骗系统将无效或不正确的用户识别为合法用户时，就存在此漏洞。如果应用程序存在以下情况，则可能存在认证弱点：

* 允许自动化攻击，如凭证填充（credential stuffing），攻击者拥有泄露的有效用户名和密码列表。最近，这种类型的攻击已扩展到包括混合密码攻击凭证填充（也称为密码喷洒攻击），攻击者使用泄露凭证的变体或增量来尝试获得访问权限，例如尝试Password1!、Password2!、Password3!等。

* 允许暴力破解或其他自动化脚本攻击，且未被快速阻止。

* 允许使用默认、弱或众所周知的密码，例如"Password1"或用户名为"admin"且密码为"admin"。

* 允许用户使用已知已泄露的凭证创建新账户。

* 允许使用弱或无效的凭证恢复和忘记密码流程，例如"基于知识的答案"，这些无法做到安全。

* 使用明文、加密或弱哈希密码数据存储（参见[A04:2025-加密失败](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/)）。

* 缺少或无效的多因素认证。

* 如果多因素认证不可用，允许使用弱或无效的备用方案。

* 在URL、隐藏字段或其他客户端可访问的不安全位置中暴露会话标识符。

* 在成功登录后重复使用相同的会话标识符。

* 在注销或不活动期间未正确使用户会话或认证令牌（主要是单点登录（SSO）令牌）失效。

* 未正确断言所提供凭证的范围和预期受众。

## 如何预防

* 在可能的情况下，实施并强制使用多因素认证，以防止自动化凭证填充、暴力破解和被盗凭证重用攻击。

* 在可能的情况下，鼓励并启用密码管理器的使用，以帮助用户做出更好的选择。

* 不要随产品发布或部署任何默认凭证，特别是管理员用户。

* 实施弱密码检查，例如针对前10,000个最糟糕密码列表测试新密码或更改后的密码。

* 在新账户创建和密码更改期间，针对已知泄露凭证列表进行验证（例如：使用[haveibeenpwned.com](https://haveibeenpwned.com)）。

* 将密码长度、复杂度和轮换策略与[美国国家标准与技术研究院（NIST）800-63b中第5.1.1节的记忆秘密指南](https://pages.nist.gov/800-63-3/sp800-63b.html#:~:text=5.1.1%20Memorized%20Secrets)或其他现代的、基于证据的密码策略保持一致。

* 除非怀疑发生泄露，否则不要强制人类轮换密码。如果怀疑发生泄露，立即强制重置密码。

* 确保注册、凭证恢复和API路径通过对所有结果使用相同的消息（"用户名或密码无效。"）来加固，以防止账户枚举攻击。

* 限制或逐渐增加失败的登录尝试，但要注意不要创建拒绝服务场景。记录所有失败，并在检测到或怀疑发生凭证填充、暴力破解或其他攻击时向管理员发出警报。

* 使用服务器端、安全的内置会话管理器，在登录后生成具有高熵的新随机会话ID。会话标识符不应出现在URL中，应安全地存储在安全cookie中，并在注销、空闲和绝对超时后失效。

* 理想情况下，使用预先制作的、广受信任的系统来处理认证、身份和会话管理。尽可能通过购买和使用经过加固和充分测试的系统来转移此风险。

* 验证所提供凭证的预期用途，例如对于JWT，验证`aud`、`iss`声明和范围


## 攻击场景示例

**场景 #1：** 凭证填充，即使用已知的用户名和密码组合列表，现在是一种非常常见的攻击。最近，攻击者被发现基于常见的人类行为"递增"或以其他方式调整密码。例如，将'Winter2025'改为'Winter2026'，或'ILoveMyDog6'改为'ILoveMyDog7'或'ILoveMyDog5'。这种密码尝试的调整称为混合凭证填充攻击或密码喷洒攻击，它们可能比传统版本更有效。如果应用程序没有实施针对自动化威胁（暴力破解、脚本或机器人）或凭证填充的防御措施，该应用程序可以被用作密码预言机来确定凭证是否有效，并获得未经授权的访问。

**场景 #2：** 大多数成功的认证攻击是由于继续将密码作为唯一的认证因素使用。曾经被认为是最佳实践的密码轮换和复杂度要求鼓励用户既重用密码又使用弱密码。组织建议根据NIST 800-63停止这些做法，并在所有重要系统上强制使用多因素认证。

**场景 #3：** 应用程序会话超时未正确实现。用户使用公共计算机访问应用程序，没有选择"注销"，而是直接关闭浏览器标签页然后离开。另一个例子是，如果单点登录（SSO）会话无法通过单点注销（SLO）关闭。也就是说，一次登录让您进入例如您的邮件阅读器、文档系统和聊天系统。但注销只发生在当前系统。如果攻击者在受害者认为已成功注销后使用同一浏览器，但用户仍然对某些应用程序保持认证状态，则可以访问受害者的账户。当敏感应用程序未正确退出且同事可以（临时）访问未锁定的计算机时，同样的问题也可能发生在办公室和企业中。

## 参考资料

* [OWASP认证速查表](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

* [OWASP安全编码实践](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/01-introduction/05-introduction)


## 映射的CWE列表

* [CWE-258 配置文件中的空密码](https://cwe.mitre.org/data/definitions/258.html)

* [CWE-259 使用硬编码密码](https://cwe.mitre.org/data/definitions/259.html)

* [CWE-287 认证不当](https://cwe.mitre.org/data/definitions/287.html)

* [CWE-288 使用备用路径或通道绕过认证](https://cwe.mitre.org/data/definitions/288.html)

* [CWE-289 通过备用名称绕过认证](https://cwe.mitre.org/data/definitions/289.html)

* [CWE-290 通过欺骗绕过认证](https://cwe.mitre.org/data/definitions/290.html)

* [CWE-291 依赖IP地址进行认证](https://cwe.mitre.org/data/definitions/291.html)

* [CWE-293 使用Referer字段进行认证](https://cwe.mitre.org/data/definitions/293.html)

* [CWE-294 通过捕获-重放绕过认证](https://cwe.mitre.org/data/definitions/294.html)

* [CWE-295 证书验证不当](https://cwe.mitre.org/data/definitions/295.html)

* [CWE-297 证书与主机不匹配验证不当](https://cwe.mitre.org/data/definitions/297.html)

* [CWE-298 证书与主机不匹配验证不当](https://cwe.mitre.org/data/definitions/298.html)

* [CWE-299 证书与主机不匹配验证不当](https://cwe.mitre.org/data/definitions/299.html)

* [CWE-300 非端点可访问的通道](https://cwe.mitre.org/data/definitions/300.html)

* [CWE-302 通过假设不可变数据绕过认证](https://cwe.mitre.org/data/definitions/302.html)

* [CWE-303 认证算法实现不正确](https://cwe.mitre.org/data/definitions/303.html)

* [CWE-304 认证中缺少关键步骤](https://cwe.mitre.org/data/definitions/304.html)

* [CWE-305 通过主要弱点绕过认证](https://cwe.mitre.org/data/definitions/305.html)

* [CWE-306 关键功能缺少认证](https://cwe.mitre.org/data/definitions/306.html)

* [CWE-307 过度认证尝试限制不当](https://cwe.mitre.org/data/definitions/307.html)

* [CWE-308 使用单因素认证](https://cwe.mitre.org/data/definitions/308.html)

* [CWE-309 使用密码系统进行主要认证](https://cwe.mitre.org/data/definitions/309.html)

* [CWE-346 来源验证错误](https://cwe.mitre.org/data/definitions/346.html)

* [CWE-350 依赖反向DNS解析执行安全关键操作](https://cwe.mitre.org/data/definitions/350.html)

* [CWE-384 会话固定](https://cwe.mitre.org/data/definitions/384.html)

* [CWE-521 弱密码要求](https://cwe.mitre.org/data/definitions/521.html)

* [CWE-613 会话过期不足](https://cwe.mitre.org/data/definitions/613.html)

* [CWE-620 未验证的密码更改](https://cwe.mitre.org/data/definitions/620.html)

* [CWE-640 忘记密码的弱密码恢复机制](https://cwe.mitre.org/data/definitions/640.html)

* [CWE-798 使用硬编码凭证](https://cwe.mitre.org/data/definitions/798.html)

* [CWE-940 通信通道来源验证不当](https://cwe.mitre.org/data/definitions/940.html)

* [CWE-941 通信通道中目标指定不正确](https://cwe.mitre.org/data/definitions/941.html)

* [CWE-1390 弱认证](https://cwe.mitre.org/data/definitions/1390.html)

* [CWE-1391 使用弱凭证](https://cwe.mitre.org/data/definitions/1391.html)

* [CWE-1392 使用默认凭证](https://cwe.mitre.org/data/definitions/1392.html)

* [CWE-1393 使用默认密码](https://cwe.mitre.org/data/definitions/1393.html)
