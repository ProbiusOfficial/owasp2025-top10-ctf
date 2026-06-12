# A10:2025 异常情况处理不当 ![icon](../assets/TOP_10_Icons_Final_Mishandling_of_Exceptional_Conditions.png){: style="height:80px;width:80px" align="right"}


## 背景

异常情况处理不当（Mishandling of Exceptional Conditions）是2025年的一个新类别。该类别包含24个CWE，聚焦于不当的错误处理、逻辑错误、安全失效（failing open）以及其他由异常条件和系统可能遇到的情况引发的相关场景。该类别包含一些以前与代码质量差相关的CWE。那对我们来说太笼统了；在我们看来，这个更具体的类别提供了更好的指导。

该类别包含的值得注意的CWE：*CWE-209 生成包含敏感信息的错误消息、CWE-234 未能处理缺失参数、CWE-274 对权限不足处理不当、CWE-476 空指针解引用*，以及 *CWE-636 未安全失效（'Failing Open'）*。


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
   <td>24
   </td>
   <td>20.67%
   </td>
   <td>2.95%
   </td>
   <td>100.00%
   </td>
   <td>37.95%
   </td>
   <td>7.11
   </td>
   <td>3.81
   </td>
   <td>769,581
   </td>
   <td>3,416
   </td>
  </tr>
</table>



## 描述

软件中异常情况处理不当发生在程序未能预防、检测和响应异常和不可预测的情况时，这会导致崩溃、意外行为，有时还会导致漏洞。这可能涉及以下三种失误中的一种或多种：应用程序没有阻止异常情况的发生，没有在情况发生时识别它，和/或之后对该情况的响应很差或根本没有响应。

 

异常情况可能由缺失、不完善或不完整的输入验证引起，或者由在错误发生的函数处进行延迟的高级别错误处理引起，或者由意外的环境状态（如内存、权限或网络问题）、不一致的异常处理，或完全未处理的异常引起，使系统陷入未知和不可预测的状态。每当应用程序不确定其下一条指令时，就说明异常情况已被处理不当。难以发现的错误和异常可能在很长时间内威胁整个应用程序的安全性。

 

当我们处理异常情况不当时，可能会发生许多不同的安全漏洞，

例如逻辑错误、溢出、竞争条件、欺诈性交易，或内存、状态、资源、时序、身份验证和授权方面的问题。这些类型的漏洞可能对系统或其数据的机密性、可用性和/或完整性产生负面影响。攻击者利用应用程序有缺陷的错误处理来攻击此漏洞。


## 预防措施

为了正确处理异常情况，我们必须为这种情况做好计划（做最坏的打算）。我们必须在错误发生的直接位置"捕获"每一个可能的系统错误，然后处理它（这意味着做一些有意义的事情来解决问题并确保我们从问题中恢复）。作为处理的一部分，我们应该包括抛出错误（以用户可以理解的方式通知用户）、记录事件，以及在我们认为合理的情况下发出告警。我们还应该有一个全局异常处理程序，以防我们遗漏了什么。理想情况下，我们还应该有监控和/或可观测性工具或功能，用于监视重复的错误或表明正在进行攻击的模式，并可以发出某种响应、防御或阻止。这可以帮助我们阻止和响应专注于我们错误处理弱点的脚本和机器人。

 

捕获和处理异常情况可以确保我们程序的底层基础设施不会被迫处理不可预测的情况。如果您正在进行任何类型的交易，极其重要的是回滚交易的每个部分并重新开始（也称为安全失效，failing closed）。试图在交易进行到一半时恢复它，往往是我们造成不可恢复错误的地方。

 

只要可能，在任何地方添加速率限制、资源配额、节流和其他限制，以首先防止异常情况的发生。信息技术中的任何事物都不应该是无限制的，因为这会导致缺乏应用程序弹性、拒绝服务、成功的暴力破解攻击以及巨额的云账单。

考虑是否应该以统计信息的形式输出相同重复的错误，仅显示它们发生的频率和时间范围，且仅当错误超过一定速率时。此信息应附加到原始消息中，以免干扰自动化的日志记录和监控，参见 [A09:2025 安全日志与告警失效](A09_2025-Security_Logging_and_Alerting_Failures.md)。

除此之外，我们还希望包括严格的输入验证（对必须接受的潜在危险字符进行消毒或转义），以及*集中式*的错误处理、日志记录、监控和告警，以及一个全局异常处理程序。一个应用程序不应该有多个处理异常情况的函数，它应该在一个地方、以相同的方式每次执行。我们还应该为本节中的所有建议创建项目安全需求，在设计阶段执行威胁建模和/或安全设计审查活动，执行代码审查或静态分析，以及对最终系统执行压力、性能和渗透测试。

 

