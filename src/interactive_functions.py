def add_click_functionality():
    """
    Add simple JavaScript click handling that reads pre-computed custom data.
    Returns HTML with embedded JavaScript for click handling.
    """
    
    html_content = """
    <script>
    // === MODAL FUNCTION ===
    function createModal(data) {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: rgba(0,0,0,0.5); display: flex; justify-content: center; 
            align-items: center; z-index: 10000;
        `;
        
        // Create HTML for grouped issues
        let issuesHTML = '';
        
        // Define priority colors
        const priorityColors = {
            'High Priority': '#FF4444',
            'Critical Priority': '#FF4444', 
            'Medium Priority': '#FF8C00',
            'Low Priority': '#4285F4',
            'No Priority': '#888888'
        };
        
        // Get color for priority (with fallback)
        function getPriorityColor(priority) {
            for (const [key, color] of Object.entries(priorityColors)) {
                if (priority.toLowerCase().includes(key.toLowerCase().split(' ')[0])) {
                    return color;
                }
            }
            return priorityColors['No Priority'];
        }
        
        // Build HTML for each priority group
        Object.keys(data.groups).forEach(priority => {
            const color = getPriorityColor(priority);
            const issueList = data.groups[priority];
            
            if (issueList.length > 0) {
                issuesHTML += `
                    <div style="margin-bottom: 20px;">
                        <h4 style="color: ${color}; margin-bottom: 10px; border-bottom: 2px solid ${color}; padding-bottom: 5px;">
                            ${priority} (${issueList.length} issues)
                        </h4>
                        <ul style="list-style: none; padding-left: 10px;">
                            ${issueList.map(issue => `
                                <li style="margin-bottom: 8px; padding: 8px; background: rgba(${color.slice(1).match(/.{2}/g).map(x => parseInt(x, 16)).join(', ')}, 0.1); border-radius: 4px; border-left: 4px solid ${color};">
                                    <span style="color: ${color}; font-weight: bold;">●</span> ${issue.title}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                `;
            }
        });
        
        if (!issuesHTML) {
            issuesHTML = '<p style="text-align: center; color: #666;">No issues found for this selection.</p>';
        }
        
        modal.innerHTML = `
            <div style="background: white; border-radius: 8px; padding: 20px; max-width: 80%; max-height: 80%; overflow-y: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">
                    <h3 style="margin: 0;">${data.title}</h3>
                    <button onclick="this.closest('div').parentElement.parentElement.remove()" style="background: #ff4444; color: white; border: none; border-radius: 4px; padding: 8px 12px; cursor: pointer;">Close</button>
                </div>
                <div style="font-size: 12px; color: #666; margin-bottom: 15px;">Issues are ordered by priority: High → Medium → Low → No Priority</div>
                ${issuesHTML}
            </div>
        `;
        
        document.body.appendChild(modal);
        modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
    }
    
    // === UNIFIED CLICK HANDLER ===
    function handleClick(eventData) {
        if (eventData.points.length === 0) return;
        
        const point = eventData.points[0];
        const customData = point.customdata;
        
        if (!customData) {
            console.log('No custom data found for this point');
            return;
        }
        
        try {
            const data = JSON.parse(customData);
            createModal(data);
        } catch (error) {
            console.error('Error parsing custom data:', error);
        }
    }
    
    // === ADD CLICK HANDLERS TO ALL PLOTLY CHARTS ===
    function addClickHandlers() {
        const plotlyDivs = document.querySelectorAll('.plotly-graph-div');
        
        plotlyDivs.forEach(div => {
            // Remove existing handlers to prevent duplicates
            if (div.removeAllListeners) {
                div.removeAllListeners('plotly_click');
            }
            
            // Add click handler
            div.on('plotly_click', handleClick);
        });
        
        console.log(`Added click handlers to ${plotlyDivs.length} charts`);
    }
    
    // === INITIALIZATION ===
    function initializeClickHandlers() {
        addClickHandlers();
        
        // Set up observer to catch dynamically added plots
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && (node.classList.contains('plotly-graph-div') || node.querySelector('.plotly-graph-div'))) {
                        setTimeout(addClickHandlers, 100);
                    }
                });
            });
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeClickHandlers);
    } else {
        setTimeout(initializeClickHandlers, 500);
    }
    
    // Also try multiple times to catch plots that render later
    setTimeout(initializeClickHandlers, 1000);
    setTimeout(initializeClickHandlers, 2000);
    
    console.log('Click functionality loaded');
    </script>
    """
    
    return html_content


