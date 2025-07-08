def generate_summary_html(stats):
    """Generate HTML for summary statistics display"""
    return f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0;">
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <h3 style="margin: 0; color: #4ECDC4;">{stats['total']}</h3>
            <p style="margin: 5px 0 0 0;">Total Issues</p>
        </div>
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <h3 style="margin: 0; color: #4285F4;">{stats['open']}</h3>
            <p style="margin: 5px 0 0 0;">Open Issues</p>
        </div>
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <h3 style="margin: 0; color: #FF8C00;">{stats['closed']}</h3>
            <p style="margin: 5px 0 0 0;">Closed Issues</p>
        </div>
    </div>
    """
