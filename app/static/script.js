// Text Analysis App JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analysisForm');
    const textarea = document.getElementById('textInput');
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    const submitBtn = document.getElementById('submitBtn');
    
    // Check if form exists
    if (!form) {
        console.error('Analysis form not found');
        return;
    }
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const text = textarea.value.trim();
        if (!text) {
            alert('Please enter some text to analyze');
            return;
        }
        
        // Show loading state
        showLoading();
        
        // Scroll to results area
        if (resultsDiv) {
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
        
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    include_keywords: document.getElementById('includeKeywords').checked,
                    include_sentiment: document.getElementById('includeSentiment').checked
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            showResults(data);
            
        } catch (error) {
            showError('Failed to analyze text: ' + error.message);
        } finally {
            hideLoading();
        }
    });
    
    function showLoading() {
        if (loadingDiv) loadingDiv.style.display = 'block';
        if (resultsDiv) resultsDiv.classList.remove('show');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Analyzing...';
        }
    }
    
    function hideLoading() {
        if (loadingDiv) loadingDiv.style.display = 'none';
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Analyze Text';
        }
    }
    
    function showResults(data) {
        const summaryDiv = document.getElementById('summary');
        const titleDiv = document.getElementById('title');
        const topicsDiv = document.getElementById('topics');
        const sentimentDiv = document.getElementById('sentiment');
        const keywordsDiv = document.getElementById('keywords');
        const processingTimeDiv = document.getElementById('processingTime');
        
        // Check if all elements exist
        if (!summaryDiv || !titleDiv || !topicsDiv || !sentimentDiv || !keywordsDiv || !processingTimeDiv) {
            console.error('One or more DOM elements not found');
            showError('Error: Page elements not found. Please refresh the page.');
            return;
        }
        
        // Update summary
        summaryDiv.textContent = data.summary || 'No summary available';
        
        // Update metadata
        titleDiv.textContent = data.metadata?.title || 'No title extracted';
        topicsDiv.textContent = data.metadata?.topics?.join(', ') || 'No topics found';
        
        // Update sentiment with color coding
        const sentiment = data.metadata?.sentiment || 'neutral';
        sentimentDiv.textContent = sentiment.charAt(0).toUpperCase() + sentiment.slice(1);
        sentimentDiv.className = `sentiment-${sentiment}`;
        
        // Update keywords
        keywordsDiv.textContent = data.metadata?.keywords?.join(', ') || 'No keywords found';
        
        // Update processing time
        processingTimeDiv.textContent = `Processed in ${(data.processing_time || 0).toFixed(2)} seconds`;
        
        // Show results
        resultsDiv.classList.add('show');
    }
    
    function showError(message) {
        if (!resultsDiv) {
            console.error('Results div not found');
            return;
        }
        resultsDiv.innerHTML = `
            <div class="error">
                <strong>Error:</strong> ${message}
            </div>
        `;
        resultsDiv.classList.add('show');
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Auto-resize textarea
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }

    // History functionality
    const loadHistoryBtn = document.getElementById('loadHistoryBtn');
    const historyContent = document.getElementById('historyContent');
    const searchFilter = document.getElementById('searchFilter');
    const sentimentFilter = document.getElementById('sentimentFilter');
    const keywordFilter = document.getElementById('keywordFilter');
    const applyFiltersBtn = document.getElementById('applyFiltersBtn');
    const clearFiltersBtn = document.getElementById('clearFiltersBtn');

    if (loadHistoryBtn && historyContent) {
        loadHistoryBtn.addEventListener('click', async function() {
            await loadHistory();
        });
    }

    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', async function() {
            await loadHistory();
        });
    }

    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            clearFilters();
        });
    }

    // Allow Enter key to apply filters
    if (searchFilter) {
        searchFilter.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                loadHistory();
            }
        });
    }

    if (keywordFilter) {
        keywordFilter.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                loadHistory();
            }
        });
    }

    async function loadHistory() {
        try {
            if (loadHistoryBtn) {
                loadHistoryBtn.disabled = true;
                loadHistoryBtn.textContent = 'Loading...';
            }
            if (applyFiltersBtn) {
                applyFiltersBtn.disabled = true;
                applyFiltersBtn.textContent = 'Loading...';
            }

            // Build query parameters
            const params = new URLSearchParams();
            if (searchFilter && searchFilter.value.trim()) {
                params.append('search', searchFilter.value.trim());
            }
            if (sentimentFilter && sentimentFilter.value) {
                params.append('sentiment', sentimentFilter.value);
            }
            if (keywordFilter && keywordFilter.value.trim()) {
                params.append('keyword', keywordFilter.value.trim());
            }

            const url = `/api/history${params.toString() ? '?' + params.toString() : ''}`;
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            displayHistory(data.analyses, data.filters);

        } catch (error) {
            if (historyContent) {
                historyContent.innerHTML = `
                    <div class="error">
                        <strong>Error:</strong> Failed to load history: ${error.message}
                    </div>
                `;
            }
        } finally {
            if (loadHistoryBtn) {
                loadHistoryBtn.disabled = false;
                loadHistoryBtn.textContent = 'Load History';
            }
            if (applyFiltersBtn) {
                applyFiltersBtn.disabled = false;
                applyFiltersBtn.textContent = 'Apply Filters';
            }
        }
    }

    function clearFilters() {
        if (searchFilter) searchFilter.value = '';
        if (sentimentFilter) sentimentFilter.value = '';
        if (keywordFilter) keywordFilter.value = '';
        loadHistory();
    }

    function displayHistory(analyses, filters = {}) {
        if (!analyses || analyses.length === 0) {
            const filterInfo = getFilterInfo(filters);
            historyContent.innerHTML = `
                <p class="history-placeholder">
                    No analysis history found${filterInfo ? ` with current filters${filterInfo}` : ''}.
                </p>
            `;
            return;
        }

        const filterInfo = getFilterInfo(filters);
        const filterHeader = filterInfo ? `<div class="filter-info">Showing results for: ${filterInfo}</div>` : '';

        const historyHTML = filterHeader + analyses.map(analysis => `
            <div class="history-item">
                <div class="history-item-header">
                    <h4 class="history-item-title">${analysis.title || 'Untitled Analysis'}</h4>
                    <span class="history-item-date">${new Date(analysis.created_at).toLocaleString()}</span>
                </div>
                <div class="history-item-summary">${analysis.summary}</div>
                <div class="history-item-meta">
                    <span>📊 ${analysis.sentiment}</span>
                    <span>🏷️ ${analysis.topics?.join(', ') || 'No topics'}</span>
                    <span>🔑 ${analysis.keywords?.join(', ') || 'No keywords'}</span>
                    <span>⏱️ ${analysis.processing_time?.toFixed(2)}s</span>
                </div>
            </div>
        `).join('');

        historyContent.innerHTML = historyHTML;
    }

    function getFilterInfo(filters) {
        const parts = [];
        if (filters.search) parts.push(`search: "${filters.search}"`);
        if (filters.sentiment) parts.push(`sentiment: ${filters.sentiment}`);
        if (filters.keyword) parts.push(`keyword: "${filters.keyword}"`);
        return parts.length > 0 ? ` (${parts.join(', ')})` : '';
    }
});
