# A04:2025 加密失败（Cryptographic Failures） ![icon](../assets/TOP_10_Icons_Final_Crypto_Failures.png){: style="height:80px;width:80px" align="right"}



## 背景

该弱点下降两位至第4名，重点关注与缺乏加密、加密强度不足、加密密钥泄露及相关错误有关的失败。该风险中最常见的三个通用弱点枚举（CWE）涉及弱伪随机数生成器的使用：*CWE-327 使用已损坏或有风险的加密算法、CWE-331：熵不足*、*CWE-1241：在随机数生成器中使用可预测算法*，以及 *CWE-338 使用加密强度弱的伪随机数生成器（PRNG）*。



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
   <td>32
   </td>
   <td>13.77%
   </td>
   <td>3.80%
   </td>
   <td>100.00%
   </td>
   <td>47.74%
   </td>
   <td>7.23
   </td>
   <td>3.90
   </td>
   <td>1,665,348
   </td>
   <td>2,185
   </td>
  </tr>
</table>



## 描述

一般来说，所有传输中的数据都应在[传输层](https://en.wikipedia.org/wiki/Transport_layer)（[OSI模型](https://en.wikipedia.org/wiki/OSI_model)第4层）进行加密。以前存在的障碍，如CPU性能和私钥/证书管理，现在已通过CPU内置的加密加速指令（例如：[AES支持](https://en.wikipedia.org/wiki/AES_instruction_set)）以及[LetsEncrypt.org](https://LetsEncrypt.org)等服务简化的私钥和证书管理得到解决，主要云厂商还为其特定平台提供了更紧密集成的证书管理服务。

除了保护传输层之外，确定哪些数据需要静态加密以及哪些数据在传输中需要额外加密（在[应用层](https://en.wikipedia.org/wiki/Application_layer)，OSI第7层）也很重要。例如，密码、信用卡号、健康记录、个人信息和商业机密需要额外保护，特别是如果这些数据受隐私法约束，例如欧盟《通用数据保护条例》（GDPR），或法规如PCI数据安全标准（PCI DSS）。对于所有这些数据：



* 是否有任何旧的或弱的加密算法或协议被默认使用或在旧代码中使用？
* 是否在使用默认加密密钥，是否生成了弱加密密钥，是否重复使用密钥，或者是否缺少适当的密钥管理和轮换？
* 加密密钥是否被签入源代码仓库？
* 加密是否未强制执行，例如，是否缺少任何HTTP头（浏览器）安全指令或头？
* 接收到的服务器证书和信任链是否经过正确验证？
* 初始化向量（IV）是否被忽略、重复使用，或对于加密操作模式来说生成得不够安全？是否在使用不安全的操作模式，如ECB？当认证加密更合适时，是否仅使用了加密？
* 在缺少基于密码的密钥派生函数（PBKDF）的情况下，是否将密码用作加密密钥？
* 所使用的随机性是否并非为满足加密要求而设计？即使选择了正确的函数，是否需要由开发者进行种子设置，如果不是，开发者是否用缺乏足够熵/不可预测性的种子覆盖了其内置的强种子设置功能？
* 是否在使用已弃用的哈希函数，如MD5或SHA1，或者在需要加密哈希函数时使用了非加密哈希函数？
* 加密错误消息或侧信道信息是否可被利用，例如以填充预言机（padding oracle）攻击的形式？
* 加密算法是否可以被降级或绕过？

参见参考ASVS：加密（V11）、安全通信（V12）和数据保护（V14）。


## 如何预防

至少执行以下操作，并查阅参考资料：



* 对应用程序处理、存储或传输的数据进行分类和标记。根据隐私法、监管要求或业务需求识别哪些数据是敏感的。
* 将最敏感的密钥存储在硬件或基于云的HSM（硬件安全模块）中。
* 尽可能使用广受信任的加密算法实现。
* 不要不必要地存储敏感数据。尽快丢弃它，或使用符合PCI DSS的令牌化甚至截断。不保留的数据无法被盗取。
* 确保所有敏感数据在静态时都经过加密。
* 确保使用最新且强大的标准算法、协议和密钥；使用适当的密钥管理。
* 仅使用协议 >= TLS 1.2 加密所有传输中的数据，使用前向保密（FS）密码，放弃对密码块链接（CBC）密码的支持，支持量子密钥交换算法。对于HTTPS，使用HTTP严格传输安全（HSTS）强制加密。使用工具检查一切。
* 对包含敏感数据的响应禁用缓存。这包括CDN、Web服务器和任何应用程序缓存（例如：Redis）中的缓存。
* 根据数据分类应用所需的安全控制。
* 不要使用未加密的协议，如FTP和STARTTLS。避免使用SMTP传输机密数据。
* 使用带有工作因子（延迟因子）的强大自适应加盐哈希函数存储密码，例如Argon2、yescrypt、scrypt或PBKDF2-HMAC-SHA-512。对于使用bcrypt的遗留系统，请在[OWASP速查表：密码存储](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)获取更多建议。
* 初始化向量必须根据操作模式适当选择。这可能意味着使用CSPRNG（加密安全伪随机数生成器）。对于需要nonce的模式，初始化向量（IV）不需要CSPRNG。在所有情况下，IV都不应针对固定密钥使用两次。
* 始终使用认证加密，而不仅仅是加密。
* 密钥应以加密方式随机生成，并以字节数组形式存储在内存中。如果使用密码，则必须通过适当的基于密码的密钥派生函数将其转换为密钥。
* 确保在适当的地方使用加密随机性，并且它没有以可预测的方式或用低熵进行种子设置。大多数现代API不需要开发者对CSPRNG进行种子设置即可保证安全。
* 避免使用已弃用的加密函数、块构建方法和填充方案，如MD5、SHA1、密码块链接模式（CBC）、PKCS #1 v1.5。
* 通过安全专家、为此目的设计的工具或两者兼而有之，审查设置和配置是否满足安全要求。
* 您需要现在就开始为后量子密码学（PQC）做准备，参见参考（ENISA），以便高风险系统不迟于2030年底得到保护。


## 攻击场景示例

**场景 #1**：一个网站没有对所有页面使用或强制使用TLS，或支持弱加密。攻击者监控网络流量（例如，在不安全的无线网络上），将连接从HTTPS降级为HTTP，拦截请求，并窃取用户的会话cookie。然后攻击者重放此cookie并劫持用户的（已认证）会话，访问或修改用户的私人数据。除了上述行为，他们还可以修改所有传输的数据，例如， money transfer 的接收方。

**场景 #2**：密码数据库使用未加盐或简单哈希来存储每个人的密码。文件上传漏洞允许攻击者检索密码数据库。所有未加盐的哈希都可以通过预计算哈希的彩虹表暴露。由简单或快速哈希函数生成的哈希即使经过加盐，也可能被GPU破解。


## 参考资料



* [OWASP主动控制：C2：使用加密保护数据](https://top10proactive.owasp.org/archive/2024/the-top-10/c2-crypto/)
* [OWASP应用程序安全验证标准（ASVS）：](https://owasp.org/www-project-application-security-verification-standard) [V11,](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x20-V11-Cryptography.md) [12, ](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x21-V12-Secure-Communication.md) [14](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x23-V14-Data-Protection.md)
* [OWASP速查表：传输层保护](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
* [OWASP速查表：用户隐私保护](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html)
* [OWASP速查表：密码存储](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
* [OWASP速查表：加密存储](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
* [OWASP速查表：HSTS](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)
* [OWASP测试指南：测试弱加密](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/README)
* [ENISA：向后量子密码学过渡的协调实施路线图](https://digital-strategy.ec.europa.eu/en/library/coordinated-implementation-roadmap-transition-post-quantum-cryptography)
* [NIST发布首批3项最终确定的后量子加密标准](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)


## 映射的CWE列表

* [CWE-261 密码弱编码](https://cwe.mitre.org/data/definitions/261.html)

* [CWE-296 证书信任链跟踪不当](https://cwe.mitre.org/data/definitions/296.html)

* [CWE-319 敏感信息明文传输](https://cwe.mitre.org/data/definitions/319.html)

* [CWE-320 密钥管理错误（已禁止）](https://cwe.mitre.org/data/definitions/320.html)

* [CWE-321 使用硬编码加密密钥](https://cwe.mitre.org/data/definitions/321.html)

* [CWE-322 无实体认证的密钥交换](https://cwe.mitre.org/data/definitions/322.html)

* [CWE-323 在加密中重用Nonce、密钥对](https://cwe.mitre.org/data/definitions/323.html)

* [CWE-324 使用已过期的密钥](https://cwe.mitre.org/data/definitions/324.html)

* [CWE-325 缺少必需的加密步骤](https://cwe.mitre.org/data/definitions/325.html)

* [CWE-326 加密强度不足](https://cwe.mitre.org/data/definitions/326.html)

* [CWE-327 使用已损坏或有风险的加密算法](https://cwe.mitre.org/data/definitions/327.html)

* [CWE-328 可逆的单向哈希](https://cwe.mitre.org/data/definitions/328.html)

* [CWE-329 在CBC模式下未使用随机IV](https://cwe.mitre.org/data/definitions/329.html)

* [CWE-330 使用随机性不足的值](https://cwe.mitre.org/data/definitions/330.html)

* [CWE-331 熵不足](https://cwe.mitre.org/data/definitions/331.html)

* [CWE-332 PRNG中熵不足](https://cwe.mitre.org/data/definitions/332.html)

* [CWE-334 随机值空间小](https://cwe.mitre.org/data/definitions/334.html)

* [CWE-335 伪随机数生成器（PRNG）中种子使用不正确](https://cwe.mitre.org/data/definitions/335.html)

* [CWE-336 伪随机数生成器（PRNG）中使用相同种子](https://cwe.mitre.org/data/definitions/336.html)

* [CWE-337 伪随机数生成器（PRNG）中使用可预测种子](https://cwe.mitre.org/data/definitions/337.html)

* [CWE-338 使用加密强度弱的伪随机数生成器（PRNG）](https://cwe.mitre.org/data/definitions/338.html)

* [CWE-340 生成可预测的数字或标识符](https://cwe.mitre.org/data/definitions/340.html)

* [CWE-342 从先前值预测精确值](https://cwe.mitre.org/data/definitions/342.html)

* [CWE-347 加密签名验证不当](https://cwe.mitre.org/data/definitions/347.html)

* [CWE-523 凭证传输未受保护](https://cwe.mitre.org/data/definitions/523.html)

* [CWE-757 协商期间选择安全性较低的算法（'算法降级'）](https://cwe.mitre.org/data/definitions/757.html)

* [CWE-759 使用无盐的单向哈希](https://cwe.mitre.org/data/definitions/759.html)

* [CWE-760 使用具有可预测盐的单向哈希](https://cwe.mitre.org/data/definitions/760.html)

* [CWE-780 不使用OAEP的RSA算法使用](https://cwe.mitre.org/data/definitions/780.html)

* [CWE-916 使用计算工作量不足的密码哈希](https://cwe.mitre.org/data/definitions/916.html)

* [CWE-1240 使用具有风险实现的加密原语](https://cwe.mitre.org/data/definitions/1240.html)

* [CWE-1241 在随机数生成器中使用可预测算法](https://cwe.mitre.org/data/definitions/1241.html)
