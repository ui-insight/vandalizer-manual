import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date, timedelta, datetime
import json
from data_processing import group_issues_by_priority

def create_cumulative_issues_plot(issues_df):
    """Create cumulative issues plot with matching hover templates"""
    current_date = date.today()
    
    # === TRACE 1: Cumulative Issues Opened ===
    opened_data = issues_df.groupby('date').size().reset_index(name='count')
    opened_data = opened_data.sort_values('date')
    opened_data['cumulative'] = opened_data['count'].cumsum()

    # Extend to current date if needed
    last_opened_date = opened_data['date'].max()
    if pd.to_datetime(last_opened_date).date() < current_date:
        current_row = pd.DataFrame({
            'date': [current_date],
            'count': [0], 
            'cumulative': [opened_data['cumulative'].iloc[-1]]
        })
        opened_data = pd.concat([opened_data, current_row], ignore_index=True)

    # === TRACE 2: Cumulative Issues Closed ===
    closed_issues = issues_df[issues_df['state'] == 'closed'].copy()
        
    if not closed_issues.empty:
        closed_issues['effective_close_date'] = closed_issues['closed_date'].fillna(closed_issues['created_date'])
        closed_data = closed_issues.groupby('effective_close_date').size().reset_index(name='count')
        closed_data = closed_data.sort_values('effective_close_date')
        closed_data['cumulative'] = closed_data['count'].cumsum()
                
        last_closed_date = closed_data['effective_close_date'].max()
        if pd.to_datetime(last_closed_date).date() < current_date:
            current_row = pd.DataFrame({
                'effective_close_date': [current_date],
                'count': [0], 
                'cumulative': [closed_data['cumulative'].iloc[-1]]
            })
            closed_data = pd.concat([closed_data, current_row], ignore_index=True)
            
        closed_data = closed_data.rename(columns={'effective_close_date': 'close_date'})
    else:
        closed_data = pd.DataFrame({
            'close_date': [current_date],
            'count': [0],
            'cumulative': [0]
        })

    # === PREPARE CUSTOM DATA ===
    # For opened trace - issues opened by each date
    opened_custom_data = []
    for _, row in opened_data.iterrows():
        date_filter = row['date']
        relevant_issues = issues_df[pd.to_datetime(issues_df['date']) <= pd.to_datetime(date_filter)].to_dict('records')
        grouped_issues = group_issues_by_priority(relevant_issues)
        
        custom_data = {
            'title': f'All issues opened by {date_filter} ({len(relevant_issues)} total)',
            'groups': grouped_issues
        }
        opened_custom_data.append(json.dumps(custom_data, default=str))
    
    # For closed trace - issues closed by each date
    closed_custom_data = []
    for _, row in closed_data.iterrows():
        date_filter = row['close_date']
        if not closed_issues.empty:
            relevant_issues = closed_issues[
                pd.to_datetime(closed_issues['effective_close_date']) <= pd.to_datetime(date_filter)
            ].to_dict('records')
        else:
            relevant_issues = []
        
        grouped_issues = group_issues_by_priority(relevant_issues)
        
        custom_data = {
            'title': f'All issues closed by {date_filter} ({len(relevant_issues)} total)',
            'groups': grouped_issues
        }
        closed_custom_data.append(json.dumps(custom_data, default=str))

    # === PREPARE HOVER TEXT ===
    # Create hover text matching the style used in open issues and weekly activity plots
    opened_hover_text = []
    for _, row in opened_data.iterrows():
        date_str = row['date']
        cumulative_count = int(row['cumulative'])
        opened_hover_text.append(
            f"<b>{date_str}</b><br>Cumulative opened: {cumulative_count}<br><br><i>Click to see all issues opened by this date</i>"
        )
    
    closed_hover_text = []
    for _, row in closed_data.iterrows():
        date_str = row['close_date']
        cumulative_count = int(row['cumulative'])
        closed_hover_text.append(
            f"<b>{date_str}</b><br>Cumulative closed: {cumulative_count}<br><br><i>Click to see all issues closed by this date</i>"
        )

    # === CREATE COMBINED CHART ===
    fig = go.Figure()

    # Add trace 1: Cumulative issues opened (matching hover template style)
    fig.add_trace(go.Scatter(
        x=opened_data['date'],
        y=opened_data['cumulative'],
        mode='lines+markers',
        name='Total Issues',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8),
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=opened_hover_text,
        customdata=opened_custom_data
    ))

    # Add trace 2: Cumulative issues closed (matching hover template style)
    fig.add_trace(go.Scatter(
        x=closed_data['close_date'],
        y=closed_data['cumulative'],
        mode='lines+markers',
        name='Closed Issues',
        line=dict(color='#FF8C00', width=3),
        marker=dict(size=8),
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=closed_hover_text,
        customdata=closed_custom_data
    ))

    # Update layout
    fig.update_layout(
        title="Issues Opened",
        xaxis_title="Date",
        yaxis_title="Cumulative Count",
        height=600,  # Increased from 500 to 600
        margin=dict(t=60, b=80, l=60, r=40),
        showlegend=True,
        legend=dict(x=0.05, y=0.95),
        legend_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=0.5),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=0.5)
    )
    
    return fig

