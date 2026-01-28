#!/usr/bin/env python3
"""
NEP-5 合约交互工具
实践示例 - 演示如何与NEP-5合约交互

注意: 此示例需要连接到NEO节点
"""

import json
from typing import Optional

# NEP-5 标准方法
NEP5_METHODS = {
    'name': '获取代币名称',
    'symbol': '获取代币符号', 
    'decimals': '获取小数位数',
    'totalSupply': '获取总供应量',
    'balanceOf': '查询账户余额',
    'transfer': '转账'
}


def address_to_scripthash(address: str) -> str:
    """将NEO地址转换为脚本哈希（小端序）"""
    import base58
    import hashlib
    
    decoded = base58.b58decode(address)
    # 去掉版本前缀(1字节)和校验和(4字节)
    script_hash = decoded[1:-4]
    # 转换为小端序十六进制
    return script_hash[::-1].hex()


def build_invoke_script(contract_hash: str, method: str, params: list) -> dict:
    """构建调用脚本"""
    return {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [contract_hash, method, params],
        "id": 1
    }


def format_balance(raw_balance: int, decimals: int = 8) -> str:
    """格式化余额显示"""
    return f"{raw_balance / (10 ** decimals):.{decimals}f}"


class NEP5Token:
    """NEP-5代币类"""
    
    def __init__(self, contract_hash: str, name: str = "", symbol: str = ""):
        self.contract_hash = contract_hash
        self.name = name
        self.symbol = symbol
        self.decimals = 8
    
    def get_balance_params(self, address: str) -> dict:
        """获取查询余额的RPC参数"""
        script_hash = address_to_scripthash(address)
        return build_invoke_script(
            self.contract_hash,
            "balanceOf",
            [{"type": "Hash160", "value": script_hash}]
        )
    
    def get_transfer_params(self, from_addr: str, to_addr: str, amount: int) -> dict:
        """获取转账的RPC参数"""
        from_hash = address_to_scripthash(from_addr)
        to_hash = address_to_scripthash(to_addr)
        return build_invoke_script(
            self.contract_hash,
            "transfer",
            [
                {"type": "Hash160", "value": from_hash},
                {"type": "Hash160", "value": to_hash},
                {"type": "Integer", "value": str(amount)}
            ]
        )


# 示例代币
SAMPLE_TOKENS = {
    'NEO': {
        'hash': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
        'name': 'NEO',
        'symbol': 'NEO',
        'decimals': 0
    },
    'GAS': {
        'hash': '602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7',
        'name': 'GAS',
        'symbol': 'GAS', 
        'decimals': 8
    }
}


if __name__ == '__main__':
    print("=" * 50)
    print("NEP-5 合约交互工具")
    print("=" * 50)
    
    print("\n📋 NEP-5 标准方法:")
    for method, desc in NEP5_METHODS.items():
        print(f"   {method}: {desc}")
    
    print("\n📦 示例代币:")
    for name, info in SAMPLE_TOKENS.items():
        print(f"   {name}: {info['hash'][:16]}...")
    
    # 演示构建RPC调用
    print("\n🔧 构建balanceOf调用示例:")
    token = NEP5Token(SAMPLE_TOKENS['NEO']['hash'], 'NEO', 'NEO')
    params = token.get_balance_params("AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y")
    print(json.dumps(params, indent=2))