如果可能，您的整个组织应该以相同的方式处理异常情况，因为这使得审查和审计代码中的错误变得更加容易，而这是一个重要的安全控制。


## 攻击场景示例

**场景 #1：** 如果应用程序在文件上传时捕获异常，但未正确释放资源，则可能通过异常情况处理不当导致资源耗尽（拒绝服务）。每个新异常都会使资源被锁定或以其他方式不可用，直到所有资源都被耗尽。

**场景 #2：** 通过不当处理或数据库错误将完整的系统错误暴露给用户，导致敏感数据泄露。攻击者继续强制产生错误，以便使用敏感的系统信息来创建更好的SQL注入攻击。用户错误消息中的敏感数据属于侦察信息。

**场景 #3：** 金融交易中的状态损坏可能由攻击者通过网络中断来打断多步骤交易造成。假设交易顺序为：借记用户账户、贷记目标账户、记录交易。如果系统在交易进行到一半出现错误时，没有正确地回滚整个交易（安全失效），攻击者可能会耗尽用户的账户，或者可能出现竞争条件，使攻击者能够多次向目标账户汇款。


## 参考资源

OWASP MASVS‑RESILIENCE

- [OWASP速查表：日志记录](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

- [OWASP速查表：错误处理](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

- [OWASP应用程序安全验证标准（ASVS）：V16.5 错误处理](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md#v165-error-handling)

- [OWASP测试指南：4.8.1 测试错误处理](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/01-Testing_For_Improper_Error_Handling)

* [异常最佳实践（Microsoft, .Net）](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions)

* [整洁代码与异常处理的艺术（Toptal）](https://www.toptal.com/developers/abap/clean-code-and-the-art-of-exception-handling)

* [通用错误处理规则（Google for Developers）](https://developers.google.com/tech-writing/error-messages/error-handling)

* [真实世界中异常情况处理不当的案例](https://www.firstreference.com/blog/human-error-and-internal-control-failures-cause-us62m-fine/) 

## 映射的CWE列表
* [CWE-209	生成包含敏感信息的错误消息](https://cwe.mitre.org/data/definitions/209.html)
* [CWE-215	将敏感信息插入调试代码](https://cwe.mitre.org/data/definitions/215.html)
* [CWE-234	未能处理缺失参数](https://cwe.mitre.org/data/definitions/234.html)
* [CWE-235	对额外参数处理不当](https://cwe.mitre.org/data/definitions/235.html)
* [CWE-248	未捕获的异常](https://cwe.mitre.org/data/definitions/248.html)
* [CWE-252	未检查的返回值](https://cwe.mitre.org/data/definitions/252.html)
* [CWE-274	对权限不足处理不当](https://cwe.mitre.org/data/definitions/274.html)
* [CWE-280	对权限或特权不足处理不当](https://cwe.mitre.org/data/definitions/280.html)
* [CWE-369	除以零](https://cwe.mitre.org/data/definitions/369.html)
* [CWE-390	检测到错误条件但未采取行动](https://cwe.mitre.org/data/definitions/390.html)
* [CWE-391	未检查的错误条件](https://cwe.mitre.org/data/definitions/391.html)
* [CWE-394	意外的状态码或返回值](https://cwe.mitre.org/data/definitions/394.html)
* [CWE-396	为通用异常声明Catch](https://cwe.mitre.org/data/definitions/396.html)
* [CWE-397	为通用异常声明Throws](https://cwe.mitre.org/data/definitions/397.html)
* [CWE-460	抛出异常时清理不当](https://cwe.mitre.org/data/definitions/460.html)
* [CWE-476	空指针解引用](https://cwe.mitre.org/data/definitions/476.html)
* [CWE-478	多条件表达式中缺少默认情况](https://cwe.mitre.org/data/definitions/478.html)
* [CWE-484	Switch中遗漏Break语句](https://cwe.mitre.org/data/definitions/484.html)
* [CWE-550	服务器生成的错误消息包含敏感信息](https://cwe.mitre.org/data/definitions/550.html)
* [CWE-636	未安全失效（'Failing Open'）](https://cwe.mitre.org/data/definitions/636.html)
* [CWE-703	对异常情况检查或处理不当](https://cwe.mitre.org/data/definitions/703.html)
* [CWE-754	对异常或特殊情况检查不当](https://cwe.mitre.org/data/definitions/754.html)
* [CWE-755	对异常情况处理不当](https://cwe.mitre.org/data/definitions/755.html)
* [CWE-756	缺少自定义错误页面](https://cwe.mitre.org/data/definitions/756.html)
