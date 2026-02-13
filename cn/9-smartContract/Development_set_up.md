---
layout: post
lang: cn
lang-ref: Development_set_up
---


# Neo N3智能合约开发环境

>
> **目的**: 设置Neo N3开发环境
>
> **要点**:
>
> 1. 系统要求
>
> 2. .NET SDK安装
>
> 3. Neo N3智能合约模板

对于Neo N3 C#开发者来说，开发体验得到了显著改善。Neo N3使用现代.NET（而不是.NET Framework），并为智能合约开发提供了官方模板和工具。

## 开发环境

Neo N3智能合约开发支持**Windows、macOS和Linux**。跨平台的.NET SDK使得在任何操作系统上开发都很容易。

### 系统要求

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) 或更高版本
- [Visual Studio 2022](https://visualstudio.microsoft.com/vs/community/) (Windows/Mac) 或 [VS Code](https://code.visualstudio.com/) 配合C#扩展
- [Neo N3智能合约模板](https://github.com/neo-project/neo-devpack-dotnet)

### 安装.NET SDK

从微软官方网站下载并安装.NET 8.0 SDK（或更高版本）。

验证安装：
```bash
dotnet --version
```

### 安装Neo合约模板

```bash
dotnet new install Neo.SmartContract.Template
```

这将安装官方的Neo N3智能合约项目模板。

### 创建新的合约项目

```bash
dotnet new neo-contract -n MyContract
cd MyContract
```

这将创建一个具有正确结构和引用的新Neo N3智能合约项目。

### 项目结构

```
MyContract/
├── MyContract.csproj
├── MyContract.cs
└── ...
```

生成的`.csproj`文件包含对`Neo.SmartContract.Framework`的引用。

### Visual Studio设置（可选）

如果使用Visual Studio 2022：

1. 安装Visual Studio 2022，勾选".NET桌面开发"工作负载
2. 打开上面创建的`.csproj`文件
3. 构建项目（Ctrl+Shift+B）

### VS Code设置（可选）

如果使用VS Code：

1. 安装C#扩展
2. 打开项目文件夹
3. 使用终端构建：`dotnet build`

### 替代方案：使用Neo Express

[Neo Express](https://github.com/neo-project/neo-express)是一个用于创建和管理Neo N3本地网络的工具，专为开发和测试设计：

```bash
dotnet tool install -g neo-express
neo-express init
neo-express start
```

## 下一步
**恭喜！** 设置好开发工具后，下一步是[编译合约、部署并调用它](Development_compile.md)。

## 上一步
如果你还没有设置私有链，请先点击[这里](Development_privateChain.md)。
