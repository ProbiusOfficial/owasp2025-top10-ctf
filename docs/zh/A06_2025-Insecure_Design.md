# A06:2025 不安全设计（Insecure Design） ![icon](../assets/TOP_10_Icons_Final_Insecure_Design.png){: style="height:80px;width:80px" align="right"}


## 背景

不安全设计从第4名下滑两位至第6名，因为**[A02:2025-安全配置错误](A02_2025-Security_Misconfiguration.md)**和**[A03:2025-软件供应链失败](A03_2025-Software_Supply_Chain_Failures.md)**超越了它。该类别于2021年引入，我们已经看到行业在威胁建模方面有了显著改进，并且对安全设计的重视程度更高。该类别关注与设计和架构缺陷相关的风险，呼吁更多地使用威胁建模、安全设计模式和参考架构。这包括应用程序业务逻辑中的缺陷，例如缺乏对应用程序内部不需要或意外状态变更的定义。作为一个社区，我们需要超越编码空间中的"左移"，延伸到编码前的活动，如需求编写和应用程序设计，这些对于安全设计原则至关重要（例如，参见**[建立现代AppSec计划：规划和设计阶段](0x03_2025-Establishing_a_Modern_Application_Security_Program.md)**）。值得注意的通用弱点枚举（CWE）包括 *CWE-256：凭证未受保护存储、CWE-269 权限管理不当、CWE-434 危险类型文件的无限制上传、CWE-501：信任边界违反，以及 CWE-522：凭证保护不足。*


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
   <td>39
   </td>
   <td>22.18%
   </td>
   <td>1.86%
   </td>
   <td>88.76%
   </td>
   <td>35.18%
   </td>
   <td>6.96
   </td>
   <td>4.05
   </td>
   <td>729,882
   </td>
   <td>7,647
   </td>
  </tr>
</table>



## 描述

不安全设计是一个广泛的类别，代表不同的弱点，表现为"缺失或无效的控制设计"。不安全设计并非所有其他Top Ten风险类别的根源。请注意，不安全设计和不安全实现之间存在区别。我们区分设计缺陷和实现缺陷是有原因的，它们有不同的根本原因，在开发过程的不同阶段发生，并且有不同的补救措施。安全的设计仍然可能存在实现缺陷，导致可能被利用的漏洞。不安全的设计无法通过完美的实现来修复，因为所需的安全控制从未被创建以防御特定攻击。导致不安全设计的因素之一是所开发软件或系统中缺乏固有的业务风险分析，因此未能确定需要何种级别的安全设计。

拥有安全设计的三个关键部分是：

* 需求收集和资源管理
* 创建安全设计
* 拥有安全开发生命周期


### 需求与资源管理

与业务部门一起收集和协商应用程序的业务需求，包括关于所有数据资产的机密性、完整性、可用性和真实性的保护需求，以及预期的业务逻辑。考虑您的应用程序将暴露的程度，以及是否需要租户隔离（超出访问控制所需的部分）。编制技术需求，包括功能性和非功能性安全需求。规划和协商涵盖所有设计、构建、测试和运营（包括安全活动）的预算。


### 安全设计

安全设计是一种文化和方法论，持续评估威胁并确保代码经过稳健设计和测试，以防止已知的攻击方法。威胁建模应集成到细化会议（或类似活动）中；寻找数据流和访问控制或其他安全控制的变化。在故事开发中，确定正确的流程和失败状态，确保它们被相关方充分理解和同意。分析预期流程和失败流程的假设和条件，以确保它们保持准确和可取。确定如何验证假设并强制执行正确行为所需的条件。确保结果记录在故事中。从错误中学习，并提供积极的激励以促进改进。安全设计既不是附加组件，也不是可以添加到软件中的工具。


### 安全开发生命周期

