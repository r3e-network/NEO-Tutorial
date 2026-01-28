#!/usr/bin/env python3
"""
NEO 交易结构解析器
实践示例 - 演示如何解析和构建NEO交易

依赖安装: pip install requests
"""

import json
import hashlib
from typing import Dict, List, Any


class NeoTransaction:
    """NEO交易结构类"""
    
    # 交易类型映射
    TX_TYPES = {
        0x00: 'MinerTransaction',
        0x01: 'IssueTransaction', 
        0x02: 'ClaimTransaction',
        0x20: 'EnrollmentTransaction',
        0x40: 'RegisterTransaction',
        0x80: 'ContractTransaction',
        0xd0: 'PublishTransaction',
        0xd1: 'InvocationTransaction'
    }
    
    def __init__(self):
        self.type = 0x80  # 默认ContractTransaction
        self.version = 0
        self.attributes = []
        self.inputs = []
        self.outputs = []
        self.scripts = []
    
    def add_attribute(self, usage: int, data: str):
        """添加交易属性"""
        self.attributes.append({
            'usage': usage,
            'data': data
        })
    
    def add_input(self, txid: str, vout: int):
        """添加交易输入（引用之前的UTXO）"""
        self.inputs.append({
            'txid': txid,
            'vout': vout
        })
    
    def add_output(self, asset_id: str, value: str, address: str):
        """添加交易输出"""
        self.outputs.append({
            'asset': asset_id,
            'value': value,
            'address': address
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'type': self.TX_TYPES.get(self.type, 'Unknown'),
            'version': self.version,
            'attributes': self.attributes,
            'vin': self.inputs,
            'vout': [
                {**out, 'n': i} 
                for i, out in enumerate(self.outputs)
            ],
            'scripts': self.scripts
        }
    
    def to_json(self, indent=2) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=indent)


def parse_transaction(tx_json: Dict) -> None:
    """解析并打印交易详情"""
    print("\n" + "=" * 50)
    print("交易解析结果")
    print("=" * 50)
    
    print(f"\n📋 基本信息:")
    print(f"   交易ID: {tx_json.get('txid', 'N/A')}")
    print(f"   类型: {tx_json.get('type', 'N/A')}")
    print(f"   版本: {tx_json.get('version', 0)}")
    print(f"   大小: {tx_json.get('size', 'N/A')} bytes")
    
    # 解析输入
    inputs = tx_json.get('vin', [])
    print(f"\n📥 输入 ({len(inputs)} 个):")
    for i, inp in enumerate(inputs):
        print(f"   [{i}] txid: {inp['txid'][:16]}...")
        print(f"       vout: {inp['vout']}")
    
    # 解析输出
    outputs = tx_json.get('vout', [])
    print(f"\n📤 输出 ({len(outputs)} 个):")
    for out in outputs:
        print(f"   [{out['n']}] {out['value']} -> {out['address']}")
    
    # 解析属性
    attrs = tx_json.get('attributes', [])
    if attrs:
        print(f"\n🏷️  属性 ({len(attrs)} 个):")
        for attr in attrs:
            print(f"   usage={attr['usage']}: {attr['data'][:32]}...")


# 示例交易数据
SAMPLE_TX = {
    "txid": "0xee85d489e4428a538f39c1903771e1f222a383f8327c96ed19cc02079149a1fd",
    "size": 665,
    "type": "ContractTransaction",
    "version": 0,
    "attributes": [],
    "vout": [
        {
            "n": 0,
            "asset": "0xc56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b",
            "value": "1000",
            "address": "Ae2d6qj91YL3LVUMkza7WQsaTYjzjHm4z1"
        },
        {
            "n": 1,
            "asset": "0xc56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b", 
            "value": "99999000",
            "address": "AWHX6wX5mEJ4Vwg7uBcqESeq3NggtNFhzD"
        }
    ],
    "vin": [
        {
            "txid": "0x3631f66024ca6f5b033d7e0809eb993443374830025af904fb51b0334f127cda",
            "vout": 0
        }
    ],
    "sys_fee": "0",
    "net_fee": "0",
    "scripts": []
}


if __name__ == '__main__':
    print("=" * 50)
    print("NEO 交易结构解析器")
    print("=" * 50)
    
    # 解析示例交易
    parse_transaction(SAMPLE_TX)
    
    print("\n" + "=" * 50)
    print("构建新交易示例")
    print("=" * 50)
    
    # 构建新交易
    tx = NeoTransaction()
    tx.add_input(
        "0x3631f66024ca6f5b033d7e0809eb993443374830025af904fb51b0334f127cda",
        0
    )
    tx.add_output(
        "0xc56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b",
        "100",
        "Ae2d6qj91YL3LVUMkza7WQsaTYjzjHm4z1"
    )
    
    print("\n构建的交易:")
    print(tx.to_json())
