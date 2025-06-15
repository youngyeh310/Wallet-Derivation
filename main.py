#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from mnemonic import Mnemonic
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import base58
import hashlib
import hmac
from typing import Tuple
import struct
import pandas as pd
from datetime import datetime
from eth_account import Account
from eth_account.signers.local import LocalAccount
import bip32utils

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear_screen()
    
    ascii_art = [
        "    ███████╗██╗  ██╗██████╗ ██╗███████╗███████╗",
        "    ╚════██║██║ ██╔╝██╔══██╗██║██╔════╝██╔════╝",
        "        ██╔╝█████╔╝ ██████╔╝██║███████╗███████╗",
        "       ██╔╝ ██╔═██╗ ██╔══██╗██║╚════██║╚════██║",
        "       ██║  ██║  ██╗██║  ██║██║███████║███████║",
        "       ╚═╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝"
    ]
    
    print('\n')
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.BLUE, Colors.MAGENTA, Colors.CYAN]
    for i, line in enumerate(ascii_art):
        color = colors[i % len(colors)]
        print(f"{color}{Colors.BOLD}{line}{Colors.RESET}")
        time.sleep(0.1)
    print('\n')
    
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.YELLOW}{Colors.BOLD}                助记词批量钱包生成器V1                       {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.GREEN}             SOL & ETH Wallet Generator from Mnemonic        {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╠══════════════════════════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.MAGENTA}  🔐 支持格式: 12/24词助记词 (BIP-39标准)                  {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.BLUE}  🛡️  派生路径: SOL (m/44'/501'/0'/0') | ETH (m/44'/60'/0'/0/0) {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.WHITE}  ⚡ 批量处理: 自动生成钱包地址和私钥                     {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╠══════════════════════════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.GRAY}  开发者: {Colors.YELLOW}{Colors.BOLD}@7KRIS5{Colors.GRAY}                                   {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.GRAY}  版本: 2025 助记词钱包生成版                            {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}")
    
    print(f'\n{Colors.RED}{Colors.BOLD}⚠️  安全提醒:{Colors.RESET}')
    print(f'{Colors.YELLOW}   • 请妥善保管生成的私钥和助记词{Colors.RESET}')
    print(f'{Colors.YELLOW}   • 建议在离线环境中运行此工具{Colors.RESET}')
    print(f'{Colors.YELLOW}   • 请勿将私钥信息分享给他人{Colors.RESET}')
    
    print(f'\n{Colors.GREEN}{Colors.BOLD}📖 使用说明:{Colors.RESET}')
    print(f'{Colors.WHITE}   1. 将助记词放入 IN.txt 文件（每行一个）{Colors.RESET}')
    print(f'{Colors.WHITE}   2. 工具将自动派生 SOL 和 ETH 钱包{Colors.RESET}')
    print(f'{Colors.WHITE}   3. 结果将保存到 CSV 文件{Colors.RESET}')
    
    print(f'\n{Colors.CYAN}{"═" * 62}\n{Colors.RESET}')
    
    input(f"{Colors.GREEN}按 Enter 键开始生成钱包...{Colors.RESET}")

def read_all_mnemonics_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            mnemonics = [line.strip() for line in lines if line.strip()]
            return mnemonics
    except FileNotFoundError:
        print(f"{Colors.RED}错误: 找不到文件 {file_path}{Colors.RESET}")
        return []
    except Exception as e:
        print(f"{Colors.RED}读取文件时出错: {e}{Colors.RESET}")
        return []

def validate_mnemonic(mnemonic_phrase):
    mnemo = Mnemonic("english")
    return mnemo.check(mnemonic_phrase)

def derive_key_from_path(seed: bytes, path: str) -> bytes:
    master_key = hmac.new(b"ed25519 seed", seed, hashlib.sha512).digest()
    master_private_key = master_key[:32]
    master_chain_code = master_key[32:]
    
    path_indices = [
        44 + 0x80000000,
        501 + 0x80000000,
        0 + 0x80000000,
        0 + 0x80000000
    ]
    
    private_key = master_private_key
    chain_code = master_chain_code
    
    for index in path_indices:
        data = b'\x00' + private_key + struct.pack('>I', index)
        hmac_result = hmac.new(chain_code, data, hashlib.sha512).digest()
        private_key = hmac_result[:32]
        chain_code = hmac_result[32:]
    
    return private_key

def derive_ethereum_key(seed: bytes, path: str = "m/44'/60'/0'/0/0") -> Tuple[str, str]:
    try:
        bip32_root_key = bip32utils.BIP32Key.fromEntropy(seed)
        path_parts = path.replace("m/", "").split("/")
        bip32_key = bip32_root_key
        for part in path_parts:
            index = int(part.replace("'", "")) + (0x80000000 if "'" in part else 0)
            bip32_key = bip32_key.ChildKey(index)
        
        private_key = bip32_key.PrivateKey()
        account: LocalAccount = Account.from_key(private_key)
        return account.address, private_key.hex()
    except Exception as e:
        print(f"{Colors.RED}生成Ethereum钱包时出错: {e}{Colors.RESET}")
        return None, None

def generate_solana_wallet(mnemonic_phrase):
    try:
        mnemo = Mnemonic("english")
        seed = mnemo.to_seed(mnemonic_phrase, passphrase="")
        private_key_bytes = derive_key_from_path(seed, "m/44'/501'/0'/0'")
        keypair = Keypair.from_seed(private_key_bytes)
        public_key = keypair.pubkey()
        wallet_address = str(public_key)
        private_key_32 = keypair.secret()[:32]
        public_key_32 = bytes(keypair.pubkey())
        full_private_key = private_key_32 + public_key_32
        private_key_base58 = base58.b58encode(full_private_key).decode('utf-8')
        return wallet_address, private_key_base58
    except Exception as e:
        print(f"{Colors.RED}生成Solana钱包时出错: {e}{Colors.RESET}")
        return None, None

def generate_wallets(mnemonic_phrase):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic_phrase, passphrase="")
    sol_address, sol_private_key = generate_solana_wallet(mnemonic_phrase)
    eth_address, eth_private_key = derive_ethereum_key(seed)
    return sol_address, sol_private_key, eth_address, eth_private_key