安全软件需要安全开发生命周期、安全设计模式、铺平道路（paved road）方法论、安全组件库、适当的工具、威胁建模，以及用于改进流程的事件事后分析。在软件项目开始时、整个项目期间以及持续的软件维护期间，请联系您的安全专家。考虑利用[OWASP软件保证成熟度模型（SAMM）](https://owaspsamm.org/)来帮助构建您的安全软件开发工作。

开发人员的自我责任常常被低估。培养一种意识、责任和主动风险缓解的文化。关于安全的定期交流（例如在威胁建模会议期间）可以形成一种将安全纳入所有重要设计决策的心态。


## 如何预防



* 与AppSec专业人员一起建立和使用安全开发生命周期，以帮助评估和设计安全和隐私相关的控制
* 建立并使用安全设计模式或铺平道路组件库
* 对应用程序的关键部分（如认证、访问控制、业务逻辑和关键流程）使用威胁建模
* 将威胁建模作为教育工具，以培养安全思维
* 将安全语言和控制集成到用户故事中
* 在应用程序的每一层（从前端到后端）集成合理性检查
* 编写单元测试和集成测试，以验证所有关键流程都能抵抗威胁模型。为应用程序的每一层编译用例*和*滥用用例
* 根据暴露程度和保护需求，在系统和网络层隔离层级
* 通过设计在所有层级中稳健地隔离租户


## 攻击场景示例

**场景 #1：** 凭证恢复工作流程可能包含"安全问题与答案"，这是NIST 800-63b、OWASP ASVS和OWASP Top 10所禁止的。安全问题与答案不能作为身份证据被信任，因为多个人可能知道答案。此类功能应被移除并替换为更安全的设计。

**场景 #2：** 一家电影院连锁允许团体预订折扣，最多十五名参与者，超过则需要押金。攻击者可以对此流程进行威胁建模，并测试是否能在应用程序的业务逻辑中找到攻击向量，例如通过少量请求一次性预订六百个座位和所有电影院，导致巨大的收入损失。

**场景 #3：** 一家零售连锁的电子商务网站没有针对黄牛党运行的机器人进行防护，这些机器人购买高端显卡以在拍卖网站上转售。这给显卡制造商和零售连锁所有者带来了糟糕的公众形象，并与无法以任何价格获得这些显卡的爱好者产生了持久的恶感。仔细的防机器人设计和领域逻辑规则，例如在可用性发布后几秒钟内完成的购买，可能识别出不真实的购买并拒绝此类交易。


## 参考资料



* [OWASP速查表：安全设计原则](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html)
* [OWASP SAMM：设计 | 安全架构](https://owaspsamm.org/model/design/secure-architecture/)
* [OWASP SAMM：设计 | 威胁评估](https://owaspsamm.org/model/design/threat-assessment/)
* [NIST – 开发者软件验证最低标准指南](https://www.nist.gov/publications/guidelines-minimum-standards-developer-verification-software)
* [威胁建模宣言](https://threatmodelingmanifesto.org/)
* [Awesome Threat Modeling](https://github.com/hysnsec/awesome-threat-modelling)


## 映射的CWE列表

* [CWE-73 文件名或路径的外部控制](https://cwe.mitre.org/data/definitions/73.html)

* [CWE-183 允许的输入宽松列表](https://cwe.mitre.org/data/definitions/183.html)

* [CWE-256 凭证未受保护存储](https://cwe.mitre.org/data/definitions/256.html)

* [CWE-266 权限分配不正确](https://cwe.mitre.org/data/definitions/266.html)

* [CWE-269 权限管理不当](https://cwe.mitre.org/data/definitions/269.html)

* [CWE-286 用户管理不正确](https://cwe.mitre.org/data/definitions/286.html)

* [CWE-311 敏感数据缺少加密](https://cwe.mitre.org/data/definitions/311.html)

* [CWE-312 敏感信息明文存储](https://cwe.mitre.org/data/definitions/312.html)

* [CWE-313 文件或磁盘上的明文存储](https://cwe.mitre.org/data/definitions/313.html)

* [CWE-316 内存中敏感信息明文存储](https://cwe.mitre.org/data/definitions/316.html)

* [CWE-362 使用共享资源进行并发执行且同步不当（'竞态条件'）](https://cwe.mitre.org/data/definitions/362.html)

* [CWE-382 J2EE不良实践：使用System.exit()](https://cwe.mitre.org/data/definitions/382.html)

* [CWE-419 未受保护的主通道](https://cwe.mitre.org/data/definitions/419.html)

* [CWE-434 危险类型文件的无限制上传](https://cwe.mitre.org/data/definitions/434.html)

* [CWE-436 解释冲突](https://cwe.mitre.org/data/definitions/436.html)

* [CWE-444 HTTP请求解释不一致（'HTTP请求走私'）](https://cwe.mitre.org/data/definitions/444.html)

* [CWE-451 用户界面（UI）对关键信息的错误表示](https://cwe.mitre.org/data/definitions/451.html)

* [CWE-454 可信变量或数据存储的外部初始化](https://cwe.mitre.org/data/definitions/454.html)

* [CWE-472 对假设不可变的Web参数的外部控制](https://cwe.mitre.org/data/definitions/472.html)

* [CWE-501 信任边界违反](https://cwe.mitre.org/data/definitions/501.html)

* [CWE-522 凭证保护不足](https://cwe.mitre.org/data/definitions/522.html)

* [CWE-525 使用包含敏感信息的Web浏览器缓存](https://cwe.mitre.org/data/definitions/525.html)

* [CWE-539 使用包含敏感信息的持久Cookie](https://cwe.mitre.org/data/definitions/539.html)

* [CWE-598 使用带有敏感查询字符串的GET请求方法](https://cwe.mitre.org/data/definitions/598.html)

* [CWE-602 服务器端安全的客户端强制执行](https://cwe.mitre.org/data/definitions/602.html)

* [CWE-628 函数调用参数指定不正确](https://cwe.mitre.org/data/definitions/628.html)

* [CWE-642 关键状态数据的外部控制](https://cwe.mitre.org/data/definitions/642.html)

* [CWE-646 依赖外部提供文件的文件名或扩展名](https://cwe.mitre.org/data/definitions/646.html)

* [CWE-653 隔离不足](https://cwe.mitre.org/data/definitions/653.html)

* [CWE-656 依赖通过隐蔽实现安全](https://cwe.mitre.org/data/definitions/656.html)

* [CWE-657 违反安全设计原则](https://cwe.mitre.org/data/definitions/657.html)

* [CWE-676 使用潜在危险函数](https://cwe.mitre.org/data/definitions/676.html)

* [CWE-693 保护机制失效](https://cwe.mitre.org/data/definitions/693.html)

* [CWE-799 交互频率控制不当](https://cwe.mitre.org/data/definitions/799.html)

* [CWE-807 在安全决策中依赖不受信任的输入](https://cwe.mitre.org/data/definitions/807.html)

* [CWE-841 行为工作流执行不当](https://cwe.mitre.org/data/definitions/841.html)

* [CWE-1021 对渲染的UI层或框架限制不当](https://cwe.mitre.org/data/definitions/1021.html)

* [CWE-1022 使用带有window.opener访问权限的不可信目标的Web链接](https://cwe.mitre.org/data/definitions/1022.html)

* [CWE-1125 攻击面过大](https://cwe.mitre.org/data/definitions/1125.html)
