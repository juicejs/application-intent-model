# Sinth — the CLI for AIM

**Synthesize intent into reality.**

Python CLI tool for managing AIM packages from the registry.

## Quick Start

### Installation

**From PyPI** (once published):
```bash
pip install sinth
sinth fetch weather
```

**From source**:
```bash
cd cli/
pip install -e .
sinth fetch weather
```

**Standalone script**:
```bash
python3 cli/aim_cli/cli.py fetch weather
```

## Documentation

- **[CLI.md](./CLI.md)** - User guide and command reference
- **[PUBLISHING.md](./PUBLISHING.md)** - Guide for publishing to PyPI

## Components

- 🎯 `sinth` - Interactive menu for all operations
- 📦 `sinth init` - Initialize AIM project
- ⬇️ `sinth fetch <package>` - Fetch packages from registry
- 📋 `sinth list` - List installed packages
- ✅ `sinth validate` - Validate intent files
- ℹ️ `sinth info <package>` - Show package information
- ⚙️ `sinth config` - Configuration wizard and management
- 🔄 `sinth synth <package>` - Generate synthesis prompts

## Requirements

- Python 3.6+
- No external dependencies (pure stdlib)

## For Developers

**Install in development mode**:
```bash
cd cli/
pip install -e .
```

**Build package**:
```bash
pip install build
python -m build
```

**Run tests**:
```bash
python -m aim_cli --help
sinth fetch weather
```

## License

MIT License - see [LICENSE](./LICENSE)
