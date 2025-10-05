#!/usr/bin/env python3
"""
SavorMe Documentation Review Automation
Professional AI Consultant - Documentation Quality Assurance

This script automates the documentation review process to ensure:
- Version consistency across all files
- Current date references
- No broken links or outdated references
- Windows-compatible commands
- Complete coverage of all documentation files
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

class DocumentationReviewer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.issues = []
        self.fixes_applied = []
        self.current_version = "2.1.0"
        self.current_date = datetime.now().strftime("%B %d, %Y")
        
    def scan_documentation_files(self) -> List[Path]:
        """Find all documentation files in the project."""
        doc_extensions = ['.md', '.txt', '.rst']
        doc_files = []
        
        for ext in doc_extensions:
            doc_files.extend(self.project_root.rglob(f"*{ext}"))
        
        # Filter out files in venv, .git, and other non-project directories
        filtered_files = []
        for file in doc_files:
            if not any(part in str(file) for part in ['venv', '.git', '__pycache__', 'node_modules']):
                filtered_files.append(file)
        
        return filtered_files
    
    def check_version_consistency(self, file_path: Path) -> List[str]:
        """Check if version numbers are consistent across files."""
        issues = []
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Look for version patterns
            version_patterns = [
                r'version["\']?\s*:\s*["\']?(\d+\.\d+\.\d+)',
                r'Version["\']?\s*:\s*["\']?(\d+\.\d+\.\d+)',
                r'v(\d+\.\d+\.\d+)',
                r'(\d+\.\d+\.\d+)'
            ]
            
            for pattern in version_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if match != self.current_version:
                        issues.append(f"Version mismatch: found {match}, expected {self.current_version}")
                        
        except Exception as e:
            issues.append(f"Error reading file: {e}")
            
        return issues
    
    def check_date_consistency(self, file_path: Path) -> List[str]:
        """Check if dates are current."""
        issues = []
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Look for date patterns
            date_patterns = [
                r'(\w+ \d{1,2}, \d{4})',  # October 1, 2025
                r'(\d{4}-\d{2}-\d{2})',   # 2025-10-01
                r'(\d{1,2}/\d{1,2}/\d{4})' # 10/1/2025
            ]
            
            current_year = datetime.now().year
            for pattern in date_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if str(current_year) not in match:
                        issues.append(f"Outdated date found: {match}")
                        
        except Exception as e:
            issues.append(f"Error reading file: {e}")
            
        return issues
    
    def check_command_compatibility(self, file_path: Path) -> List[str]:
        """Check if commands are Windows-compatible."""
        issues = []
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check for non-Windows commands
            problematic_patterns = [
                (r'python -m venv', 'Use "py -m venv" for Windows compatibility'),
                (r'python -m uvicorn', 'Use "py -m uvicorn" for Windows compatibility'),
                (r'python app\.py', 'Use "py app.py" for Windows compatibility'),
                (r'source venv/bin/activate', 'Use "venv\\Scripts\\activate.bat" for Windows'),
                (r'\.env\.example', 'File does not exist, use direct .env creation instructions')
            ]
            
            for pattern, message in problematic_patterns:
                if re.search(pattern, content):
                    issues.append(message)
                    
        except Exception as e:
            issues.append(f"Error reading file: {e}")
            
        return issues
    
    def check_broken_references(self, file_path: Path) -> List[str]:
        """Check for references to deleted or non-existent files."""
        issues = []
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Files that have been deleted
            deleted_files = [
                'MAPPING_STRATEGY.md',
                'IMPLEMENTATION_ROADMAP.md', 
                'FRONTEND_UPDATE_GUIDE.md',
                'QUICK_START_GUIDE.md',
                'REPOSITORY_SPLIT_GUIDE.md'
            ]
            
            for deleted_file in deleted_files:
                if deleted_file in content:
                    issues.append(f"Reference to deleted file: {deleted_file}")
                    
        except Exception as e:
            issues.append(f"Error reading file: {e}")
            
        return issues
    
    def generate_fix_suggestions(self, file_path: Path, issues: List[str]) -> List[str]:
        """Generate specific fix suggestions for identified issues."""
        suggestions = []
        
        for issue in issues:
            if "Version mismatch" in issue:
                suggestions.append(f"Update version to {self.current_version}")
            elif "Outdated date" in issue:
                suggestions.append(f"Update date to {self.current_date}")
            elif "Windows compatibility" in issue:
                suggestions.append("Replace with Windows-compatible command")
            elif "deleted file" in issue:
                suggestions.append("Remove reference to deleted file")
                
        return suggestions
    
    def run_comprehensive_review(self) -> Dict[str, Any]:
        """Run the complete documentation review process."""
        print("🔍 Starting Comprehensive Documentation Review...")
        
        doc_files = self.scan_documentation_files()
        review_results = {
            'total_files': len(doc_files),
            'files_with_issues': 0,
            'total_issues': 0,
            'file_details': {},
            'summary': {}
        }
        
        for file_path in doc_files:
            print(f"📄 Reviewing: {file_path.name}")
            
            file_issues = []
            file_issues.extend(self.check_version_consistency(file_path))
            file_issues.extend(self.check_date_consistency(file_path))
            file_issues.extend(self.check_command_compatibility(file_path))
            file_issues.extend(self.check_broken_references(file_path))
            
            if file_issues:
                review_results['files_with_issues'] += 1
                review_results['total_issues'] += len(file_issues)
                
                suggestions = self.generate_fix_suggestions(file_path, file_issues)
                
                review_results['file_details'][str(file_path)] = {
                    'issues': file_issues,
                    'suggestions': suggestions,
                    'priority': 'HIGH' if len(file_issues) > 3 else 'MEDIUM' if len(file_issues) > 1 else 'LOW'
                }
        
        # Generate summary
        review_results['summary'] = {
            'health_score': max(0, 100 - (review_results['total_issues'] * 5)),
            'critical_files': [f for f, details in review_results['file_details'].items() 
                             if details['priority'] == 'HIGH'],
            'recommendations': self.generate_recommendations(review_results)
        }
        
        return review_results
    
    def generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on review results."""
        recommendations = []
        
        if results['total_issues'] > 10:
            recommendations.append("🚨 CRITICAL: High number of issues found. Prioritize fixing version and date inconsistencies.")
        
        if results['files_with_issues'] > results['total_files'] * 0.5:
            recommendations.append("⚠️ WARNING: More than 50% of files have issues. Consider systematic updates.")
        
        if any('Windows compatibility' in str(issues) for issues in results['file_details'].values()):
            recommendations.append("💻 ACTION: Update all commands to be Windows-compatible.")
        
        if any('deleted file' in str(issues) for issues in results['file_details'].values()):
            recommendations.append("🗑️ CLEANUP: Remove all references to deleted files.")
        
        recommendations.append("✅ BEST PRACTICE: Implement automated checks in CI/CD pipeline.")
        recommendations.append("📚 DOCUMENTATION: Create documentation standards and templates.")
        
        return recommendations
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive review report."""
        report = f"""
