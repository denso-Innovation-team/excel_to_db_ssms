"""
README.md - Project Documentation
"""

# 🏭 DENSO888 - Excel to SQL Management System

Modern desktop application for importing Excel data to SQL databases with mock data generation capabilities.

## 🚀 Features

### ✅ Core Functionality

- **Excel Import**: Support for .xlsx, .xls, .xlsm files
- **Database Support**: SQLite (local) and SQL Server (network)
- **Mock Data Generation**: Generate realistic test data with multiple templates
- **Data Processing**: Automatic type detection and data cleaning
- **Real-time Progress**: Live progress tracking with cancellation support

### 🎨 Modern UI/UX

- **Modular Design**: Clean, maintainable architecture
- **DENSO Branding**: Corporate colors and styling
- **Responsive Layout**: Adaptive interface with scrollable content
- **Dark/Light Themes**: Multiple theme support
- **Thai/English**: Localization support

### 🛠️ Technical Features

- **Batch Processing**: Efficient handling of large files
- **Error Recovery**: Robust error handling and logging
- **Connection Pooling**: Optimized database connections
- **Memory Management**: Efficient resource usage
- **Configuration Management**: Persistent settings and preferences

## 📦 Installation

### Option 1: Download Executable (Recommended)

1. Download `DENSO888-2.0.0-setup.exe` from releases
2. Run installer and follow instructions
3. Launch from desktop or start menu

### Option 2: Run from Source

'''bash

# Clone repository

git clone <https://github.com/denso888/excel-to-database.git>
cd excel-to-database

# Install dependencies

pip install -r requirements.txt

# Run application

python main.py
'''

## 🖥️ System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Database**: SQLite (included) or SQL Server 2016+

## 📋 Quick Start Guide

### 1. Database Setup

1. Open **Database** tab
2. Choose SQLite (default) or SQL Server
3. Configure connection settings
4. Click **Test Connection**

### 2. Import Excel Data

1. Go to **Import Excel** tab
2. Click **Browse** or drag & drop Excel file
3. Review file information and data preview
4. Enter table name
5. Click **Import to Database**

### 3. Generate Mock Data

1. Open **Mock Data** tab
2. Select data template (employees, sales, etc.)
3. Choose number of records
4. Click **Generate Mock Data**

## 🏗️ Architecture

### 📁 Project Structure

'''
excel_to_database/
├── 📱 gui/ # User Interface Layer
│ ├── components/ # Reusable UI components
│ ├── pages/ # Feature-specific pages
│ ├── themes/ # UI theming system
│ └── main_window.py # Main application window
├── 🎛️ controllers/ # Business Logic Layer
│ └── app_controller.py # Main application controller
├── 🔧 core/ # Domain Logic Layer
│ ├── database_manager.py # Database operations
│ ├── excel_handler.py # Excel processing
│ └── mock_generator.py # Mock data generation
├── 📊 models/ # Data Models
│ ├── app_config.py # Application configuration
│ └── database_config.py # Database settings
├── 🛠️ utils/ # Utility Functions
├── 🎨 assets/ # Static Assets
└── 📦 build/ # Build & Distribution
'''

### 🔄 Data Flow

'''
UI Layer → Controller → Core Logic → Database
↑ ↓
← Event System ← Progress Updates ←──┘
'''

## 🛠️ Development

### Setup Development Environment

'''bash

# Create virtual environment

python -m venv venv
source venv/bin/activate # Linux/Mac

# or

venv\Scripts\activate # Windows

# Install development dependencies

pip install -r build/requirements.txt

# Run in development mode

python main.py
'''

### Build Executable

'''bash

# Build single executable

python build/build_exe.py

# Or use batch script (Windows)

run_build.bat
'''

### Testing

'''bash

# Run unit tests

python -m pytest tests/

# Run specific test

python -m pytest tests/test_database.py
'''

## 📝 Configuration

### Application Settings (`config/settings.json`)

