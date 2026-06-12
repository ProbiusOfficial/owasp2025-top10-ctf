# A03:2025 软件供应链失效 ![icon](../assets/TOP_10_Icons_Final_Vulnerable_Outdated_Components.png){: style="height:80px;width:80px" align="right"}

## 背景

在 Top 10 社区调查中排名第一，恰好 50% 的受访者将其评为第 1 位。自 2013 年首次以"A9 – 使用具有已知漏洞的组件"出现在 Top 10 中以来，该风险的范围已扩大到包括所有供应链失效，而不仅仅是涉及已知漏洞的失效。尽管范围扩大，供应链失效仍然难以识别，只有 11 个通用漏洞披露（CVE）具有相关的 CWE。然而，在贡献数据中进行测试和报告时，该类别的平均发生率最高，为 5.19%。相关的 CWE 包括 *CWE-477：使用已弃用函数*、*CWE-1104：使用未维护的第三方组件*、*CWE-1329：依赖不可更新的组件* 以及 *CWE-1395：依赖存在漏洞的第三方组件*。

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
   <td>6
   </td>
   <td>9.56%
   </td>
   <td>5.72%
   </td>
   <td>65.42%
   </td>
   <td>27.47%
   </td>
   <td>8.17
   </td>
   <td>5.23
   </td>
   <td>215,248
   </td>
   <td>11
   </td>
  </tr>
</table>

## 描述

软件供应链失效是指在构建、分发或更新软件的过程中发生的故障或其他损害。它们通常由系统依赖的第三方代码、工具或其他依赖项中的漏洞或恶意更改引起。

如果出现以下情况，您可能存在漏洞：

* 您没有仔细跟踪所使用的所有组件的版本（包括客户端和服务器端）。这包括您直接使用的组件以及嵌套（传递）依赖项。
* 软件存在漏洞、不受支持或已过时。这包括操作系统、Web/应用程序服务器、数据库管理系统（DBMS）、应用程序、API 和所有组件、运行时环境以及库。
* 您没有定期扫描漏洞并订阅与您使用的组件相关的安全公告。
* 您没有变更管理流程或供应链中的变更跟踪，包括跟踪 IDE、IDE 扩展和更新、组织代码仓库的更改、沙箱、镜像和库仓库、工件的创建和存储方式等。供应链的每个部分都应记录，尤其是变更。
* 您没有加固供应链的每个部分，特别关注访问控制和最小权限的应用。
* 您的供应链系统没有任何职责分离。任何个人都不应能够在没有另一个人监督的情况下编写代码并将其一路推广到生产环境。
* 来自不可信来源的组件，跨越技术栈的任何部分，被用于或可能影响生产环境。
* 您没有以基于风险的及时方式修复或升级底层平台、框架和依赖项。这在修补是变更控制下的每月或每季度任务的环境中很常见，使组织在修复漏洞之前面临数天或数月的不必要暴露。
* 软件开发人员没有测试更新、升级或修补后的库的兼容性。
* 您没有保护系统每个部分的配置（参见 [A02:2025-安全配置错误](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)）。
* 您的 CI/CD 流水线安全性低于其构建和部署的系统，尤其是在其复杂的情况下。

## 如何预防

应建立补丁管理流程，以：