def create_open_issues_plot(issues_df):

    events = []
    
    for _, issue in issues_df.iterrows():
        events.append({
            'date': pd.to_datetime(issue['created_date']).date(),
            'type': 'opened',
            'issue_data': issue.to_dict()
        })
    
    closed_issues = issues_df[issues_df['state'] == 'closed']
    for _, issue in closed_issues.iterrows():
        close_date = issue['closed_date'] if pd.notna(issue['closed_date']) else issue['created_date']
        events.append({
            'date': pd.to_datetime(close_date).date(),
            'type': 'closed',
            'issue_data': issue.to_dict()
        })
    
    events_df = pd.DataFrame(events)
    events_df = events_df.sort_values('date')
    
    # === GROUP EVENTS BY DATE ===
    events_by_date = events_df.groupby(['date', 'type']).size().reset_index(name='count')
    events_by_date = events_by_date.pivot(index='date', columns='type', values='count').fillna(0)
    
    if 'opened' not in events_by_date.columns:
        events_by_date['opened'] = 0
    if 'closed' not in events_by_date.columns:
        events_by_date['closed'] = 0
    
    events_by_date = events_by_date.sort_index()
    events_by_date['net_change'] = events_by_date['opened'] - events_by_date['closed']
    events_by_date['open_issues'] = events_by_date['net_change'].cumsum()
    
    significant_dates = events_by_date[events_by_date['net_change'] != 0].copy()
    
    current_date = datetime.now().date()
    if len(significant_dates) > 0:
        last_date = significant_dates.index.max()
        if last_date < current_date:
            current_row = pd.DataFrame({
                'opened': [0], 'closed': [0], 'net_change': [0],
                'open_issues': [significant_dates['open_issues'].iloc[-1]]
            }, index=[current_date])
            significant_dates = pd.concat([significant_dates, current_row])

    # === PREPARE CUSTOM DATA ===
    custom_data = []
    
    for date, row in significant_dates.iterrows():
        # Get issues that should be open on this specific date
        open_issues_list = []
        
        for _, issue in issues_df.iterrows():
            created_date = pd.to_datetime(issue['created_date']).date()
            
            # Issue must be created on or before this date
            if created_date <= date:
                if issue['state'] == 'open':
                    # Open issues are included if created by this date
                    open_issues_list.append(issue.to_dict())
                elif issue['state'] == 'closed' and pd.notna(issue['closed_date']):
                    closed_date = pd.to_datetime(issue['closed_date']).date()
                    # Closed issues are included only if they closed AFTER this date
                    if closed_date > date:
                        open_issues_list.append(issue.to_dict())
        
        grouped_issues = group_issues_by_priority(open_issues_list)
        
        net_change = row['net_change']
        change_text = f"+{int(net_change)}" if net_change > 0 else f"{int(net_change)}" if net_change < 0 else "±0"
        
        custom_data_point = {
            'title': f'Open issues on {date} ({len(open_issues_list)} total)',
            'groups': grouped_issues
        }
        custom_data.append(json.dumps(custom_data_point, default=str))

    # === CREATE CHART ===
    fig = go.Figure()
    
    if len(significant_dates) > 0:
        # Create hover text matching JS format
        hover_text = []
        for date, row in significant_dates.iterrows():
            net_change = row['net_change']
            change_text = f"+{int(net_change)}" if net_change > 0 else f"{int(net_change)}" if net_change < 0 else "±0"
            hover_text.append(
                f"<b>{date}</b><br>Total open issues: {int(row['open_issues'])}<br>"
                f"Net change: {change_text}<br><br><i>Click to view open issues</i>"
            )
        
        fig.add_trace(go.Scatter(
            x=significant_dates.index,
            y=significant_dates['open_issues'],
            mode='lines+markers',
            name='Open Issues',
            line=dict(color='#4285F4', width=3, shape='hv'),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(66, 133, 244, 0.1)',
            hovertemplate='%{hovertext}<extra></extra>',
            hovertext=hover_text,
            customdata=custom_data
        ))
    
    fig.update_layout(
        title="Open Issues Trend (Click points for details)",
        xaxis_title="Date",
        yaxis_title="Total Open Issues",
        height=500,
        margin=dict(t=60, b=80, l=60, r=40),
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=0.5, type='date'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=0.5)
    )
    
    return fig

