#!/usr/bin/env python3
"""
NEO 私钥和地址生成器
实践示例 - 演示如何从私钥生成NEO地址

依赖安装: pip install ecdsa base58
"""

import hashlib
import os
import base58

# 尝试导入ecdsa，如果没有则提供安装提示
try:
    from ecdsa import SigningKey, NIST256p
except ImportError:
    print("请先安装依赖: pip install ecdsa base58")
    exit(1)


def generate_private_key():
    """生成256位随机私钥"""
    return os.urandom(32)


def private_key_to_wif(private_key: bytes) -> str:
    """
    将私钥转换为WIF格式
    WIF = Base58Check(0x80 + private_key)
    """
    # 添加版本前缀 0x80
    extended_key = b'\x80' + private_key
    
    # 双重SHA256哈希
    first_hash = hashlib.sha256(extended_key).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    
    # 添加校验和（前4字节）
    checksum = second_hash[:4]
    final_key = extended_key + checksum
    
    # Base58编码
    return base58.b58encode(final_key).decode('utf-8')


def private_key_to_public_key(private_key: bytes) -> bytes:
    """
    使用secp256r1曲线从私钥导出公钥
    返回压缩格式的公钥（33字节）
    """
    signing_key = SigningKey.from_string(private_key, curve=NIST256p)
    verifying_key = signing_key.get_verifying_key()
    
    # 获取公钥点坐标
    x = verifying_key.pubkey.point.x()
    y = verifying_key.pubkey.point.y()
    
    # 压缩公钥格式: 前缀(02或03) + x坐标
    prefix = b'\x02' if y % 2 == 0 else b'\x03'
    compressed_pubkey = prefix + x.to_bytes(32, 'big')
    
    return compressed_pubkey


def public_key_to_script_hash(public_key: bytes) -> bytes:
    """
    从公钥生成脚本哈希
    脚本 = 0x21 + 公钥 + 0xAC (CHECKSIG)
    脚本哈希 = RIPEMD160(SHA256(脚本))
    """
    # 构建验证脚本
    script = b'\x21' + public_key + b'\xAC'
    
    # SHA256哈希
    sha256_hash = hashlib.sha256(script).digest()
    
    # RIPEMD160哈希
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    script_hash = ripemd160.digest()
    
    return script_hash


def script_hash_to_address(script_hash: bytes) -> str:
    """
    从脚本哈希生成NEO地址
    地址 = Base58Check(0x17 + script_hash)
    """
    # 添加版本前缀 0x17 (NEO地址以'A'开头)
    extended_hash = b'\x17' + script_hash
    
    # 双重SHA256哈希
    first_hash = hashlib.sha256(extended_hash).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    
    # 添加校验和
    checksum = second_hash[:4]
    final_data = extended_hash + checksum
    
    # Base58编码
    return base58.b58encode(final_data).decode('utf-8')


def generate_neo_account():
    """生成完整的NEO账户信息"""
    # 1. 生成私钥
    private_key = generate_private_key()
    
    # 2. 转换为WIF
    wif = private_key_to_wif(private_key)
    
    # 3. 导出公钥
    public_key = private_key_to_public_key(private_key)
    
    # 4. 生成脚本哈希
    script_hash = public_key_to_script_hash(public_key)
    
    # 5. 生成地址
    address = script_hash_to_address(script_hash)
    
    return {
        'private_key': private_key.hex(),
        'wif': wif,
        'public_key': public_key.hex(),
        'script_hash': script_hash.hex(),
        'address': address
    }


if __name__ == '__main__':
    print("=" * 60)
    print("NEO 账户生成器")
    print("=" * 60)
    
    account = generate_neo_account()
    
    print(f"\n私钥 (Hex):     {account['private_key']}")
    print(f"WIF:            {account['wif']}")
    print(f"公钥 (压缩):    {account['public_key']}")
    print(f"脚本哈希:       {account['script_hash']}")
    print(f"NEO地址:        {account['address']}")
    
    print("\n" + "=" * 60)
    print("⚠️  警告: 请妥善保管私钥，切勿泄露！")
    print("=" * 60)