* 集中生成和管理整个软件的软件物料清单（SBOM）。
* 不仅跟踪您的直接依赖项，还要跟踪它们的（传递）依赖项，依此类推。
* 通过删除未使用的依赖项、不必要的功能、组件、文件和文档来减少攻击面。
* 使用 OWASP Dependency Track、OWASP Dependency Check、retire.js 等工具持续清点客户端和服务器端组件（例如框架、库）及其依赖项的版本。
* 持续监控通用漏洞披露（CVE）、国家漏洞数据库（NVD）和 [开源漏洞（OSV）](https://osv.dev/) 等来源，以查找您使用的组件中的漏洞。使用软件成分分析、软件供应链或以安全为重点的 SBOM 工具来自动化该流程。订阅与您使用的组件相关的安全漏洞告警。
* 仅通过安全链接从官方（可信）来源获取组件。优先选择签名包，以减少包含被修改的恶意组件的机会（参见 [A08:2025-软件和数据完整性失效](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/)）。
* 慎重选择您使用的依赖项版本，仅在需要时升级。
* 监控未维护或不创建旧版本安全补丁的库和组件。如果无法修补，请考虑迁移到替代方案。如果这也不可能，请考虑部署虚拟补丁来监控、检测或防护已发现的问题。
* 定期更新您的 CI/CD、IDE 和任何其他开发人员工具
* 避免同时向所有系统部署更新。使用分阶段推出或金丝雀部署来限制暴露，以防可信供应商被入侵。

应建立变更管理流程或跟踪系统，以跟踪以下变更：

* CI/CD 设置（所有构建工具和流水线）
* 代码仓库
* 沙箱区域
* 开发人员 IDE
* SBOM 工具和创建的工件
* 日志系统和日志
* 第三方集成，例如 SaaS
* 工件仓库
* 容器注册表

加固以下系统，包括启用 MFA 和锁定 IAM：

* 您的代码仓库（包括不提交密钥、保护分支、备份）
* 开发人员工作站（定期修补、MFA、监控等）
* 您的构建服务器和 CI/CD（职责分离、访问控制、签名构建、环境范围的密钥、防篡改日志等）
* 您的工件（通过来源、签名和时间戳确保完整性，推广工件而不是为每个环境重新构建，确保构建是不可变的）
* 基础设施即代码（像所有代码一样管理，包括使用 PR 和版本控制）

每个组织都必须确保为应用程序或组合的生命周期制定持续的监控、分类和应用更新或配置更改的计划。

## 攻击场景示例

**场景 #1：** 可信供应商被恶意软件入侵，导致您在升级时计算机系统被入侵。最著名的例子可能是：

* 2019 年 SolarWinds 入侵事件导致约 18,000 个组织被入侵。[https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack](https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack)

**场景 #2：** 可信供应商被入侵，使其仅在特定条件下才表现出恶意行为。

* 2025 年 Bybit 15 亿美元盗窃案是由[钱包软件中的供应链攻击](https://www.sygnia.co/blog/sygnia-investigation-bybit-hack/)引起的，该攻击仅在目标钱包被使用时才执行。

**场景 #3：** 2025 年的 [`Shai-Hulud` 供应链攻击](https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem)是第一个成功自我传播的 npm 蠕虫。攻击者在流行包中植入恶意版本，使用安装后脚本收集和窃取敏感数据到公共 GitHub 仓库。该恶意软件还会检测受害者环境中的 npm 令牌，并自动使用它们推送任何可访问包的恶意版本。该蠕虫在被 npm 阻止之前传播到超过 500 个包版本。这次供应链攻击是先进的、快速传播的且具有破坏性的，通过针对开发人员机器，它证明了开发人员本身现在已成为供应链攻击的主要目标。

**场景 #4：** 组件通常以与应用程序本身相同的权限运行，因此任何组件中的缺陷都可能导致严重影响。此类缺陷可能是意外的（例如编码错误）或故意的（例如组件中的后门）。发现的一些可利用组件漏洞示例包括：

* CVE-2017-5638，一个 Struts 2 远程代码执行漏洞，允许在服务器上执行任意代码，已被归咎于重大入侵事件。
* CVE-2021-44228（"Log4Shell"），一个 Apache Log4j 远程代码执行零日漏洞，已被归咎于勒索软件、加密挖矿和其他攻击活动。

## 参考

* [OWASP 应用程序安全验证标准：V15 安全编码与架构](https://owasp.org/www-project-application-security-verification-standard/)
* [OWASP 速查表系列：依赖图 SBOM](https://cheatsheetseries.owasp.org/cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html)
* [OWASP 速查表系列：漏洞依赖管理](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html)
* [OWASP Dependency-Track](https://owasp.org/www-project-dependency-track/)
* [OWASP CycloneDX](https://owasp.org/www-project-cyclonedx/)
* [OWASP 应用程序安全验证标准：V1 架构、设计和威胁建模](https://owasp-aasvs.readthedocs.io/en/latest/v1.html)
* [OWASP Dependency Check（用于 Java 和 .NET 库）](https://owasp.org/www-project-dependency-check/)
* OWASP 测试指南 - 映射应用程序架构（OTG-INFO-010）
* [OWASP 虚拟补丁最佳实践](https://owasp.org/www-community/Virtual_Patching_Best_Practices)
* [不安全库的不幸现实](https://www.scribd.com/document/105692739/JeffWilliamsPreso-Sm)
* [MITRE 通用漏洞披露（CVE）搜索](https://www.cve.org)
* [国家漏洞数据库（NVD）](https://nvd.nist.gov)
* [Retire.js 用于检测已知漏洞的 JavaScript 库](https://retirejs.github.io/retire.js/)
* [GitHub 咨询数据库](https://github.com/advisories)
* Ruby 库安全咨询数据库和工具
* [SAFECode 软件完整性控制（PDF）](https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf)
* [Glassworm 供应链攻击](https://thehackernews.com/2025/10/self-spreading-glassworm-infects-vs.html)
* [PhantomRaven 供应链攻击活动](https://thehackernews.com/2025/10/phantomraven-malware-found-in-126-npm.html)

## 映射的 CWE 列表

* [CWE-447 使用已弃用函数](https://cwe.mitre.org/data/definitions/447.html)

* [CWE-1035 2017 Top 10 A9：使用具有已知漏洞的组件](https://cwe.mitre.org/data/definitions/1035.html)

* [CWE-1104 使用未维护的第三方组件](https://cwe.mitre.org/data/definitions/1104.html)

* [CWE-1329 依赖不可更新的组件](https://cwe.mitre.org/data/definitions/1329.html)

* [CWE-1357 依赖不够可信的组件](https://cwe.mitre.org/data/definitions/1357.html)

* [CWE-1395 依赖存在漏洞的第三方组件](https://cwe.mitre.org/data/definitions/1395.html)