def add_coordinated_toggle_functionality():
    """
    Add JavaScript to create custom toggle switches for the unified pie chart
    with dynamic legend positioning.
    """
    
    html_content = """
    <style>
    .pie-chart-controls {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 60px;
        margin: 20px 0 20px 0;
        padding: 20px;
        transform: translateX(-60px);  # Shift left to align with pie chart visual center
    }
    
    .toggle-group {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
    }
    
    .toggle-label {
        font-weight: bold;
        font-size: 16px;
        color: #333;
        margin-bottom: 8px;
    }
    
    .toggle-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .toggle-text {
        font-size: 14px;
        color: #666;
        min-width: 70px;
        text-align: center;
    }
    
    .toggle-text.active {
        color: #333;
        font-weight: 600;
    }
    
    /* Toggle Switch Styles */
    .toggle-switch {
        position: relative;
        width: 60px;
        height: 30px;
        background: #ddd;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .toggle-switch.active {
        background: #4285f4;
    }
    
    .toggle-knob {
        position: absolute;
        top: 3px;
        left: 3px;
        width: 24px;
        height: 24px;
        background: white;
        border-radius: 50%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .toggle-switch.active .toggle-knob {
        transform: translateX(30px);
    }
    
    /* Scope toggle colors */
    .scope-toggle.active {
        background: #4285f4;
    }
    
    /* Grouping toggle colors */
    .grouping-toggle.active {
        background: #ff8c00;
    }
    </style>
    
    <script>
    // === CUSTOM TOGGLE CREATION ===
    function createCustomToggles() {
        // Find the unified pie chart
        const plotlyDivs = document.querySelectorAll('.plotly-graph-div');
        let unifiedChart = null;
        
        for (const div of plotlyDivs) {
            // Check if this chart has our pie traces
            if (div.data && div.data.length >= 4 && div.data[0].type === 'pie') {
                unifiedChart = div;
                break;
            }
        }
        
        if (!unifiedChart) {
            console.log('Unified pie chart not found, will retry...');
            return false;
        }
        
        // Check if toggles already exist
        if (document.querySelector('.pie-chart-controls')) {
            console.log('Toggles already exist');
            return true;
        }
        
        // Create the controls container
        const controlsHTML = `
            <div class="pie-chart-controls">
                <div class="toggle-group">
                    <div class="toggle-label" style="color: #4285f4;">Scope</div>
                    <div class="toggle-container">
                        <span class="toggle-text active scope-left">Open</span>
                        <div class="toggle-switch scope-toggle" data-toggle="scope">
                            <div class="toggle-knob"></div>
                        </div>
                        <span class="toggle-text scope-right">All</span>
                    </div>
                </div>
                
                <div class="toggle-group">
                    <div class="toggle-label" style="color: #ff8c00;">Group by</div>
                    <div class="toggle-container">
                        <span class="toggle-text active grouping-left">Priority</span>
                        <div class="toggle-switch grouping-toggle" data-toggle="grouping">
                            <div class="toggle-knob"></div>
                        </div>
                        <span class="toggle-text grouping-right">Labels</span>
                    </div>
                </div>
            </div>
        `;
        
        // Insert controls above the chart
        const controlsDiv = document.createElement('div');
        controlsDiv.innerHTML = controlsHTML;
        unifiedChart.parentNode.insertBefore(controlsDiv, unifiedChart);
        
        // Set up toggle functionality
        setupToggleHandlers(unifiedChart);
        
        console.log('Custom toggles created successfully');
        return true;
    }
    
    // === TOGGLE HANDLERS WITH DYNAMIC LEGEND ===
    function setupToggleHandlers(unifiedChart) {
        // Track current state
        let currentScope = 'open';  // 'open' or 'all'
        let currentGrouping = 'priority';  // 'priority' or 'labels'
        
        // Define legend configurations for each state
        const legendConfigs = {
            'open-priority': { orientation: "v", x: 0.85, y: 0.5, xanchor: 'left', yanchor: 'middle' },
            'all-priority': { orientation: "v", x: 0.85, y: 0.5, xanchor: 'left', yanchor: 'middle' },
            'open-labels': { orientation: "v", x: 0.85, y: 0.5, xanchor: 'left', yanchor: 'middle' },
            'all-labels': { orientation: "v", x: 1.02, y: 0.5, xanchor: 'left', yanchor: 'middle' } // Special positioning for this problematic case
        };
        
        // Function to update chart based on current state
        function updateChart() {
            const traceIndex = getTraceIndex(currentScope, currentGrouping);
            const visibility = [false, false, false, false];
            visibility[traceIndex] = true;
            
            const title = `${currentScope === 'open' ? 'Open' : 'All'} Issues by ${currentGrouping === 'priority' ? 'Priority' : 'Labels'}`;
            const legendKey = `${currentScope}-${currentGrouping}`;
            const legendConfig = legendConfigs[legendKey];
            
            // Update both trace visibility and legend positioning
            Plotly.update(unifiedChart, 
                { visible: visibility },
                { 
                    title: title,
                    legend: legendConfig,
                    // Adjust right margin based on legend position
                    'margin.r': legendConfig.x > 1 ? 150 : 120
                }
            );
            
            console.log(`Updated chart to: ${title} with legend config:`, legendConfig);
        }
        
        function getTraceIndex(scope, grouping) {
            if (scope === 'open' && grouping === 'priority') return 0;
            if (scope === 'all' && grouping === 'priority') return 1;
            if (scope === 'open' && grouping === 'labels') return 2;
            if (scope === 'all' && grouping === 'labels') return 3;
            return 0;
        }
        
        function updateToggleUI(toggleType, isActive) {
            const toggle = document.querySelector(`.${toggleType}-toggle`);
            const leftText = document.querySelector(`.${toggleType}-left`);
            const rightText = document.querySelector(`.${toggleType}-right`);
            
            if (toggle && leftText && rightText) {
                if (isActive) {
                    toggle.classList.add('active');
                    leftText.classList.remove('active');
                    rightText.classList.add('active');
                } else {
                    toggle.classList.remove('active');
                    leftText.classList.add('active');
                    rightText.classList.remove('active');
                }
            }
        }
        
        // Add click handlers to toggles
        const scopeToggle = document.querySelector('.scope-toggle');
        const groupingToggle = document.querySelector('.grouping-toggle');
        
        if (scopeToggle) {
            scopeToggle.addEventListener('click', function() {
                currentScope = currentScope === 'open' ? 'all' : 'open';
                updateToggleUI('scope', currentScope === 'all');
                updateChart();
            });
        }
        
        if (groupingToggle) {
            groupingToggle.addEventListener('click', function() {
                currentGrouping = currentGrouping === 'priority' ? 'labels' : 'priority';
                updateToggleUI('grouping', currentGrouping === 'labels');
                updateChart();
            });
        }
        
        console.log('Toggle handlers with dynamic legend set up successfully');
    }
    
    // === INITIALIZATION ===
    function initCustomToggles() {
        if (createCustomToggles()) {
            return;
        }
        
        // Retry logic
        let retryCount = 0;
        const maxRetries = 10;
        
        const retryInterval = setInterval(() => {
            retryCount++;
            if (createCustomToggles() || retryCount >= maxRetries) {
                clearInterval(retryInterval);
            }
        }, 500);
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCustomToggles);
    } else {
        setTimeout(initCustomToggles, 100);
    }
    
    // Also set up observer for dynamic content
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1 && 
                    (node.classList.contains('plotly-graph-div') || node.querySelector('.plotly-graph-div'))) {
                    setTimeout(initCustomToggles, 100);
                }
            });
        });
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
    
    console.log('Custom toggle functionality with dynamic legend loaded');
    </script>
    """
    
    return html_content
