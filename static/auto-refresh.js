/**
 * Auto-Refresh JavaScript for Weather & News Dashboard
 * =====================================================
 *
 * Features:
 * - Automatic data refresh without page reload
 * - Manual refresh button
 * - Loading indicators
 * - Error handling with retry logic
 * - Pause/resume functionality
 * - Smart update intervals
 */

// Configuration
const CONFIG = {
    WEATHER_INTERVAL: 600000,    // 10 minutes in milliseconds
    NEWS_INTERVAL: 300000,        // 5 minutes in milliseconds
    RETRY_DELAY: 5000,            // 5 seconds retry on error
    MAX_RETRIES: 3,               // Maximum retry attempts
    ANIMATION_DURATION: 300       // CSS transition duration in ms
};

// State management
const state = {
    weatherTimer: null,
    newsTimer: null,
    isRefreshing: false,
    isPaused: false,
    retryCount: 0,
    lastWeatherUpdate: null,
    lastNewsUpdate: null
};

/**
 * Initialize auto-refresh when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Auto-refresh initialized');

    // Start automatic refresh timers
    startAutoRefresh();

    // Setup manual refresh button if it exists
    setupRefreshButton();

    // Setup pause/resume button if it exists
    setupPauseButton();

    // Display last update times
    updateTimestamps();
});

/**
 * Start automatic refresh for weather and news
 */
function startAutoRefresh() {
    if (state.isPaused) {
        console.log('⏸️ Auto-refresh is paused');
        return;
    }

    // Refresh weather every 10 minutes
    state.weatherTimer = setInterval(() => {
        refreshWeather();
    }, CONFIG.WEATHER_INTERVAL);

    // Refresh news every 5 minutes
    state.newsTimer = setInterval(() => {
        refreshNews();
    }, CONFIG.NEWS_INTERVAL);

    console.log('✅ Auto-refresh timers started');
    console.log(`   Weather: Every ${CONFIG.WEATHER_INTERVAL / 1000}s`);
    console.log(`   News: Every ${CONFIG.NEWS_INTERVAL / 1000}s`);
}

/**
 * Stop all auto-refresh timers
 */
function stopAutoRefresh() {
    if (state.weatherTimer) {
        clearInterval(state.weatherTimer);
        state.weatherTimer = null;
    }

    if (state.newsTimer) {
        clearInterval(state.newsTimer);
        state.newsTimer = null;
    }

    console.log('⏹️ Auto-refresh stopped');
}

/**
 * Refresh weather data from API
 */
async function refreshWeather() {
    if (state.isRefreshing) {
        console.log('⏳ Refresh already in progress');
        return;
    }

    const weatherElement = document.querySelector('.weather-data');
    if (!weatherElement) return;

    try {
        // Show loading state
        showLoading(weatherElement);

        // Fetch weather data
        const response = await fetch('/api/weather');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            updateWeatherUI(data.data);
            state.lastWeatherUpdate = new Date();
            state.retryCount = 0;
            console.log('✅ Weather updated successfully');
        } else {
            throw new Error(data.error || 'Unknown error');
        }

    } catch (error) {
        console.error('❌ Weather refresh error:', error);
        handleRefreshError('weather', error);
    } finally {
        hideLoading(weatherElement);
    }
}

/**
 * Refresh news data from API
 */
async function refreshNews() {
    if (state.isRefreshing) {
        console.log('⏳ Refresh already in progress');
        return;
    }

    const newsElement = document.querySelector('.news-data');
    if (!newsElement) return;

    try {
        // Show loading state
        showLoading(newsElement);

        // Fetch news data
        const response = await fetch('/api/news');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            updateNewsUI(data.data);
            state.lastNewsUpdate = new Date();
            state.retryCount = 0;
            console.log('✅ News updated successfully');
        } else {
            throw new Error(data.error || 'Unknown error');
        }

    } catch (error) {
        console.error('❌ News refresh error:', error);
        handleRefreshError('news', error);
    } finally {
        hideLoading(newsElement);
    }
}

/**
 * Refresh all data (weather + news)
 */
async function refreshAll() {
    if (state.isRefreshing) {
        console.log('⏳ Refresh already in progress');
        return;
    }

    state.isRefreshing = true;

    try {
        await Promise.all([
            refreshWeather(),
            refreshNews()
        ]);

        showNotification('✅ Data refreshed successfully', 'success');
    } catch (error) {
        showNotification('❌ Refresh failed', 'error');
    } finally {
        state.isRefreshing = false;
    }
}

/**
 * Update weather UI with new data
 */
function updateWeatherUI(weatherData) {
    // Update temperature
    const tempElement = document.querySelector('.temperature');
    if (tempElement) {
        animateNumberChange(tempElement, weatherData.temp + '°C');
    }

    // Update description
    const descElement = document.querySelector('.weather-description');
    if (descElement) {
        fadeUpdate(descElement, weatherData.description);
    }

    // Update city
    const cityElement = document.querySelector('.weather-city');
    if (cityElement) {
        cityElement.textContent = weatherData.city;
    }

    // Update timestamp
    updateTimestamps();
}

/**
 * Update news UI with new data
 */