def create_weekly_activity_chart(issues_df):

    events = []
    
    for _, issue in issues_df.iterrows():
        events.append({
            'date': pd.to_datetime(issue['created_date']).date(),
            'type': 'opened',
            'issue_data': issue.to_dict()
        })
    
    closed_issues = issues_df[issues_df['state'] == 'closed']
    for _, issue in closed_issues.iterrows():
        close_date = issue['closed_date'] if pd.notna(issue['closed_date']) else issue['created_date']
        events.append({
            'date': pd.to_datetime(close_date).date(),
            'type': 'closed',
            'issue_data': issue.to_dict()
        })
    
    events_df = pd.DataFrame(events)
    
    def get_week_start(date):
        days_since_monday = date.weekday()
        monday = date - timedelta(days=days_since_monday)
        return monday
    
    events_df['week_start'] = events_df['date'].apply(get_week_start)
    weekly_data = events_df.groupby(['week_start', 'type']).size().reset_index(name='count')
    weekly_pivot = weekly_data.pivot(index='week_start', columns='type', values='count').fillna(0)
    
    if 'opened' not in weekly_pivot.columns:
        weekly_pivot['opened'] = 0
    if 'closed' not in weekly_pivot.columns:
        weekly_pivot['closed'] = 0

    # === PREPARE CUSTOM DATA ===
    opened_custom_data = []
    closed_custom_data = []
    
    for week_start, row in weekly_pivot.iterrows():
        # Convert week_start to a proper date object
        week_start_date: date = pd.to_datetime(str(week_start)).date()
        week_end: date = week_start_date + timedelta(days=6)
        week_events = events_df[events_df['week_start'] == week_start]
        
        # Opened issues for this week
        opened_issues = [event['issue_data'] for _, event in week_events.iterrows() 
                        if event['type'] == 'opened']
        grouped_opened = group_issues_by_priority(opened_issues)
        
        opened_custom_data.append(json.dumps({
            'title': f'Issues opened during week of {week_start} ({week_start} to {week_end.strftime("%Y-%m-%d")})',
            'groups': grouped_opened
        }, default=str))
        
        # Closed issues for this week
        closed_issues_week = [event['issue_data'] for _, event in week_events.iterrows() 
                             if event['type'] == 'closed']
        grouped_closed = group_issues_by_priority(closed_issues_week)
        
        closed_custom_data.append(json.dumps({
            'title': f'Issues closed during week of {week_start} ({week_start} to {week_end.strftime("%Y-%m-%d")})',
            'groups': grouped_closed
        }, default=str))

    # === CREATE CHART ===
    fig = go.Figure()
    
    if len(weekly_pivot) > 0:
        # Create hover text matching JS format
        opened_hover = []
        closed_hover = []
        
        for week_start, row in weekly_pivot.iterrows():
            # Convert week_start to a proper date object
            week_start_date: date = pd.to_datetime(str(week_start)).date()
            week_end: date = week_start_date + timedelta(days=6)

            opened_count = int(row['opened'])
            closed_count = int(row['closed'])
            
            opened_hover.append(
                f"<b>Week of {week_start_date}</b><br>({week_start_date} to {week_end})<br>"
                f"Issues opened: {opened_count}<br><br><i>Click for details</i>"
            )
            
            closed_hover.append(
                f"<b>Week of {week_start_date}</b><br>({week_start_date} to {week_end})<br>"
                f"Issues closed: {closed_count}<br><br><i>Click for details</i>"
            )
        
        if weekly_pivot['opened'].sum() > 0:
            fig.add_trace(go.Bar(
                x=weekly_pivot.index,
                y=weekly_pivot['opened'],
                name='Issues Opened',
                marker=dict(color='#4285F4', opacity=0.8),
                hovertemplate='%{hovertext}<extra></extra>',
                hovertext=opened_hover,
                customdata=opened_custom_data
            ))
        
        if weekly_pivot['closed'].sum() > 0:
            fig.add_trace(go.Bar(
                x=weekly_pivot.index,
                y=-weekly_pivot['closed'],
                name='Issues Closed',
                marker=dict(color='#FF8C00', opacity=0.8),
                hovertemplate='%{hovertext}<extra></extra>',
                hovertext=closed_hover,
                customdata=closed_custom_data
            ))
    
    fig.update_layout(
        title="Weekly Issue Activity",
        xaxis_title="Date",
        yaxis_title="Weekly Changes",
        height=400,
        margin=dict(t=80, b=80, l=60, r=40),
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        barmode='overlay',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=0.5, type='date'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=0.5, 
                  zeroline=True, zerolinecolor='rgba(0,0,0,0.4)', zerolinewidth=2)
    )
    
    return fig

