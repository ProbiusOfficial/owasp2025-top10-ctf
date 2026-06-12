# A08:2025 软件与数据完整性失效 ![icon](../assets/TOP_10_Icons_Final_Software_and_Data_Integrity_Failures.png){: style="height:80px;width:80px" align="right"}

## 背景

软件与数据完整性失效（Software or Data Integrity Failures）继续位列第8位，名称从"Software *and* Data Integrity Failures"微调为"Software *or* Data Integrity Failures"，以使其含义更加明确。该类别关注的是未能维护信任边界以及未能验证软件、代码和数据构件的完整性，其关注层面比软件供应链失效（Software Supply Chain Failures）更低。该类别聚焦于在软件更新和关键数据方面做出假设，却未验证其完整性。值得注意的常见弱点枚举（CWE）包括 *CWE-829：包含来自不可信控制域的功能*、*CWE-915：对动态确定的对象属性进行不当控制的修改*，以及 *CWE-502：不可信数据的反序列化*。


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
   <td>14
   </td>
   <td>8.98%
   </td>
   <td>2.75%
   </td>
   <td>78.52%
   </td>
   <td>45.49%
   </td>
   <td>7.11
   </td>
   <td>4.79
   </td>
   <td>501,327
   </td>
   <td>3,331
   </td>
  </tr>
</table>



## 描述

软件与数据完整性失效涉及代码和基础设施未能防止无效或不可信的代码或数据被当作可信和有效的数据来处理。一个例子是应用程序依赖于来自不可信来源、仓库和内容分发网络（CDN）的插件、库或模块。一个不安全的CI/CD流水线，如果没有进行软件完整性检查就消费和提供软件，可能会引入未授权访问、不安全或恶意代码或系统被入侵的潜在风险。另一个例子是CI/CD从不可信的地方拉取代码或构件，和/或在使用前未对其进行验证（通过检查签名或类似机制）。最后，许多应用程序现在包含自动更新功能，更新在下载时缺乏足够的完整性验证，就被应用到先前受信任的应用程序上。攻击者可能会上传他们自己的更新，使其被分发并在所有安装实例上运行。另一个例子是对象或数据被编码或序列化为一种结构，攻击者可以看到并修改这种结构，从而容易受到不安全的反序列化攻击。


## 预防措施



* 使用数字签名或类似机制来验证软件或数据来自预期来源，且未被篡改。
* 确保库和依赖项（如npm或Maven）仅从受信任的仓库获取。如果您的风险状况较高，请考虑托管一个经过审查的内部已知良好仓库。
* 确保对代码和配置更改有审查流程，以尽量减少恶意代码或配置被引入软件流水线的可能性。
* 确保您的CI/CD流水线具有适当的隔离、配置和访问控制，以确保流经构建和部署过程的代码的完整性。
* 确保不会从不可信的客户端接收未签名或未加密的序列化数据，并在未进行某种形式的完整性检查或数字签名以检测序列化数据被篡改或重放的情况下使用它。


## 攻击场景示例

**场景 #1 包含来自不可信来源的Web功能：** 一家公司使用外部服务提供商来提供支持功能。为了方便，它将 `myCompany.SupportProvider.com` DNS映射到 `support.myCompany.com`。这意味着在 `myCompany.com` 域上设置的所有Cookie（包括身份验证Cookie）现在都会被发送到该支持提供商。任何能够访问支持提供商基础设施的人都可以窃取所有访问过 `support.myCompany.com` 的用户的Cookie，并执行会话劫持攻击。

**场景 #2 未经签名的更新：** 许多家用路由器、机顶盒、设备固件等在更新时不验证已签名的固件。未签名固件正成为攻击者日益增长的攻击目标，预计情况只会变得更糟。这是一个重大问题，因为很多时候除了在未来版本中修复并等待旧版本淘汰之外，没有其他补救机制。

**场景 #3 使用来自不可信来源的软件包：** 一名开发者在寻找他们需要的软件包的更新版本时遇到困难，因此他们没有从常规的、受信任的包管理器下载，而是从一个在线网站下载。该软件包未签名，因此没有机会确保其完整性。该软件包包含恶意代码。

**场景 #4 不安全的反序列化：** 一个React应用程序调用一组Spring Boot微服务。作为函数式程序员，他们试图确保其代码是不可变的。他们想到的解决方案是将用户状态序列化，并在每次请求中来回传递。攻击者注意到"rO0" Java对象签名（base64编码），并使用 [Java Deserialization Scanner](https://github.com/federicodotta/Java-Deserialization-Scanner) 在应用服务器上获得远程代码执行权限。

## 参考资源

* [OWASP速查表：软件供应链安全](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)
* [OWASP速查表：基础设施即代码](https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet.html)
* [OWASP速查表：反序列化](https://wiki.owasp.org/index.php/Deserialization_Cheat_Sheet)
* [SAFECode软件完整性控制](https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf)
* ["最糟糕的噩梦"网络攻击：SolarWinds黑客事件未公开的故事](https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack)
* [CodeCov Bash上传器被入侵事件](https://about.codecov.io/security-update)
* [Securing DevOps，作者：Julien Vehent](https://www.manning.com/books/securing-devops)
* [Tenendo：不安全的反序列化](https://tenendo.com/insecure-deserialization/)


## 映射的CWE列表

* [CWE-345 数据真实性验证不足](https://cwe.mitre.org/data/definitions/345.html)

* [CWE-353 缺少完整性检查支持](https://cwe.mitre.org/data/definitions/353.html)

* [CWE-426 不可信的搜索路径](https://cwe.mitre.org/data/definitions/426.html)

* [CWE-427 不受控制的搜索路径元素](https://cwe.mitre.org/data/definitions/427.html)

* [CWE-494 下载代码时缺少完整性检查](https://cwe.mitre.org/data/definitions/494.html)

* [CWE-502 不可信数据的反序列化](https://cwe.mitre.org/data/definitions/502.html)

* [CWE-506 嵌入恶意代码](https://cwe.mitre.org/data/definitions/506.html)

* [CWE-509 复制恶意代码（病毒或蠕虫）](https://cwe.mitre.org/data/definitions/509.html)

* [CWE-565 依赖Cookie而不进行验证和完整性检查](https://cwe.mitre.org/data/definitions/565.html)

* [CWE-784 在安全决策中依赖Cookie而不进行验证和完整性检查](https://cwe.mitre.org/data/definitions/784.html)

* [CWE-829 包含来自不可信控制域的功能](https://cwe.mitre.org/data/definitions/829.html)

* [CWE-830 包含来自不可信来源的Web功能](https://cwe.mitre.org/data/definitions/830.html)

* [CWE-915 对动态确定的对象属性进行不当控制的修改](https://cwe.mitre.org/data/definitions/915.html)

* [CWE-926 Android应用程序组件的不当导出](https://cwe.mitre.org/data/definitions/926.html)
