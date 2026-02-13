---
layout: post
lang: en
lang-ref: Development_set_up
---


# Neo N3 Smart Contract Development Environment

>
> **Objective**: Set up the Neo N3 development environment
>
> **Main points**:
>
> 1. System requirements
>
> 2. .NET SDK Setup
>
> 3. Neo N3 Smart Contract Template
>


For Neo N3 C# developers, the development experience has been significantly improved. Neo N3 uses modern .NET (not .NET Framework) and provides official templates and tools for smart contract development.

## Environment

Neo N3 smart contract development supports **Windows, macOS, and Linux**. The cross-platform .NET SDK makes it easy to develop on any operating system.

### Requirements

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later
- [Visual Studio 2022](https://visualstudio.microsoft.com/vs/community/) (Windows/Mac) or [VS Code](https://code.visualstudio.com/) with C# extension
- [Neo N3 Smart Contract Template](https://github.com/neo-project/neo-devpack-dotnet)

### Install .NET SDK

Download and install the .NET 8.0 SDK (or later) from the official Microsoft website.

Verify installation:
```bash
dotnet --version
```

### Install Neo Contract Template

```bash
dotnet new install Neo.SmartContract.Template
```

This installs the official Neo N3 smart contract project template.

### Create a New Contract Project

```bash
dotnet new neo-contract -n MyContract
cd MyContract
```

This creates a new Neo N3 smart contract project with the proper structure and references.

### Project Structure

```
MyContract/
├── MyContract.csproj
├── MyContract.cs
└── ...
```

The generated `.csproj` file includes references to `Neo.SmartContract.Framework`.

### Visual Studio Setup (Optional)

If using Visual Studio 2022:

1. Install Visual Studio 2022 with ".NET desktop development" workload
2. Open the `.csproj` file created above
3. Build the project (Ctrl+Shift+B)

### VS Code Setup (Optional)

If using VS Code:

1. Install the C# extension
2. Open the project folder
3. Use terminal to build: `dotnet build`

### Alternative: Using Neo Express

[Neo Express](https://github.com/neo-project/neo-express) is a tool for creating and managing Neo N3 local networks, designed for development and testing:

```bash
dotnet tool install -g neo-express
neo-express init
neo-express start
```

## Next Step
**Congratulations!**, After set up the development tools, next step is to [compile the contract, deploy it and invoke it.](Development_compile.md)

## Previous Step
If you are not set up the private chain yet , you may first click [here](Development_privateChain.md).
