# Mnemonic Wallet Generator

## English

### 📖 Project Description

A powerful batch mnemonic wallet generator that supports simultaneous generation of Solana (SOL) and Ethereum (ETH) wallet addresses. The tool is based on the BIP-39 standard and can securely derive corresponding wallet addresses and private keys from mnemonic phrases.

### ✨ Key Features

- 🔐 **Multi-chain Support**: Generate both Solana and Ethereum wallets simultaneously
- 📝 **Batch Processing**: Support batch reading and processing of multiple mnemonic phrases
- 🛡️ **Standard Compliance**: Fully compliant with BIP-39 and BIP-44 standards
- 💾 **Data Export**: Automatically generate CSV format wallet information tables
- 🎨 **User-friendly Interface**: Colorful terminal interface with clear progress display
- ✅ **Validation Mechanism**: Automatic mnemonic phrase validity verification
- 📊 **Statistics**: Detailed processing result statistics

### 🔧 Technical Specifications

| Blockchain | Derivation Path | Standard |
|------------|-----------------|----------|
| Solana | `m/44'/501'/0'/0'` | BIP-44 |
| Ethereum | `m/44'/60'/0'/0/0` | BIP-44 |

### 📦 Installation

Before running the script, please ensure the following Python libraries are installed:

```bash
pip install mnemonic solders base58 pandas eth-account bip32utils
````

Or install all at once using:

```bash
pip install -r requirements.txt
```

### 🚀 Usage

1. **Prepare Mnemonic File**

   * Create an `IN.txt` file in the same directory as the script
   * Input one mnemonic phrase per line (supports 12 or 24 words)
   * Ensure mnemonic format is correct with words separated by spaces

2. **Run Script**

   ```bash
   python wallet_generator.py
   ```

3. **View Results**

   * The program will generate a `钱包信息.csv` file in the same directory
   * The CSV file contains all wallet addresses, private keys, and related information

### 📁 File Structure

```
Project Folder/
├── wallet_generator.py    # Main program file
├── IN.txt                # Input file (mnemonic list)
├── 钱包信息.csv          # Output file (generated wallet info)
└── README.md             # Documentation
```

### 📋 Output Format

The generated CSV file contains the following fields:

| Field Name | Description                                |
| ---------- | ------------------------------------------ |
| 序号         | Mnemonic processing order                  |
| SOL钱包地址    | Solana wallet public key address           |
| SOL私钥      | Solana wallet private key (Base58 encoded) |
| ETH钱包地址    | Ethereum wallet address                    |
| ETH私钥      | Ethereum wallet private key (hexadecimal)  |
| 助记词        | Original mnemonic phrase                   |
| SOL派生路径    | Solana derivation path                     |
| ETH派生路径    | Ethereum derivation path                   |
| 生成时间       | Wallet generation timestamp                |
| 状态         | Generation status (Success/Failed)         |

### ⚠️ Security Warnings

* **Private Key Security**: Please keep the generated private keys and mnemonic phrases secure and never share them with others
* **Offline Usage**: It is recommended to run this tool in an offline environment to ensure security
* **Backup Important**: Please backup the generated wallet information files promptly
* **Test First**: Before processing important mnemonic phrases, please test the tool functionality with test data first

### 🐛 Troubleshooting

**Common Issues and Solutions:**

1. **Module Import Error**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Mnemonic Validation Failed**

   * Check mnemonic word count (should be 12 or 24 words)
   * Confirm correct word spelling
   * Verify mnemonic compliance with BIP-39 standard

3. **File Reading Error**

   * Ensure `IN.txt` file exists in the same directory as the script
   * Check file encoding format (UTF-8 recommended)

### 👤 Developer Information

* **Developer**: @7KRIS5
* **Version**: 2025 Mnemonic Wallet Generation Edition
* **License**: MIT License

---
### 📖 项目简介

这是一个功能强大的助记词批量钱包生成器，支持同时生成 Solana (SOL) 和 Ethereum (ETH) 钱包地址。工具基于 BIP-39 标准，能够从助记词安全地派生出对应的钱包地址和私钥。

### ✨ 主要特性

* 🔐 **多链支持**: 同时生成 Solana 和 Ethereum 钱包
* 📝 **批量处理**: 支持批量读取和处理多个助记词
* 🛡️ **标准兼容**: 完全遵循 BIP-39 和 BIP-44 标准
* 💾 **数据导出**: 自动生成 CSV 格式的钱包信息表格
* 🎨 **友好界面**: 彩色终端界面，清晰显示处理进度
* ✅ **验证机制**: 自动验证助记词有效性
* 📊 **统计信息**: 详细的处理结果统计

### 🔧 技术规格

| 区块链      | 派生路径               | 标准     |
| -------- | ------------------ | ------ |
| Solana   | `m/44'/501'/0'/0'` | BIP-44 |
| Ethereum | `m/44'/60'/0'/0/0` | BIP-44 |

### 📦 安装依赖

在运行脚本前，请确保安装以下 Python 库：

```bash
pip install mnemonic solders base58 pandas eth-account bip32utils
```

或使用以下命令一次性安装：

```bash
pip install -r requirements.txt
```

### 🚀 使用方法

1. **准备助记词文件**

   * 在脚本同目录下创建 `IN.txt` 文件
   * 每行输入一个助记词（支持12或24个单词）
   * 确保助记词格式正确，单词之间用空格分隔

2. **运行脚本**

   ```bash
   python wallet_generator.py
   ```

3. **查看结果**

   * 程序会在同目录下生成 `钱包信息.csv` 文件
   * CSV文件包含所有钱包地址、私钥和相关信息

### 📁 文件结构

```
项目文件夹/
├── wallet_generator.py    # 主程序文件
├── IN.txt                # 输入文件（助记词列表）
├── 钱包信息.csv          # 输出文件（生成的钱包信息）
└── README.md             # 说明文档
```

### 📋 输出格式

生成的 CSV 文件包含以下字段：

| 字段名     | 说明                     |
| ------- | ---------------------- |
| 序号      | 助记词处理顺序                |
| SOL钱包地址 | Solana 钱包公钥地址          |
| SOL私钥   | Solana 钱包私钥 (Base58编码) |
| ETH钱包地址 | Ethereum 钱包地址          |
| ETH私钥   | Ethereum 钱包私钥 (十六进制)   |
| 助记词     | 原始助记词                  |
| SOL派生路径 | Solana 派生路径            |
| ETH派生路径 | Ethereum 派生路径          |
| 生成时间    | 钱包生成时间戳                |
| 状态      | 生成状态（成功/失败）            |

### ⚠️ 安全提醒

* **私钥安全**: 请妥善保管生成的私钥和助记词，切勿泄露给他人
* **离线使用**: 建议在离线环境中运行此工具以确保安全性
* **备份重要**: 请及时备份生成的钱包信息文件
* **测试优先**: 在处理重要助记词前，请先使用测试数据验证工具功能

**常见问题及解决方案：**

1. **模块导入**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ``
2. **助记词验证失败**

   * 检查助记词单词数量（应为12或24个）
   * 确认单词拼写正确
   * 验证助记词是否符合 BIP-39 标准

3. **文件读取错误**

   * 确保 `IN.txt` 文件存在于脚本同目录
   * 检查文件编码格式（推荐使用 UTF-8）

### 👤 开发者信息

* **开发者**: @7KRIS5
* **版本**: 2025 助记词钱包生成版
* **许可证**: MIT License