function updateNewsUI(newsData) {
    const newsContainer = document.querySelector('.news-list') ||
                         document.querySelector('.column ul');

    if (!newsContainer) return;

    // Fade out old content
    newsContainer.style.opacity = '0';

    setTimeout(() => {
        // Clear existing news
        newsContainer.innerHTML = '';

        // Add new news items
        newsData.forEach(article => {
            const listItem = createNewsElement(article);
            newsContainer.appendChild(listItem);
        });

        // Fade in new content
        newsContainer.style.opacity = '1';
    }, CONFIG.ANIMATION_DURATION);

    // Update timestamp
    updateTimestamps();
}

/**
 * Create news list item element
 */
function createNewsElement(article) {
    const li = document.createElement('li');

    const link = document.createElement('a');
    link.href = article.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = article.title;

    li.appendChild(link);

    // Add image if available
    if (article.image) {
        const img = document.createElement('img');
        img.src = article.image;
        img.alt = article.title;
        img.loading = 'lazy';
        img.style.maxWidth = '100%';
        img.style.marginTop = '0.75rem';
        img.style.borderRadius = '12px';
        li.appendChild(img);
    }

    return li;
}

/**
 * Show loading indicator on element
 */
function showLoading(element) {
    element.classList.add('loading');
    element.style.opacity = '0.6';
    element.style.pointerEvents = 'none';
}

/**
 * Hide loading indicator from element
 */
function hideLoading(element) {
    element.classList.remove('loading');
    element.style.opacity = '1';
    element.style.pointerEvents = 'auto';
}

/**
 * Animate number change with fade effect
 */
function animateNumberChange(element, newValue) {
    element.style.transition = `opacity ${CONFIG.ANIMATION_DURATION}ms`;
    element.style.opacity = '0';

    setTimeout(() => {
        element.textContent = newValue;
        element.style.opacity = '1';
    }, CONFIG.ANIMATION_DURATION);
}

/**
 * Fade update for text elements
 */
function fadeUpdate(element, newText) {
    element.style.transition = `opacity ${CONFIG.ANIMATION_DURATION}ms`;
    element.style.opacity = '0';

    setTimeout(() => {
        element.textContent = newText;
        element.style.opacity = '1';
    }, CONFIG.ANIMATION_DURATION);
}

/**
 * Handle refresh errors with retry logic
 */
function handleRefreshError(type, error) {
    state.retryCount++;

    if (state.retryCount < CONFIG.MAX_RETRIES) {
        console.log(`🔄 Retrying ${type} refresh (${state.retryCount}/${CONFIG.MAX_RETRIES})...`);

        setTimeout(() => {
            if (type === 'weather') {
                refreshWeather();
            } else if (type === 'news') {
                refreshNews();
            }
        }, CONFIG.RETRY_DELAY);
    } else {
        console.error(`❌ Max retries reached for ${type}`);
        showNotification(`Failed to update ${type}. Will retry later.`, 'error');
        state.retryCount = 0;
    }
}

/**
 * Setup manual refresh button
 */
function setupRefreshButton() {
    const refreshBtn = document.querySelector('.refresh-btn');

    if (refreshBtn) {
        refreshBtn.addEventListener('click', async function(e) {
            e.preventDefault();

            // Disable button during refresh
            this.disabled = true;
            this.textContent = '🔄 Refreshing...';

            await refreshAll();

            // Re-enable button
            this.disabled = false;
            this.textContent = '🔄 Refresh Data';
        });
    }
}

/**
 * Setup pause/resume button
 */
function setupPauseButton() {
    const pauseBtn = document.querySelector('.pause-btn');

    if (pauseBtn) {
        pauseBtn.addEventListener('click', function(e) {
            e.preventDefault();

            if (state.isPaused) {
                startAutoRefresh();
                state.isPaused = false;
                this.textContent = '⏸️ Pause';
                showNotification('Auto-refresh resumed', 'info');
            } else {
                stopAutoRefresh();
                state.isPaused = true;
                this.textContent = '▶️ Resume';
                showNotification('Auto-refresh paused', 'info');
            }
        });
    }
}

/**
 * Update last update timestamps
 */
function updateTimestamps() {
    const now = new Date();

    // Update weather timestamp
    if (state.lastWeatherUpdate) {
        const weatherTimestamp = document.querySelector('.weather-timestamp');
        if (weatherTimestamp) {
            weatherTimestamp.textContent = `Updated: ${formatTime(state.lastWeatherUpdate)}`;
        }
    }

    // Update news timestamp
    if (state.lastNewsUpdate) {
        const newsTimestamp = document.querySelector('.news-timestamp');
        if (newsTimestamp) {
            newsTimestamp.textContent = `Updated: ${formatTime(state.lastNewsUpdate)}`;
        }
    }
}

/**
 * Format time for display
 */
function formatTime(date) {
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

/**
 * Show notification to user
 */
function showNotification(message, type = 'info') {
    // Check if notification container exists
    let container = document.querySelector('.notification-container');

    if (!container) {
        container = document.createElement('div');
        container.className = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        `;
        document.body.appendChild(container);
    }

    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        background: ${type === 'success' ? '#48bb78' : type === 'error' ? '#f56565' : '#4299e1'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: slideIn 0.3s ease-out;
    `;

    container.appendChild(notification);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .loading {
        position: relative;
    }
    
    .loading::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 30px;
        height: 30px;
        margin: -15px 0 0 -15px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Export functions for manual use
window.dashboardRefresh = {
    refreshWeather,
    refreshNews,
    refreshAll,
    startAutoRefresh,
    stopAutoRefresh
};