# 📋 Documentation Review Report
**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Project**: SavorMe Backend
**Reviewer**: AI Documentation Consultant

## 📊 Summary Statistics
- **Total Files Reviewed**: {results['total_files']}
- **Files with Issues**: {results['files_with_issues']}
- **Total Issues Found**: {results['total_issues']}
- **Health Score**: {results['summary']['health_score']}/100

## 🎯 Priority Actions
"""
        
        for priority in ['HIGH', 'MEDIUM', 'LOW']:
            priority_files = [f for f, details in results['file_details'].items() 
                            if details['priority'] == priority]
            if priority_files:
                report += f"\n### {priority} Priority Files:\n"
                for file_path in priority_files:
                    report += f"- `{Path(file_path).name}`\n"
        
        report += "\n## 🔧 Detailed Issues\n"
        for file_path, details in results['file_details'].items():
            report += f"\n### `{Path(file_path).name}`\n"
            for issue in details['issues']:
                report += f"- ❌ {issue}\n"
            for suggestion in details['suggestions']:
                report += f"- 💡 {suggestion}\n"
        
        report += "\n## 📈 Recommendations\n"
        for rec in results['summary']['recommendations']:
            report += f"- {rec}\n"
        
        return report

def main():
    """Main execution function."""
    print("🚀 SavorMe Documentation Review Automation")
    print("=" * 50)
    
    reviewer = DocumentationReviewer()
    results = reviewer.run_comprehensive_review()
    
    # Generate and save report
    report = reviewer.generate_report(results)
    
    # Save report to file
    report_file = Path("documentation_review_report.md")
    report_file.write_text(report, encoding='utf-8')
    
    print(f"\n✅ Review Complete!")
    print(f"📊 Health Score: {results['summary']['health_score']}/100")
    print(f"📄 Report saved to: {report_file}")
    print(f"🔍 Total Issues: {results['total_issues']}")
    
    if results['total_issues'] > 0:
        print(f"\n⚠️ Action Required: {results['files_with_issues']} files need attention")
        print("📋 See detailed report for specific fixes needed")
    else:
        print("\n🎉 All documentation files are in excellent condition!")

if __name__ == "__main__":
    main()
