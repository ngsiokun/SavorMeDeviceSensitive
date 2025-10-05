#!/usr/bin/env python3
"""
SavorMe Documentation Batch Fix Script
Professional AI Consultant - Automated Documentation Fixes

This script applies systematic fixes to documentation issues identified by the review process.
"""

import os
import re
from pathlib import Path
from typing import List, Dict

class DocumentationFixer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.fixes_applied = []
        self.current_version = "2.1.0"
        self.current_date = "October 5, 2025"
        
    def fix_version_numbers(self, file_path: Path) -> int:
        """Fix version number inconsistencies."""
        fixes = 0
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Common version patterns to fix
            version_fixes = [
                (r'version["\']?\s*:\s*["\']?2\.0\.0', f'version: {self.current_version}'),
                (r'Version["\']?\s*:\s*["\']?2\.0\.0', f'Version: {self.current_version}'),
                (r'v2\.0\.0', f'v{self.current_version}'),
                (r'2\.0\.0', self.current_version),
                (r'version["\']?\s*:\s*["\']?1\.0\.0', f'version: {self.current_version}'),
                (r'Version["\']?\s*:\s*["\']?1\.0\.0', f'Version: {self.current_version}'),
                (r'v1\.0\.0', f'v{self.current_version}'),
                (r'1\.0\.0', self.current_version),
            ]
            
            for pattern, replacement in version_fixes:
                new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                if new_content != content:
                    content = new_content
                    fixes += 1
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.fixes_applied.append(f"Fixed {fixes} version numbers in {file_path.name}")
                
        except Exception as e:
            print(f"Error fixing versions in {file_path}: {e}")
            
        return fixes
    
    def fix_dates(self, file_path: Path) -> int:
        """Fix date inconsistencies."""
        fixes = 0
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Common date patterns to fix
            date_fixes = [
                (r'October 1, 2025', self.current_date),
                (r'2025-10-01', '2025-10-05'),
                (r'10/1/2025', '10/5/2025'),
            ]
            
            for pattern, replacement in date_fixes:
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    fixes += 1
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.fixes_applied.append(f"Fixed {fixes} dates in {file_path.name}")
                
        except Exception as e:
            print(f"Error fixing dates in {file_path}: {e}")
            
        return fixes
    
    def fix_commands(self, file_path: Path) -> int:
        """Fix Windows compatibility issues."""
        fixes = 0
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Command fixes for Windows compatibility
            command_fixes = [
                (r'python -m venv', 'py -m venv'),
                (r'python -m uvicorn', 'py -m uvicorn'),
                (r'python app\.py', 'py app.py'),
                (r'source venv/bin/activate', 'venv\\\\Scripts\\\\activate.bat'),
                (r'\.env\.example', '.env file creation instructions'),
            ]
            
            for pattern, replacement in command_fixes:
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    fixes += 1
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.fixes_applied.append(f"Fixed {fixes} commands in {file_path.name}")
                
        except Exception as e:
            print(f"Error fixing commands in {file_path}: {e}")
            
        return fixes
    
    def remove_deleted_references(self, file_path: Path) -> int:
        """Remove references to deleted files."""
        fixes = 0
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Files that have been deleted
            deleted_files = [
                'MAPPING_STRATEGY.md',
                'IMPLEMENTATION_ROADMAP.md', 
                'FRONTEND_UPDATE_GUIDE.md',
                'QUICK_START_GUIDE.md',
                'REPOSITORY_SPLIT_GUIDE.md'
            ]
            
            for deleted_file in deleted_files:
                # Remove lines that reference deleted files
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    if deleted_file not in line:
                        new_lines.append(line)
                    else:
                        fixes += 1
                
                content = '\n'.join(new_lines)
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.fixes_applied.append(f"Removed {fixes} deleted file references in {file_path.name}")
                
        except Exception as e:
            print(f"Error removing deleted references in {file_path}: {e}")
            
        return fixes
    
    def apply_all_fixes(self) -> Dict[str, int]:
        """Apply all fixes to all documentation files."""
        print("🔧 Applying Batch Fixes to Documentation...")
        
        doc_files = self.get_documentation_files()
        total_fixes = {
            'versions': 0,
            'dates': 0,
            'commands': 0,
            'deleted_refs': 0,
            'total_files': len(doc_files)
        }
        
        for file_path in doc_files:
            print(f"🔨 Fixing: {file_path.name}")
            
            total_fixes['versions'] += self.fix_version_numbers(file_path)
            total_fixes['dates'] += self.fix_dates(file_path)
            total_fixes['commands'] += self.fix_commands(file_path)
            total_fixes['deleted_refs'] += self.remove_deleted_references(file_path)
        
        return total_fixes
    
    def get_documentation_files(self) -> List[Path]:
        """Get all documentation files."""
        doc_extensions = ['.md', '.txt']
        doc_files = []
        
        for ext in doc_extensions:
            doc_files.extend(self.project_root.rglob(f"*{ext}"))
        
        # Filter out files in venv, .git, and other non-project directories
        filtered_files = []
        for file in doc_files:
            if not any(part in str(file) for part in ['venv', '.git', '__pycache__', 'node_modules']):
                filtered_files.append(file)
        
        return filtered_files
    
    def generate_fix_report(self, total_fixes: Dict[str, int]) -> str:
        """Generate a report of all fixes applied."""
        report = f"""
# 🔧 Documentation Batch Fix Report
**Generated**: {self.current_date}
**Project**: SavorMe Backend

## 📊 Fix Summary
- **Total Files Processed**: {total_fixes['total_files']}
- **Version Fixes Applied**: {total_fixes['versions']}
- **Date Fixes Applied**: {total_fixes['dates']}
- **Command Fixes Applied**: {total_fixes['commands']}
- **Deleted Reference Removals**: {total_fixes['deleted_refs']}
- **Total Fixes**: {sum(total_fixes.values()) - total_fixes['total_files']}

## 🔨 Fixes Applied
"""
        
        for fix in self.fixes_applied:
            report += f"- {fix}\n"
        
        report += f"""
## ✅ Next Steps
1. Run the documentation review script again to verify fixes
2. Test all updated commands to ensure they work
3. Commit all changes to version control
4. Update any remaining manual references

## 🎯 Quality Check
Run this command to verify all fixes:
```bash
py docs_review_automation.py
```

Expected result: Health Score ≥ 90/100
"""
        
        return report

def main():
    """Main execution function."""
    print("🚀 SavorMe Documentation Batch Fix Tool")
    print("=" * 50)
    
    fixer = DocumentationFixer()
    total_fixes = fixer.apply_all_fixes()
    
    # Generate and save report
    report = fixer.generate_fix_report(total_fixes)
    
    # Save report to file
    report_file = Path("documentation_fix_report.md")
    report_file.write_text(report, encoding='utf-8')
    
    print(f"\n✅ Batch Fix Complete!")
    print(f"📊 Total Fixes Applied: {sum(total_fixes.values()) - total_fixes['total_files']}")
    print(f"📄 Fix Report saved to: {report_file}")
    
    if sum(total_fixes.values()) - total_fixes['total_files'] > 0:
        print(f"\n🎉 Successfully fixed documentation issues!")
        print("📋 Run the review script again to verify improvements")
    else:
        print("\n✨ No fixes were needed - documentation is already in good condition!")

if __name__ == "__main__":
    main()