def main():
    display_banner()
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置输入输出文件路径为脚本同目录
    input_file = os.path.join(script_dir, "IN.txt")
    output_folder = script_dir
    output_file = os.path.join(output_folder, "钱包信息.csv")
    
    print(f"{Colors.BOLD}=== Solana & Ethereum 钱包地址批量生成器 ==={Colors.RESET}")
    print(f"正在读取文件: {Colors.CYAN}{input_file}{Colors.RESET}")
    
    mnemonic_list = read_all_mnemonics_from_file(input_file)
    if not mnemonic_list:
        print(f"{Colors.RED}❌ 没有找到有效的助记词{Colors.RESET}")
        return
    
    print(f"{Colors.GREEN}✅ 成功读取到 {len(mnemonic_list)} 个助记词{Colors.RESET}")
    
    all_wallet_data = []
    successful_count = 0
    failed_count = 0
    
    for index, mnemonic_phrase in enumerate(mnemonic_list, 1):
        print(f"\n{Colors.YELLOW}--- 处理第 {index}/{len(mnemonic_list)} 个助记词 ---{Colors.RESET}")
        print(f"助记词: {Colors.CYAN}{mnemonic_phrase[:50]}...{Colors.RESET}")
        
        if not validate_mnemonic(mnemonic_phrase):
            print(f"{Colors.RED}❌ 第 {index} 个助记词无效，跳过{Colors.RESET}")
            failed_count += 1
            continue
        
        print(f"{Colors.GREEN}✅ 助记词验证通过{Colors.RESET}")
        
        sol_address, sol_private_key, eth_address, eth_private_key = generate_wallets(mnemonic_phrase)
        
        if sol_address and sol_private_key and eth_address and eth_private_key:
            wallet_data = {
                '序号': index,
                'SOL钱包地址': sol_address,
                'SOL私钥': sol_private_key,
                'ETH钱包地址': eth_address,
                'ETH私钥': eth_private_key,
                '助记词': mnemonic_phrase,
                'SOL派生路径': "m/44'/501'/0'/0'",
                'ETH派生路径': "m/44'/60'/0'/0/0",
                '生成时间': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                '状态': '成功'
            }
            all_wallet_data.append(wallet_data)
            successful_count += 1
            print(f"{Colors.GREEN}✅ Solana 钱包地址: {sol_address}{Colors.RESET}")
            print(f"{Colors.GREEN}✅ Ethereum 钱包地址: {eth_address}{Colors.RESET}")
        else:
            wallet_data = {
                '序号': index,
                'SOL钱包地址': sol_address or '生成失败',
                'SOL私钥': sol_private_key or '生成失败',
                'ETH钱包地址': eth_address or '生成失败',
                'ETH私钥': eth_private_key or '生成失败',
                '助记词': mnemonic_phrase,
                'SOL派生路径': "m/44'/501'/0'/0'",
                'ETH派生路径': "m/44'/60'/0'/0/0",
                '生成时间': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                '状态': '失败'
            }
            all_wallet_data.append(wallet_data)
            failed_count += 1
            print(f"{Colors.RED}❌ 第 {index} 个助记词生成钱包失败{Colors.RESET}")
    
    if all_wallet_data:
        try:
            os.makedirs(output_folder, exist_ok=True)
            df = pd.DataFrame(all_wallet_data)
            
            # 保存为CSV文件
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            print(f"\n{Colors.GREEN}🎉 批量处理完成!{Colors.RESET}")
            print(f"{Colors.BLUE}📊 处理统计:{Colors.RESET}")
            print(f"   - 总计助记词: {Colors.YELLOW}{len(mnemonic_list)}{Colors.RESET} 个")
            print(f"   - 成功生成: {Colors.GREEN}{successful_count}{Colors.RESET} 个")
            print(f"   - 失败: {Colors.RED}{failed_count}{Colors.RESET} 个")
            print(f"\n{Colors.GREEN}✅ CSV文件已保存:{Colors.RESET}")
            print(f"   📁 文件夹: {Colors.CYAN}{output_folder}{Colors.RESET}")
            print(f"   📄 文件名: {Colors.CYAN}钱包信息.csv{Colors.RESET}")
            print(f"   🔗 完整路径: {Colors.CYAN}{output_file}{Colors.RESET}")
            print(f"\n{Colors.BLUE}📋 CSV文件包含 {len(all_wallet_data)} 行数据{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.RED}❌ 保存CSV文件时出错: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}请确保已安装pandas、eth-account和bip32utils库:{Colors.RESET}")
            print(f"{Colors.CYAN}pip install pandas eth-account bip32utils{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ 没有成功生成任何钱包地址{Colors.RESET}")

if __name__ == "__main__":
    main()
