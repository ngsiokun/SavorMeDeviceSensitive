#!/usr/bin/env python3
"""
SavorMe Project File Organization Script
Consolidates and organizes project files for better management
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create organized directory structure"""
    directories = [
        "docs/master",           # Master documentation
        "docs/archive",          # Archived documentation
        "scripts/startup",       # Startup scripts
        "scripts/legacy",        # Legacy scripts
        "tests",                 # Testing files
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def organize_documentation():
    """Organize documentation files"""
    
    # Master documentation (keep in root)
    master_docs = [
        "SAVORME_MASTER_GUIDE.md",
        "TECHNICAL_SPECIFICATION_COMPLETE.md", 
        "CUSTOMIZATIONS_PERSISTENT.md",
        "README.md"
    ]
    
    # Move to docs/master
    docs_master = [
        "AUTOMATED_APP_STARTUP_GUIDE.md",
        "STARTUP_GUIDE.md",
        "SYSTEM_DESIGN_FINAL.md",
        "PAGE_LAYOUTS_REFERENCE.md",
        "QUICK_IMPLEMENTATION_GUIDE.md"
    ]
    
    # Archive legacy documentation
    legacy_docs = [
        "AUTOMATED_REVIEW_IMPLEMENTATION_GUIDE.md",
        "AUTOMATIC_SETUP_IMPLEMENTATION.md",
        "CLONE_SETUP_GUIDE.md",
        "COMPREHENSIVE_UPDATE_SUMMARY.md",
        "DIRECTORY_CLEANUP_ANALYSIS.md",
        "documentation_fix_report.md",
        "DOCUMENTATION_REVIEW_CHECKLIST.md",
        "documentation_review_report.md",
        "EVIDENCE_BASED_MOODS_v2.md",
        "FINAL_VERIFICATION_CHECKLIST.md",
        "MAPPING_DATA_SOURCES.md",
        "MOOD_TO_RECIPE_FLOW.md",
        "QUICK_START_COMMANDS.md",
        "REVIEW_PROCESS_IMPROVEMENT_SUMMARY.md",
        "RUN_DEMO_INSTRUCTIONS.md",
        "SYSTEM_WORKFLOW.md",
        "CLEANUP_COMPLETION_REPORT.md"
    ]
    
    # Move files
    for doc in docs_master:
        if os.path.exists(doc):
            shutil.move(doc, f"docs/master/{doc}")
            print(f"📁 Moved to docs/master: {doc}")
    
    for doc in legacy_docs:
        if os.path.exists(doc):
            shutil.move(doc, f"docs/archive/{doc}")
            print(f"📦 Archived: {doc}")

def organize_scripts():
    """Organize startup scripts"""
    
    # Primary scripts (keep in root)
    primary_scripts = [
        "savorme_professional_startup.bat",
        "start_savorme_reliable.bat"
    ]
    
    # Move to scripts/startup
    startup_scripts = [
        "setup_new_clone.bat",
        "start_savorme_auto.bat",
        "start_backend.bat",
        "start_demo.bat",
        "start_app_reliable.bat"
    ]
    
    # Move to scripts/legacy
    legacy_scripts = [
        "start_with_setup.py"
    ]
    
    # Move files
    for script in startup_scripts:
        if os.path.exists(script):
            shutil.move(script, f"scripts/startup/{script}")
            print(f"🚀 Moved to scripts/startup: {script}")
    
    for script in legacy_scripts:
        if os.path.exists(script):
            shutil.move(script, f"scripts/legacy/{script}")
            print(f"📦 Moved to scripts/legacy: {script}")

def organize_testing_files():
    """Organize testing and utility files"""
    
    testing_files = [
        "test_imports.py",
        "test_api.json",
        "batch_fix_documentation.py",
        "docs_review_automation.py"
    ]
    
    for file in testing_files:
        if os.path.exists(file):
            shutil.move(file, f"tests/{file}")
            print(f"🧪 Moved to tests: {file}")

def create_file_index():
    """Create master file index"""
    
    index_content = """# SavorMe File Index

## 📁 **Root Directory Files** (Essential)
- `SAVORME_MASTER_GUIDE.md` - Complete application reference
- `TECHNICAL_SPECIFICATION_COMPLETE.md` - Technical implementation details
- `CUSTOMIZATIONS_PERSISTENT.md` - Design system and customizations
- `README.md` - Project overview
- `savorme_professional_startup.bat` - Main startup script
- `start_savorme_reliable.bat` - Backup startup script
- `requirements.txt` - Python dependencies
- `.env` - Environment variables
- `MASTER_FILE_ORGANIZATION.md` - File organization guide

## 📁 **Core Application**
- `app/` - Backend FastAPI application
- `demo_app/` - Frontend Flask application
- `venv/` - Python virtual environment

## 📁 **Documentation**
- `docs/master/` - Essential documentation
- `docs/archive/` - Archived documentation

## 📁 **Scripts**
- `scripts/startup/` - Startup scripts
- `scripts/legacy/` - Legacy scripts

## 📁 **Testing**
- `tests/` - Testing and utility files

## 🎯 **Quick Start**
1. Read `SAVORME_MASTER_GUIDE.md`
2. Run `savorme_professional_startup.bat`
3. Access http://localhost:5000

## 🔧 **Maintenance**
- Update this index when adding new files
- Archive old files instead of deleting
- Keep root directory clean and organized
"""
    
    with open("FILE_INDEX.md", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print("📋 Created FILE_INDEX.md")

def main():
    """Main organization function"""
    print("🗂️  SavorMe Project File Organization")
    print("=" * 50)
    
    # Create directory structure
    create_directory_structure()
    
    # Organize files
    organize_documentation()
    organize_scripts()
    organize_testing_files()
    
    # Create file index
    create_file_index()
    
    print("\n✅ File organization complete!")
    print("\n📋 Summary:")
    print("- Master documentation kept in root")
    print("- Essential docs moved to docs/master/")
    print("- Legacy docs archived to docs/archive/")
    print("- Startup scripts organized in scripts/")
    print("- Testing files moved to tests/")
    print("- Created FILE_INDEX.md for reference")
    
    print("\n🎯 Next steps:")
    print("1. Review FILE_INDEX.md")
    print("2. Test startup scripts still work")
    print("3. Update any hardcoded paths if needed")
    print("4. Commit organized structure to git")

if __name__ == "__main__":
    main()
