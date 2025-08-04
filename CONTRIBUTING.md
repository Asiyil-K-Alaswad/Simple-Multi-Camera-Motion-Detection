# Contributing to Simple Multi-Camera Motion Detection

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## How to Contribute

### 1. Fork the Repository

1. Go to [https://github.com/Asiyil-K-Alaswad/Simple-Multi-Camera-Motion-Detection](https://github.com/Asiyil-K-Alaswad/Simple-Multi-Camera-Motion-Detection)
2. Click the "Fork" button to create your own copy

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Simple-Multi-Camera-Motion-Detection.git
cd Simple-Multi-Camera-Motion-Detection
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes

- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed
- Test your changes thoroughly

### 5. Test Your Changes

Run the test scripts to ensure everything works:

```bash
# Test camera functionality
python test_camera_frames.py

# Test object tracking
python test_tracking_local.py

# Test demo mode
python test_demo.py
```

### 6. Commit Your Changes

```bash
git add .
git commit -m "Add feature: brief description of changes"
```

### 7. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 8. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Provide a clear description of your changes
5. Submit the pull request

## Code Style Guidelines

- Use meaningful variable and function names
- Add docstrings to functions and classes
- Follow PEP 8 style guidelines
- Keep functions focused and concise
- Add type hints where appropriate

## Testing Guidelines

- Test with different camera configurations
- Verify performance on different hardware
- Test edge cases and error conditions
- Ensure backward compatibility

## Documentation

- Update README.md if adding new features
- Add comments to complex code sections
- Update configuration guides if needed
- Include usage examples

## Issues and Bug Reports

When reporting issues:

1. Use the issue template if available
2. Provide detailed steps to reproduce
3. Include system information (OS, Python version, etc.)
4. Attach relevant logs or error messages
5. Describe expected vs actual behavior

## Questions and Discussion

For questions or general discussion:

1. Check existing issues and discussions
2. Create a new discussion thread
3. Be respectful and constructive
4. Provide context for your questions

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉 