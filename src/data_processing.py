import pandas as pd
import json
from datetime import datetime

def load_issues_data(file_path):
    """Load and process issues from JSON file"""
    with open(file_path, 'r') as f:
        issues_data = json.load(f)

    # Convert to DataFrame and process dates
    issues_df = pd.DataFrame(issues_data)
    issues_df['created_at'] = pd.to_datetime(issues_df['created_at'])

    # Handle closed_at - some issues may not have this field
    if 'closed_at' in issues_df.columns:
        issues_df['closed_at'] = pd.to_datetime(issues_df['closed_at'])
    else:
        issues_df['closed_at'] = pd.NaT

    issues_df['date'] = issues_df['created_at'].dt.date
    
    # Add date columns for easier comparison
    issues_df['created_date'] = issues_df['created_at'].dt.date
    issues_df['closed_date'] = issues_df['closed_at'].dt.date
    
    return issues_df

def create_summary_stats(df):
    """Create summary statistics"""
    total_issues = len(df)
    open_issues = len(df[df['state'] == 'open'])
    closed_issues = len(df[df['state'] == 'closed'])
    
    return {
        'total': total_issues,
        'open': open_issues, 
        'closed': closed_issues
    }

def extract_priority(labels):
    """Extract priority from issue labels"""
    if not labels:
        return 'No Priority'
    
    priority_labels = [label for label in labels if 
                      'priority' in label.lower() or 
                      'high' in label.lower() or 
                      'medium' in label.lower() or 
                      'low' in label.lower()]
    
    return priority_labels[0] if priority_labels else 'No Priority'

def group_issues_by_priority(issues_list):
    """
    Group a list of issues by priority and return organized structure.
    Returns dict with priority groups containing issue lists.
    """
    def extract_priority(issue):
        labels = issue.get('labels', [])
        if isinstance(labels, str):
            labels = [labels] if labels else []
        
        priority_labels = [label for label in labels if any(p in label.lower() 
                          for p in ['priority', 'high', 'medium', 'low', 'critical'])]
        
        if not priority_labels:
            return 'No Priority'
        return priority_labels[0]
    
    def get_priority_order(priority):
        priority_str = priority.lower()
        if 'high' in priority_str or 'critical' in priority_str:
            return 0
        elif 'medium' in priority_str:
            return 1
        elif 'low' in priority_str:
            return 2
        else:
            return 3
    
    # Group issues by priority
    groups = {}
    for issue in issues_list:
        priority = extract_priority(issue)
        if priority not in groups:
            groups[priority] = []
        groups[priority].append(issue)
    
    # Sort within each priority group by title
    for priority in groups:
        groups[priority].sort(key=lambda x: x.get('title', ''))
    
    # Sort groups by priority order
    sorted_groups = {}
    for priority in sorted(groups.keys(), key=get_priority_order):
        sorted_groups[priority] = groups[priority]
    
    return sorted_groups