'''json
{
"app_name": "DENSO888",
"version": "2.0.0",
"window_width": 1200,
"window_height": 800,
"theme": "denso",
"language": "th",
"batch_size": 1000,
"max_workers": 4,
"enable_mock_data": true,
"auto_save_preferences": true
}
'''

### Database Configuration

- **SQLite**: Local file-based database (default: `denso888_data.db`)
- **SQL Server**: Network database with Windows/SQL authentication
- **Connection Pooling**: Automatic connection management
- **Timeout Settings**: Configurable connection and command timeouts

### User Preferences (`config/preferences.json`)

- Window state and positioning
- Recent files list
- Database connection preferences
- Import/export settings
- Theme and language preferences

## 🔧 Troubleshooting

### Common Issues

#### ❌ "Database connection failed"

**Solutions:**

- Check SQL Server service is running
- Verify server name and database name
- Ensure Windows Authentication or correct credentials
- Check network connectivity and firewall settings

#### ❌ "Excel file cannot be read"

**Solutions:**

- Ensure file is not password protected
- Check file is not corrupted
- Verify file format (.xlsx, .xls, .xlsm)
- Close file in Excel before importing

#### ❌ "Application won't start"

**Solutions:**

- Install Microsoft Visual C++ Redistributable
- Update Windows to latest version
- Run as Administrator
- Check antivirus software isn't blocking

#### ❌ "Out of memory errors"

**Solutions:**

- Process large files in smaller chunks
- Close other applications
- Increase system virtual memory
- Use 64-bit version of application

### Logging and Diagnostics

**Log Locations:**

- Application logs: `logs/denso888.log`
- Error logs: `logs/error.log`
- User preferences: `config/preferences.json`

**Enable Debug Mode:**

1. Open `config/settings.json`
2. Set `"log_level": "DEBUG"`
3. Restart application

## 🧪 Mock Data Templates

### Available Templates

1. **Employees** (1,000+ realistic employee records)

   - Personal information with Thai/English names
   - Department hierarchy and positions
   - Salary calculations based on role
   - Performance metrics and status

2. **Sales** (5,000+ transaction records)

   - Customer purchase patterns
   - Product catalog with pricing
   - Seasonal trends and discounts
   - Payment methods and delivery tracking

3. **Inventory** (2,000+ product items)

   - Stock levels and reorder points
   - Supplier information
   - Quality status and expiry dates
   - Warehouse locations

4. **Financial** (1,000+ transaction records)

   - Chart of accounts structure
   - Tax calculations and compliance
   - Approval workflows
   - Fiscal year reporting

5. **Custom** (Flexible schema)
   - User-defined column types
   - Configurable data patterns
   - Custom validation rules

## 🎨 Theming and Customization

### DENSO Corporate Theme

- **Primary Color**: #DC0003 (DENSO Red)
- **Typography**: Segoe UI font family
- **Icons**: Modern flat design with emoji support
- **Layout**: Clean, professional interface

### Custom Themes

Create custom themes by extending `DensoTheme` class:

'''python
class CustomTheme(DensoTheme):
def **init**(self):
super().**init**()
self.colors.primary = "#YOUR_COLOR"
self.colors.secondary = "#YOUR_SECONDARY"
'''

## 🌐 Localization

### Supported Languages

- **Thai (th)**: Default for Thai users
- **English (en)**: International users

### Adding New Languages

1. Create language file: `assets/i18n/your_language.json`
2. Translate all UI strings
3. Update language selection in settings

## 📊 Performance Optimization

### Large File Processing

- **Chunked Reading**: Process files in configurable chunks
- **Memory Management**: Automatic garbage collection
- **Progress Tracking**: Real-time progress with cancellation
- **Error Recovery**: Skip corrupted rows and continue

### Database Optimization

- **Connection Pooling**: Reuse database connections
- **Batch Inserts**: Insert multiple rows efficiently
- **Index Creation**: Automatic index generation
- **Transaction Management**: Proper transaction handling