def create_unified_pie_chart(issues_df):
    """
    Create a single pie chart with toggle functionality for:
    - Open vs All issues
    - Priority vs Labels grouping
    Uses Plotly's updatemenus for client-side switching between pre-computed data.
    """
    
    def extract_priority_from_issue(issue):
        """Extract priority from issue labels"""
        labels = issue.get('labels', [])
        if isinstance(labels, str):
            labels = [labels] if labels else []
        
        priority_labels = [
            label for label in labels 
            if any(p in label.lower() for p in ['priority', 'high', 'medium', 'low', 'critical'])
        ]
        return priority_labels[0] if priority_labels else 'No Priority'
    
    def extract_non_priority_labels(issue):
        """Extract non-priority labels from issue"""
        labels = issue.get('labels', [])
        if isinstance(labels, str):
            labels = [labels] if labels else []
        
        non_priority_labels = [
            label for label in labels 
            if not any(p in label.lower() for p in ['priority', 'high', 'medium', 'low', 'critical'])
        ]
        return non_priority_labels if non_priority_labels else ['No Label']
    
    def get_priority_order(priority):
        """Sort priorities in logical order"""
        priority_str = priority.lower()
        if 'high' in priority_str or 'critical' in priority_str:
            return 0
        elif 'medium' in priority_str:
            return 1
        elif 'low' in priority_str:
            return 2
        else:
            return 3
    
    def get_legend_config(labels_count, is_labels_grouping=False):
        """Get optimal legend configuration based on number of labels"""
        if is_labels_grouping and labels_count > 6:
            # For many labels, position legend to the right with more space
            return dict(
                orientation="v", 
                x=1.02, 
                y=0.5,
                xanchor='left',
                yanchor='middle'
            )
        elif labels_count > 8:
            # For very many items, position further right
            return dict(
                orientation="v", 
                x=1.05, 
                y=0.5,
                xanchor='left',
                yanchor='middle'
            )
        else:
            # Default positioning for fewer items
            return dict(
                orientation="v", 
                x=0.85, 
                y=0.5,
                xanchor='left',
                yanchor='middle'
            )
    
    def prepare_chart_data(filtered_issues, group_by='priority'):
        """Prepare data for a single chart state"""
        if len(filtered_issues) == 0:
            return [], [], [], [], [], {}
        
        grouped_data = {}
        
        for _, issue in filtered_issues.iterrows():
            issue_dict = issue.to_dict()
            
            if group_by == 'priority':
                groups = [extract_priority_from_issue(issue_dict)]
            else:  # group_by == 'labels'
                groups = extract_non_priority_labels(issue_dict)
            
            for group in groups:
                if group not in grouped_data:
                    grouped_data[group] = {'count': 0, 'issues': []}
                grouped_data[group]['count'] += 1
                grouped_data[group]['issues'].append(issue_dict)
        
        if not grouped_data:
            return [], [], [], [], [], {}
        
        # Sort groups appropriately
        if group_by == 'priority':
            sorted_groups = sorted(grouped_data.keys(), key=get_priority_order)
        else:
            # For labels, sort alphabetically but put 'No Label' last
            sorted_groups = sorted([g for g in grouped_data.keys() if g != 'No Label'])
            if 'No Label' in grouped_data:
                sorted_groups.append('No Label')
        
        labels = sorted_groups
        values = [grouped_data[group]['count'] for group in labels]
        
        # Prepare custom data and hover text
        custom_data = []
        hover_text = []
        
        for group in labels:
            issues_list = grouped_data[group]['issues']
            grouped_issues = group_issues_by_priority(issues_list)
            
            group_type = 'Priority' if group_by == 'priority' else 'Label'
            custom_data_point = {
                'title': f'{group_type}: {group}',
                'groups': grouped_issues
            }
            custom_data.append(json.dumps(custom_data_point, default=str))
            
            hover_text.append(
                f"<b>{group}</b><br>Issues: {len(issues_list)}<br><br><i>Click to see all issues</i>"
            )
        
        # Color palettes
        if group_by == 'priority':
            colors = ['#FFD580', '#BBDEFB', '#D7CCC8', '#F3E5F5', '#E0F2F1', 
                     '#F1F8E9', '#EDE7F6', '#E3F2FD', '#F9FBE7', '#FFF8E1']
        else:
            colors = ['#F5F7F7', '#B39DDB', '#A5D6A7', '#81C784', '#CE93D8', '#80CBC4',
                     '#BCAAA4', '#B0BEC5', '#F8BBD9', '#FFF176', '#9FA8DA', '#C8E6C9',
                     '#FFE082', '#B2DFDB', '#DCEDC8', '#E1BEE7']
        
        chart_colors = colors[:len(labels)]
        
        # Get appropriate legend config
        legend_config = get_legend_config(len(labels), group_by == 'labels')
        
        return labels, values, custom_data, hover_text, chart_colors, legend_config
    
    # Pre-compute all four chart states
    open_issues = issues_df[issues_df['state'] == 'open']
    all_issues = issues_df
    
    # State 1: Open issues by priority
    labels_op, values_op, custom_op, hover_op, colors_op, legend_op = prepare_chart_data(open_issues, 'priority')
    
    # State 2: All issues by priority  
    labels_ap, values_ap, custom_ap, hover_ap, colors_ap, legend_ap = prepare_chart_data(all_issues, 'priority')
    
    # State 3: Open issues by labels
    labels_ol, values_ol, custom_ol, hover_ol, colors_ol, legend_ol = prepare_chart_data(open_issues, 'labels')
    
    # State 4: All issues by labels (this is the problematic one!)
    labels_al, values_al, custom_al, hover_al, colors_al, legend_al = prepare_chart_data(all_issues, 'labels')
    
    # Create the figure with all traces (only first one visible initially)
    fig = go.Figure()
    
    # Add all four traces
    traces_data = [
        (labels_op, values_op, custom_op, hover_op, colors_op, "Open Issues by Priority"),
        (labels_ap, values_ap, custom_ap, hover_ap, colors_ap, "All Issues by Priority"),
        (labels_ol, values_ol, custom_ol, hover_ol, colors_ol, "Open Issues by Labels"),
        (labels_al, values_al, custom_al, hover_al, colors_al, "All Issues by Labels")
    ]
    
    for i, (labels, values, custom_data, hover_text, colors, name) in enumerate(traces_data):
        if labels and values:  # Only add trace if there's data
            fig.add_trace(go.Pie(
                labels=labels,
                values=values,
                name=name,
                marker=dict(colors=colors),
                hovertemplate='%{hovertext}<extra></extra>',
                hovertext=hover_text,
                customdata=custom_data,
                textinfo='label+percent',
                textposition='auto',
                visible=(i == 0)  # Only first trace visible initially
            ))
        else:
            # Add empty trace as placeholder
            fig.add_trace(go.Pie(
                labels=['No Data'],
                values=[1],
                name=name,
                marker=dict(colors=['#CCCCCC']),
                textinfo='text',
                text=['No Data Available'],
                visible=(i == 0),
                hoverinfo='skip'
            ))
    
    # Use the legend config from the first (default) trace
    default_legend = legend_op if labels_op else dict(orientation="v", x=0.85, y=0.5)
    
    # Layout with dynamic margins to accommodate legend
    fig.update_layout(
        height=600,
        margin=dict(t=20, b=20, l=20, r=120),  # Increased right margin for legend
        showlegend=True,
        legend=default_legend
    )
    
    return fig
