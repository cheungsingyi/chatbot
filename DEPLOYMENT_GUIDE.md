# Chatbot3 Deployment Guide

## Overview

This guide is for IT administrators and technical staff responsible for deploying Chatbot3 to end users.

## Deployment Architecture

**Model**: Copy-to-Local Distribution
- Users receive a complete project folder
- Each user has an isolated instance on their local hard drive
- No shared resources or network dependencies
- Each instance uses its own SQLite database
- Full isolation prevents conflicts and ensures privacy

## Prerequisites

### On Distribution Server (Your Machine)

- Python 3.10 or higher
- Git (for version control)
- ZIP utility (for packaging)

### On User Machines (Windows 11)

- Python 3.10 or higher installed
- Internet access (for initial dependency installation)
- ~500 MB free disk space per installation
- Administrator rights (for Python installation only)

## Preparation Steps

### 1. Create Distribution Package

On your development machine:

```bash
# Navigate to project directory
cd /path/to/chatbot3

# Remove development artifacts
rm -rf venv/
rm -rf __pycache__/
rm -rf */__pycache__/
rm -rf */*/__pycache__/
rm -f chatbot.db
rm -f chatbot.db-shm
rm -f chatbot.db-wal
rm -f chainlit.log
rm -f chainlit.pid

# Create distribution archive
cd ..
zip -r chatbot3-distribution.zip chatbot3/ -x "*.git*" "*/__pycache__/*" "*.pyc" "*.pyo"
```

### 2. Prepare API Key Distribution

**Option A: Pre-configured .env (Simpler but Less Secure)**

Create a `.env` file with company API key:

```bash
cd chatbot3
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY
```

⚠️ **Security Warning**: All users share the same API key. See RISKS_AND_CONSIDERATIONS.md.

**Option B: User-Managed API Keys (More Secure)**

Users create their own `.env` files:
1. Distribute `.env.example` only
2. Provide API key provisioning process
3. Users follow USER_GUIDE.md to configure

### 3. Test the Package

Before distributing:

```bash
# Extract to test location
unzip chatbot3-distribution.zip -d C:\test-deployment

# Navigate to extracted folder
cd C:\test-deployment\chatbot3

# Run installation checker
install_check.bat

# Launch chatbot
start.bat

# Verify functionality
# - Check browser opens at localhost:8001
# - Send test message
# - Verify response
# - Check persistence (refresh page, verify thread shows in sidebar)
```

## Distribution Methods

### Method 1: Shared Network Drive

1. Copy `chatbot3-distribution.zip` to shared drive:
   ```
   \\company-server\shared\software\chatbot3\chatbot3-distribution.zip
   ```

2. Distribute instructions to users:
   ```
   1. Navigate to \\company-server\shared\software\chatbot3\
   2. Copy chatbot3-distribution.zip to your desktop
   3. Right-click → Extract All → Extract to C:\
   4. Open C:\chatbot3\
   5. Read USER_GUIDE.md
   6. Run install_check.bat
   7. Run start.bat
   ```

### Method 2: Email Distribution

1. Compress `chatbot3-distribution.zip` if needed (should be <25 MB without venv)
2. Email to users with installation instructions
3. Include USER_GUIDE.md content in email body

### Method 3: USB Drive

1. Copy `chatbot3-distribution.zip` to USB drives
2. Include printed instructions
3. Physically distribute to users

### Method 4: Software Management System

Deploy via company software management system (SCCM, Intune, etc.):

1. Create installation script:
   ```batch
   @echo off
   powershell -Command "Expand-Archive -Path '%~dp0chatbot3-distribution.zip' -DestinationPath 'C:\' -Force"
   echo Installation complete. See C:\chatbot3\USER_GUIDE.md
   ```

2. Package with distribution archive
3. Deploy via management system

## Post-Deployment

### User Onboarding

Provide users with:
1. **USER_GUIDE.md** - Complete usage instructions
2. **Support contact** - Who to contact for issues
3. **API key instructions** - How to obtain/configure (if Option B)

### Initial Support Period

Expect common issues during first week:
- Python installation problems
- .env configuration errors
- Firewall blocking localhost:8001
- Confusion about where to install

### Monitoring and Maintenance

**No central logging**: Each installation is isolated
- Users must report issues directly
- No telemetry or usage analytics
- No automatic updates

**Update Process**:
1. Create new distribution package with updates
2. Communicate changes to users
3. Users manually replace files or reinstall

## Verification Checklist

Before declaring deployment successful, verify:

- [ ] User can extract and install to `C:\chatbot3\`
- [ ] `install_check.bat` passes all checks
- [ ] `start.bat` successfully launches chatbot
- [ ] Browser opens at `http://localhost:8001`
- [ ] User can send message and receive response
- [ ] Conversation persists after browser refresh
- [ ] Thread appears in sidebar after page reload
- [ ] User can resume previous conversation

## Common Deployment Issues

### Python Not Installed

**Symptom**: `install_check.bat` fails with "Python is not installed"

**Solution**: 
- Pre-install Python 3.10+ company-wide
- Or include Python installation instructions
- Ensure "Add Python to PATH" is checked during installation

### Antivirus Blocking

**Symptom**: `start.bat` hangs or chainlit command fails

**Solution**:
- Whitelist `C:\chatbot3\` in antivirus
- Whitelist Python executable
- Request IT to add exception

### Port 8001 Already In Use

**Symptom**: Error "Address already in use"

**Solution**: Modify `start.bat` to use different port:
```batch
chainlit run app.py -h --port 8002
```

### Database Permission Errors

**Symptom**: "Unable to open database file"

**Solution**:
- Ensure user has write permissions to `C:\chatbot3\`
- Don't install in Program Files (restricted permissions)

## Rollback Plan

If deployment fails:

1. **Immediate**: Instruct users to close chatbot (Ctrl+C)
2. **Remove**: Users delete `C:\chatbot3\` folder
3. **Investigate**: Collect error reports from users
4. **Fix**: Address issues in distribution package
5. **Retest**: Verify on clean test machine
6. **Redeploy**: Distribute updated package

## Security Recommendations

See **RISKS_AND_CONSIDERATIONS.md** for detailed security analysis.

**Key Points**:
- Each user has isolated database (privacy)
- No network communication between instances
- API key management is primary security concern
- Source code is visible in current implementation

## Next Steps

After successful deployment:

1. **Monitor feedback** - First 2 weeks are critical
2. **Document issues** - Create FAQ for common problems
3. **Plan updates** - Establish update distribution process
4. **Gather metrics** - Track adoption and usage (manually via user feedback)

## Support Resources

**For Users**: Direct them to `USER_GUIDE.md`

**For Admins**:
- Review `test_persistence.py` for database diagnostics
- Check `chainlit.log` for application errors
- Examine `chatbot.db` with SQLite browser if needed

## Contact

For technical issues with this deployment guide:
- Check project documentation
- Review RISKS_AND_CONSIDERATIONS.md
- Consult with development team