## 🔒 Security Considerations

### Data Protection

- **Password Masking**: Secure password input fields
- **Connection Encryption**: SSL/TLS for SQL Server
- **Local Storage**: Encrypted configuration files
- **Access Control**: User-based permissions

### Best Practices

- Use Windows Authentication when possible
- Regularly backup database files
- Keep application updated
- Monitor log files for security events

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Style

- Follow PEP 8 Python style guide
- Use type hints for all functions
- Add docstrings for all classes and methods
- Write unit tests for new features

### Testing Guidelines

- Test on multiple Windows versions
- Verify with different Excel file formats
- Test with various database configurations
- Check performance with large datasets

## 📄 License

© 2024 DENSO Corporation  
All rights reserved.

This software is proprietary and confidential. Unauthorized reproduction or distribution is prohibited.

## 🙏 Acknowledgments

### Development Team

- **Thammaphon Chittasuwanna (SDM)** - Lead Developer & Architect
- **Innovation Department** - Requirements & Testing
- **DENSO Corporation** - Project Sponsorship

### Technology Stack

- **Python 3.8+** - Core programming language
- **Tkinter** - GUI framework
- **Pandas** - Data processing
- **SQLAlchemy** - Database abstraction
- **OpenPyXL** - Excel file handling
- **PyInstaller** - Executable packaging

### Special Thanks

- DENSO IT Department for infrastructure support
- Beta testers for valuable feedback
- Open source community for excellent libraries

## 📞 Support

### Internal Support (DENSO Employees)

- **Email**: <thammaphon.chittasuwanna@denso.com>
- **Teams**: @ทอม Innovation Department
- **Internal Wiki**: DENSO888 Documentation Portal

### Documentation

- **User Guide**: `docs/USER_GUIDE.md`
- **Developer Guide**: `docs/DEVELOPER_GUIDE.md`
- **API Reference**: `docs/api/`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`

### Feedback and Bug Reports

Please report issues through:

1. Internal issue tracking system
2. Email with detailed error logs
3. Teams chat with screenshots

---

## 🎯 Roadmap

### Version 2.1 (Q2 2025)

- [ ] Advanced data validation rules
- [ ] Custom SQL query builder
- [ ] Data transformation pipeline
- [ ] Excel template generator

### Version 2.2 (Q3 2025)

- [ ] Cloud database support (Azure SQL)
- [ ] REST API integration
- [ ] Automated scheduling
- [ ] Advanced analytics dashboard

### Version 3.0 (Q4 2025)

- [ ] Web-based interface
- [ ] Multi-user collaboration
- [ ] Real-time data sync
- [ ] Machine learning data insights

---

**เฮียตอมจัดหั้ย!!! 🚀**  
_Innovation never stops at DENSO888_

---

## 📋 Quick Reference

### Keyboard Shortcuts

- `Ctrl + O` - Open file dialog
- `Ctrl + Q` - Quit application
- `F5` - Refresh current page
- `Ctrl + ,` - Open preferences

### File Formats Supported

- **Excel 2007+**: .xlsx, .xlsm
- **Excel 97-2003**: .xls
- **Maximum file size**: 100MB (configurable)

### Database Limits

- **SQLite**: Up to 281 TB database size
- **SQL Server**: Enterprise edition limits
- **Batch size**: 1,000 rows (configurable)
- **Connection timeout**: 30 seconds (configurable)

### System Performance

- **Recommended RAM**: 8GB
- **Processing speed**: ~10,000 rows/minute
- **Concurrent operations**: 4 workers (configurable)
- **Network timeout**: 30 seconds

### Error Codes

- **E001**: Database connection failed
- **E002**: File format not supported
- **E003**: Insufficient memory
- **E004**: Network timeout
- **E005**: Permission denied

---

_This documentation is maintained by the DENSO888 development team.  
Last updated: June 2025_
