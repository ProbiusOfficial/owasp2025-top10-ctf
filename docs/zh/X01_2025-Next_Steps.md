# 后续步骤

按照设计，OWASP Top 10本质上仅限于十大最重大的风险。每一份OWASP Top 10都有"濒临入选"的风险，这些风险经过长时间的考虑才决定是否纳入，但最终未能入选。其他风险更为普遍且影响更大。

以下三个问题非常值得投入精力去识别和修复，对于致力于建立成熟应用安全程序的组织、安全咨询公司，或希望扩展其产品覆盖范围的工具供应商而言都是如此。


## X01:2025 缺乏应用程序弹性

### 背景

这是2021年"拒绝服务"（Denial of Service）的重新命名。之所以改名，是因为原来的名称描述的是一种症状而非根本原因。该类别聚焦于描述与弹性问题相关的弱点的CWE。该类别的评分与A10:2025-异常情况处理不当非常接近。相关的CWE包括：*CWE-400 不受控制的资源消耗、CWE-409 对高度压缩数据（数据放大）处理不当、CWE-674 不受控制的递归*，以及 *CWE-835 带有不可达退出条件的循环（'无限循环'）。*


### 评分表


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
   <td>16
   </td>
   <td>20.05%
   </td>
   <td>4.55%
   </td>
   <td>86.01%
   </td>
   <td>41.47%
   </td>
   <td>7.92
   </td>
   <td>3.49
   </td>
   <td>865,066
   </td>
   <td>4,423
   </td>
  </tr>
</table>



### 描述

该类别代表了应用程序在应对压力、故障和边缘情况时的系统性弱点，这些情况导致应用程序无法从故障中恢复。当应用程序不能优雅地处理、承受或从意外条件、资源限制和其他不利事件中恢复时，很容易导致可用性问题（最常见），但也可能导致数据损坏、敏感数据泄露、级联故障和/或安全控制被绕过。

