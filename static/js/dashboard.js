document.addEventListener('DOMContentLoaded', function() {
    console.log('Summary charts data:', summaryCharts);
    
    if (summaryCharts) {
        try {
            const summaryDiv = document.getElementById('summary');
            for (let chartId in summaryCharts) {
                const chartDiv = document.createElement('div');
                chartDiv.id = chartId;
                chartDiv.className = 'chart';
                summaryDiv.appendChild(chartDiv);
                Plotly.newPlot(chartId, JSON.parse(summaryCharts[chartId]), {
                    responsive: true,
                    autosize: true
                });
            }
        } catch (error) {
            console.error('Error parsing or creating summary plots:', error);
        }
    } else {
        console.error('No summary charts data available');
    }

    // Add custom plot functionality
    document.getElementById('plotButton').addEventListener('click', createCustomPlot);

    // Add search functionality
    document.getElementById('searchButton').addEventListener('click', performSearch);

    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        updateChartsTheme();
    });
});

function createCustomPlot() {
    const xAxis = document.getElementById('xAxis').value;
    const yAxis = document.getElementById('yAxis').value;
    
    if (xAxis && yAxis) {
        showLoading();
        fetch('/plot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ x_axis: xAxis, y_axis: yAxis, filename: filename }),
        })
        .then(response => response.json())
        .then(data => {
            Plotly.newPlot('customPlotChart', JSON.parse(data), {
                responsive: true,
                autosize: true
            });
            hideLoading();
        });
    } else {
        alert('Please select both X and Y axes for the custom plot.');
    }
}

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function performSearch() {
    const searchTerm = document.getElementById('searchInput').value;
    
    if (searchTerm) {
        showLoading();
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ search_term: searchTerm, filename: filename }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Search request failed');
            }
            return response.json();
        })
        .then(data => {
            const resultsDiv = document.getElementById('searchResults');
            if (data.count > 0) {
                resultsDiv.innerHTML = `Found ${data.count} results for "${searchTerm}"`;
                Plotly.newPlot('searchPlot', JSON.parse(data.plot), {
                    responsive: true,
                    autosize: true
                });
            } else {
                resultsDiv.innerHTML = `No results found for "${searchTerm}"`;
                document.getElementById('searchPlot').innerHTML = '';
            }
            hideLoading();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while searching. Please try again.');
            hideLoading();
        });
    } else {
        alert('Please enter a search term.');
    }
}

function updateChartsTheme() {
    const isDarkMode = document.body.classList.contains('dark-mode');
    const updateOptions = {
        'paper_bgcolor': isDarkMode ? '#333' : '#fff',
        'plot_bgcolor': isDarkMode ? '#333' : '#fff',
        'font': { 'color': isDarkMode ? '#fff' : '#333' }
    };

    document.querySelectorAll('.chart').forEach(chart => {
        Plotly.relayout(chart.id, updateOptions);
    });
}
