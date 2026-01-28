# 持久化

> **注意**: 本章节已更新至 Neo N3 版本。

## 序列化模型
Neo N3 平台支持的原生数据类型有 Integer、ByteString、Array、Struct、Map、Boolean 等。该模型在持久化层和网络层中都有使用。

### 整数序列化

根据存储的值，可使用可变长度的类型对整数进行编码：
|数值|长度|格式|
|---|---|---|
|< 0xfd|1|uint8|
|<= 0xffff|3|0xfd + uint16|
|<= 0xffffffff|5|0xfe + uint32|
|> 0xffffffff|9|0xff + uint64|

使用一个字节存储数值1:

![single_byte](persistence_1_byte.png)

但是数值65535需要使用3个字节进行存储:

![three_bytes](persistence_3_bytes.png)

#### 整数序列化代码
你可以点击[此处](https://github.com/neo-project/neo/blob/master/src/Neo/IO/Helper.cs)查看C#版本的整数序列化代码:

``` CSharp
public static void WriteVarInt(this BinaryWriter writer, long value)
{
    if (value < 0)
        throw new ArgumentOutOfRangeException(nameof(value));
    if (value < 0xFD)
    {
        writer.Write((byte)value);
    }
    else if (value <= 0xFFFF)
    {
        writer.Write((byte)0xFD);
        writer.Write((ushort)value);
    }
    else if (value <= 0xFFFFFFFF)
    {
        writer.Write((byte)0xFE);
        writer.Write((uint)value);
    }
    else
    {
        writer.Write((byte)0xFF);
        writer.Write(value);
    }
}
```

#### 字节顺序
除IP地址和端口号外，Neo 中所有变长的整数类型都使用小端存储。

### 字符串序列化
字符串使用变长的字符串变量进行编码，由一个表示字符串长度的整数以及随后紧跟的以UTF8编码的字符串构成。

|长度|字段|类型|说明|
|---|---|---|---|
|**？**|length|integer|字符串的字节长度|
|**length**|string|uint8[length]|字符串本身|

你可以点击[此处](http://www.unicode.org/versions/Unicode9.0.0/ch03.pdf#page=54)查看关于序列化UTF-8编码的字符串的其他信息。

#### 示例
字符串`NEO`使用4个字节存储：

![var_string](persistence_var_string.png)

#### 字符串序列化代码
你可以点击[此处](https://github.com/neo-project/neo/blob/master/src/Neo/IO/Helper.cs)查看C＃版本的序列化字符串的代码：

``` CSharp
public static void WriteVarString(this BinaryWriter writer, string value)
{
    writer.WriteVarBytes(Encoding.UTF8.GetBytes(value));
}

public static void WriteVarBytes(this BinaryWriter writer, ReadOnlySpan<byte> value)
{
    writer.WriteVarInt(value.Length);
    writer.Write(value);
}
```

### UInt160 与 UInt256 序列化
UInt160和UInt256都存储为固定大小的字节数组，数组长度分别是20和32字节。Neo 使用 RIPEMD160 算法计算脚本哈希，并用 SHA256 算法计算交易和区块的哈希值。

请注意，在 Neo 中，我们会使用两次哈希函数。其中第一次始终是 SHA256。

UInt160最常用于计算合约的哈希值：

![contract](persistence_contract.png)

#### 合约哈希代码
在 Neo N3 中，合约哈希的计算方式有所改变。合约哈希由部署者的地址和合约的 NEF 校验和共同决定：

``` CSharp
// Neo N3 合约哈希计算
public static UInt160 GetContractHash(UInt160 sender, uint nefCheckSum, string name)
{
    using var sb = new ScriptBuilder();
    sb.Emit(OpCode.ABORT);
    sb.EmitPush(sender);
    sb.EmitPush(nefCheckSum);
    sb.EmitPush(name);
    return sb.ToArray().ToScriptHash();
}

// 脚本哈希计算
public static UInt160 ToScriptHash(this byte[] script)
{
    return new UInt160(script.Sha256().RIPEMD160());
}
```

#### 地址
在 Neo N3 中，地址格式有所改变。地址版本号更新为 `0x35`（53），因此所有 N3 地址都以字母 `N` 开头。

![address](persistence_address.png)

#### 地址转换代码
你可以点击[此处](https://github.com/neo-project/neo/blob/master/src/Neo/Wallets/Helper.cs)查看地址转换的代码示例：

``` CSharp
public static string ToAddress(this UInt160 scriptHash, byte addressVersion)
{
    Span<byte> data = stackalloc byte[21];
    data[0] = addressVersion;  // Neo N3: 0x35 (53)
    scriptHash.ToArray().CopyTo(data[1..]);
    return Base58.Base58CheckEncode(data);
}

public static UInt160 ToScriptHash(this string address, byte addressVersion)
{
    byte[] data = address.Base58CheckDecode();
    if (data.Length != 21)
        throw new FormatException();
    if (data[0] != addressVersion)
        throw new FormatException();
    return new UInt160(data.AsSpan(1));
}
```

### 十进制序列化
在 Neo N3 中，使用 `BigInteger` 来处理大整数运算。对于代币金额，通常使用整数表示最小单位，精度由合约定义（如 GAS 精度为 8 位小数）。