此外，[X02:2025 内存管理失效](#x022025-memory-management-failures) 也可能导致应用程序甚至整个系统的故障。

### 预防措施

为了防止这类漏洞，您必须为系统的故障和恢复进行设计。

* 添加限制、配额和故障转移功能，特别关注最消耗资源的操作
* 识别资源密集型页面并提前规划：减少攻击面，特别是不向未知或不可信用户暴露不需要的"小工具"和需要大量资源（如CPU、内存）的功能
* 执行严格的输入验证，使用允许列表和大小限制，然后进行全面测试
* 限制响应大小，并且永远不要将原始响应发送回客户端（在服务器端处理）
* 默认安全/关闭（永远不要开放），默认拒绝，如果出错则回滚
* 避免在请求线程中进行阻塞式同步调用（使用异步/非阻塞，设置超时，设置并发限制等）
* 仔细测试您的错误处理功能
* 实施弹性模式，如熔断器（circuit breakers）、舱壁（bulkheads）、重试逻辑和优雅降级
* 进行性能和负载测试；如果您有承担风险的能力，添加混沌工程
* 在合理且负担得起的范围内，实施和架构冗余
* 实施监控、可观测性和告警
* 按照RFC 2267过滤无效的发件人地址
* 通过指纹、IP或动态行为阻止已知的僵尸网络
* 工作量证明（Proof-of-Work）：在*攻击者*端启动消耗资源的操作，这对正常用户影响不大，但会影响试图发送大量请求的机器人。如果系统的总体负载增加，则使工作量证明更加困难，特别是对于不太可信或看起来像是机器人的系统
* 根据不活动时间和最终超时限制服务器端会话时间
* 限制会话绑定信息存储


### 攻击场景示例

**场景 #1：** 攻击者故意消耗应用程序资源以触发系统内的故障，导致拒绝服务。这可能是内存耗尽、磁盘空间填满、CPU饱和或打开无限连接。

**场景 #2：** 输入模糊测试导致精心构造的响应破坏应用程序业务逻辑。

**场景 #3：** 攻击者专注于应用程序的依赖项，使API或其他外部服务瘫痪，而应用程序无法继续运行。


### 参考资源

* [OWASP速查表：拒绝服务](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html)
* [OWASP MASVS‑RESILIENCE](https://mas.owasp.org/MASVS/11-MASVS-RESILIENCE/)
* [ASP.NET Core最佳实践（Microsoft）](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-9.0)
* [微服务中的弹性：舱壁 vs 熔断器（Parser）](https://medium.com/@parserdigital/resilience-in-microservices-bulkhead-vs-circuit-breaker-54364c1f9d53)
* [舱壁模式（Geeks for Geeks）](https://www.geeksforgeeks.org/system-design/bulkhead-pattern/)
* [NIST网络安全框架（CSF）](https://www.nist.gov/cyberframework)
* [避免阻塞调用：在Java中使用异步（Devlane）](https://www.devlane.com/blog/avoid-blocking-calls-go-async-in-java)

### 映射的CWE列表
* [CWE-73  文件名或路径的外部控制](https://cwe.mitre.org/data/definitions/73.html)
* [CWE-183 允许的输入许可列表过于宽松](https://cwe.mitre.org/data/definitions/183.html)
* [CWE-256 明文存储密码](https://cwe.mitre.org/data/definitions/256.html)
* [CWE-266 权限分配不正确](https://cwe.mitre.org/data/definitions/266.html)
* [CWE-269 权限管理不当](https://cwe.mitre.org/data/definitions/269.html)
* [CWE-286 用户管理不正确](https://cwe.mitre.org/data/definitions/286.html)
* [CWE-311 敏感数据缺少加密](https://cwe.mitre.org/data/definitions/311.html)
* [CWE-312 敏感信息明文存储](https://cwe.mitre.org/data/definitions/312.html)
* [CWE-313 文件或磁盘上的明文存储](https://cwe.mitre.org/data/definitions/313.html)
* [CWE-316 内存中敏感信息明文存储](https://cwe.mitre.org/data/definitions/316.html)
* [CWE-362 使用共享资源进行并发执行且同步不当（'竞争条件'）](https://cwe.mitre.org/data/definitions/362.html)
* [CWE-382 J2EE不良实践：使用System.exit()](https://cwe.mitre.org/data/definitions/382.html)
* [CWE-419 未受保护的主通道](https://cwe.mitre.org/data/definitions/419.html)
* [CWE-434 危险类型文件的不受限制上传](https://cwe.mitre.org/data/definitions/434.html)
* [CWE-436 解释冲突](https://cwe.mitre.org/data/definitions/436.html)
* [CWE-444 HTTP请求/响应的不一致解释（'HTTP请求/响应走私'）](https://cwe.mitre.org/data/definitions/444.html)
* [CWE-451 用户界面（UI）对关键信息的错误表示](https://cwe.mitre.org/data/definitions/451.html)
* [CWE-454 可信变量或数据存储的外部初始化](https://cwe.mitre.org/data/definitions/454.html)
* [CWE-472 对假定不可变的Web参数的外部控制](https://cwe.mitre.org/data/definitions/472.html)
* [CWE-501 信任边界违反](https://cwe.mitre.org/data/definitions/501.html)
* [CWE-522 凭证保护不足](https://cwe.mitre.org/data/definitions/522.html)
* [CWE-525 使用包含敏感信息的Web浏览器缓存](https://cwe.mitre.org/data/definitions/525.html)
* [CWE-539 使用包含敏感信息的持久性Cookie](https://cwe.mitre.org/data/definitions/539.html)
* [CWE-598 使用GET请求方法发送敏感查询字符串](https://cwe.mitre.org/data/definitions/598.html)
* [CWE-602 客户端强制执行服务器端安全](https://cwe.mitre.org/data/definitions/602.html)
* [CWE-628 函数调用时参数指定不正确](https://cwe.mitre.org/data/definitions/628.html)
* [CWE-642 关键状态数据的外部控制](https://cwe.mitre.org/data/definitions/642.html)
* [CWE-646 依赖外部提供文件的文件名或扩展名](https://cwe.mitre.org/data/definitions/646.html)
* [CWE-653 隔离或分隔不当](https://cwe.mitre.org/data/definitions/653.html)
* [CWE-656 依赖通过隐蔽实现安全](https://cwe.mitre.org/data/definitions/656.html)
* [CWE-657 违反安全设计原则](https://cwe.mitre.org/data/definitions/657.html)
* [CWE-676 使用潜在危险函数](https://cwe.mitre.org/data/definitions/676.html)
* [CWE-693 保护机制失效](https://cwe.mitre.org/data/definitions/693.html)
* [CWE-799 交互频率控制不当](https://cwe.mitre.org/data/definitions/799.html)
* [CWE-807 在安全决策中依赖不可信输入](https://cwe.mitre.org/data/definitions/807.html)
* [CWE-841 行为工作流执行不当](https://cwe.mitre.org/data/definitions/841.html)
* [CWE-1021 渲染的UI层或框架限制不当](https://cwe.mitre.org/data/definitions/1021.html)
* [CWE-1022 使用带有window.opener访问权限的不可信目标的Web链接](https://cwe.mitre.org/data/definitions/1022.html)
* [CWE-1125 攻击面过大](https://cwe.mitre.org/data/definitions/1125.html)


## X02:2025 内存管理失效

### 背景

Java、C#、JavaScript/TypeScript（node.js）、Go和"安全"Rust等语言是内存安全的。内存管理问题往往发生在非内存安全语言中，如C和C++。尽管该类别的相关CVE数量排名第三，但在社区调查中得分最低，在数据中的得分也很低。我们认为这是由于Web应用程序相对于更传统的桌面应用程序占主导地位。内存管理漏洞通常具有最高的CVSS评分。


### 评分表


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
   <td>2.96%
   </td>
   <td>1.13%
   </td>
   <td>55.62%
   </td>
   <td>28.45%
   </td>
   <td>6.75
   </td>
   <td>4.82
   </td>
   <td>220,414
   </td>
   <td>30,978
   </td>
  </tr>
</table>



### 描述

当应用程序被迫自行管理内存时，很容易出错。内存安全语言正被越来越多地使用，但全球仍有大量遗留系统在生产环境中运行，新的需要非内存安全语言的底层系统，以及与大型机、物联网设备、固件和其他可能被迫自行管理内存的系统交互的Web应用程序。具有代表性的CWE是 *CWE-120 复制缓冲区时未检查输入大小（'经典缓冲区溢出'）* 和 *CWE-121 基于堆栈的缓冲区溢出*。

内存管理失效可能发生在以下情况：

* 您没有为变量分配足够的内存
* 您没有验证输入，导致堆、栈或缓冲区溢出
* 您存储的数据值大于变量类型所能容纳的大小
* 您尝试使用未分配的内存或地址空间
* 您产生差一错误（从1而不是0开始计数）
* 您在对象被释放后尝试访问它
* 您使用未初始化的变量
* 您泄漏内存或以其他方式在错误中耗尽所有可用内存，直到应用程序失败

内存管理失效可能导致应用程序甚至整个系统的故障，另请参见 [X01:2025 缺乏应用程序弹性](#x012025-lack-of-application-resilience)


### 预防措施

防止内存管理失效的最佳方法是使用内存安全语言。示例包括Rust、Java、Go、C#、Python、Swift、Kotlin、JavaScript等。在创建新应用程序时，努力说服您的组织，切换到内存安全语言是值得的学习曲线。如果进行全面重构，在可能和可行的情况下，推动用内存安全语言重写。

如果您无法使用内存安全语言，请执行以下操作：

* 启用以下服务器功能，使内存管理错误更难被利用：地址空间布局随机化（ASLR）、数据执行保护（DEP）和结构化异常处理覆盖保护（SEHOP）。
* 监控您的应用程序是否存在内存泄漏。
* 非常仔细地验证您系统的所有输入，并拒绝所有不符合预期的输入。
* 研究您正在使用的语言，列出不安全函数和较安全函数，然后与整个团队分享该列表。如果可能，将其添加到您的安全编码指南或标准中。例如，在C中，优先使用strncpy()而不是strcpy()，使用strncat()而不是strcat()。
* 如果您的语言或框架提供内存安全库，请使用它们。例如：Safestringlib或SafeStr。
* 尽可能使用托管缓冲区和字符串，而不是原始数组和指针。
* 参加专注于内存问题和/或您选择的语言的安全编码培训。告知您的培训师您关注内存管理失效。
* 执行代码审查和/或静态分析。
* 使用有助于内存管理的编译器工具，如StackShield、StackGuard和Libsafe。
* 对您系统的每个输入进行模糊测试。
* 如果您进行渗透测试，请告知测试人员您关注内存管理失效，并希望他们在测试时特别注意这一点。
* 修复所有编译器错误*和*警告。不要因为程序编译通过就忽略警告。
* 确保您的基础架构定期打补丁、扫描和加固。
* 专门监控您的基础架构，以发现潜在的内存漏洞和其他故障。
* 考虑使用 [金丝雀（canaries）](https://en.wikipedia.org/wiki/Buffer_overflow_protection#Canaries) 来保护您的地址栈免受溢出攻击。

### 攻击场景示例

**场景 #1：** 缓冲区溢出是最著名的内存漏洞，攻击者向字段提交的信息超过其可接受的范围，从而溢出为底层变量创建的缓冲区。在一次成功的攻击中，溢出字符会覆盖栈指针，使攻击者能够将恶意指令插入您的程序。

**场景 #2：** 释放后使用（Use-After-Free, UAF）发生得足够频繁，以至于它成为一种半常见的浏览器漏洞赏金提交。想象一个Web浏览器处理操纵DOM元素的JavaScript。攻击者精心构造一个JavaScript载荷，创建一个对象（如DOM元素）并获取对它的引用。通过仔细操纵，他们触发浏览器释放对象的内存，同时保留一个悬空指针指向它。在浏览器意识到内存已被释放之前，攻击者分配一个占据*相同*内存空间的新对象。当浏览器尝试使用原始指针时，它现在指向攻击者控制的数据。如果这个指针是用于虚函数表的，攻击者可以将代码执行重定向到他们的载荷。

**场景 #3：** 一个接受用户输入的网络服务，没有正确验证或清理它，然后直接将其传递给日志记录函数。用户输入作为syslog(user_input)而不是syslog("%s", user_input)传递给日志记录函数，后者没有指定格式。攻击者发送包含格式说明符（如%x）的恶意载荷来读取栈内存（敏感数据泄露）或%n来写入内存地址。通过将多个格式说明符链接在一起，他们可以映射出栈，定位重要地址，然后覆盖它们。这将是一个格式字符串漏洞（不受控制的字符串格式）。

注意：现代浏览器使用多层防御来防御此类攻击，包括[浏览器沙箱](https://www.geeksforgeeks.org/ethical-hacking/what-is-browser-sandboxing/#types-of-browser-sandboxing) ASLR、DEP/NX、RELRO和PIE。对浏览器进行内存管理失效攻击并不是一种简单的攻击。

### 参考资源

* [OWASP社区页面：内存泄漏、](https://owasp.org/www-community/vulnerabilities/Memory_leak) [双重释放内存、](https://owasp.org/www-community/vulnerabilities/Doubly_freeing_memory) [& 缓冲区溢出](https://owasp.org/www-community/vulnerabilities/Buffer_Overflow)
* [Awesome Fuzzing：模糊测试资源列表](https://github.com/secfigo/Awesome-Fuzzing) 
* [Project Zero博客](https://googleprojectzero.blogspot.com)
* [Microsoft MSRC博客](https://www.microsoft.com/en-us/msrc/blog)

### 映射的CWE列表
* [CWE-14 编译器删除清除缓冲区的代码](https://cwe.mitre.org/data/definitions/14.html)
* [CWE-119 对内存缓冲区边界内操作限制不当](https://cwe.mitre.org/data/definitions/119.html)
* [CWE-120 复制缓冲区时未检查输入大小（'经典缓冲区溢出'）](https://cwe.mitre.org/data/definitions/120.html)
* [CWE-121 基于堆栈的缓冲区溢出](https://cwe.mitre.org/data/definitions/121.html)
* [CWE-122 基于堆的缓冲区溢出](https://cwe.mitre.org/data/definitions/122.html)
* [CWE-124 缓冲区下写（'缓冲区下溢'）](https://cwe.mitre.org/data/definitions/124.html)
* [CWE-125 越界读取](https://cwe.mitre.org/data/definitions/125.html)
* [CWE-126 缓冲区过度读取](https://cwe.mitre.org/data/definitions/126.html)
* [CWE-190 整数溢出或回绕](https://cwe.mitre.org/data/definitions/190.html)
* [CWE-191 整数下溢（回绕或回绕）](https://cwe.mitre.org/data/definitions/191.html)
* [CWE-196 无符号到有符号转换错误](https://cwe.mitre.org/data/definitions/196.html)
* [CWE-367 检查时/使用时（TOCTOU）竞争条件](https://cwe.mitre.org/data/definitions/367.html)
* [CWE-415 双重释放](https://cwe.mitre.org/data/definitions/415.html)
* [CWE-416 释放后使用](https://cwe.mitre.org/data/definitions/416.html)
* [CWE-457 使用未初始化变量](https://cwe.mitre.org/data/definitions/457.html)
* [CWE-459 清理不完整](https://cwe.mitre.org/data/definitions/459.html)
* [CWE-467 对指针类型使用sizeof()](https://cwe.mitre.org/data/definitions/467.html)
* [CWE-787 越界写入](https://cwe.mitre.org/data/definitions/787.html)
* [CWE-788 访问缓冲区结束后内存位置](https://cwe.mitre.org/data/definitions/788.html)
* [CWE-824 访问未初始化指针](https://cwe.mitre.org/data/definitions/824.html)



## X03:2025 对AI生成代码的不当信任（'Vibe Coding'）

### 背景

目前全世界都在谈论和使用AI，这包括软件开发人员。尽管目前尚无与AI生成代码相关的CVE或CWE，但众所周知且有文献记载，AI生成的代码往往比人类编写的代码包含更多漏洞。


### 描述

我们看到软件开发实践正在发生变化，不仅包括借助AI辅助编写的代码，还包括几乎完全在没有人工监督的情况下编写和提交的代码（通常称为vibe coding）。就像从不加思考地从博客或网站复制代码片段从来不是个好主意一样，在这种情况下问题被加剧了。好的、安全的代码片段过去和现在都很罕见，由于系统限制，AI可能会在统计上忽略它们。


### 预防措施

我们敦促所有编写代码的人员在使用AI时考虑以下事项：

* 您应该能够阅读并完全理解您提交的所有代码，即使它是由AI编写的或从在线论坛复制的。您对您提交的所有代码负责。
* 您应该彻底审查所有AI辅助编写的代码以发现漏洞，最好是用您自己的眼睛，也使用为此目的而设计的安全工具（如静态分析）。考虑使用[OWASP速查表系列：安全代码审查](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html)中描述的经典代码审查技术。
* 理想情况下，编写您自己的代码，让AI提出改进建议，检查AI的代码，并让AI进行修正，直到您对结果满意为止。
* 考虑使用检索增强生成（RAG）服务器，配合您自己收集和审查过的安全代码示例和文档，例如您组织的安全编码指南、标准或策略，并让RAG服务器强制执行任何策略或标准。
* 考虑购买为隐私和安全实施护栏的工具，与您选择的AI一起使用。
* 考虑购买私有AI，最好签订合同协议（包括隐私协议），规定AI不会用您组织的数据、查询、代码或任何其他敏感信息进行训练。
* 考虑在您的IDE和AI之间实施模型上下文协议（MCP）服务器，然后将其设置为强制执行您选择的安全工具的使用。
* 将策略和流程作为SDLC的一部分实施，以告知开发人员（和所有员工）他们在您的组织内应该如何以及不应该如何使用AI。
* 创建一份良好且有效的提示词列表，将IT安全最佳实践纳入考虑。理想情况下，它们还应该考虑您内部的安全编码指南。开发人员可以将这些提示词作为他们编程的起点。
* AI很可能成为系统开发生命周期每个阶段的一部分，既要考虑如何有效使用它，也要考虑如何安全使用它。明智地使用它。
* 实际上，**<u>不</u>** 建议将vibe coding用于复杂功能、业务关键型程序或长期使用的程序。
* 实施技术检查和保障措施，防止使用影子AI（Shadow AI）。
* 对您的开发人员进行培训，内容包括您的策略，以及安全的AI使用和在软件开发中使用AI的最佳实践。


### 参考资源

* [OWASP速查表：安全代码审查](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html)


### 映射的CWE列表
-无-
