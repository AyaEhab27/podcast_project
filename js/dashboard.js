// Dashboard functionality
let currentUser = null;

// Get current user
async function initDashboard() {
  const { data: { user }, error } = await supabase.auth.getUser();
  if (error || !user) {
    window.location.href = 'signin.html';
    return;
  }
  currentUser = user;
  
  // Update user name in dashboard
  const userName = user.user_metadata?.full_name || user.email?.split('@')[0];
  const headerTitle = document.querySelector('.dashboard-header h1');
  if (headerTitle && userName) {
    headerTitle.innerHTML = `Welcome back, ${userName}! 👋`;
  }
  
  await loadPodcasts();
  await loadStats();
}

// Load user podcasts
async function loadPodcasts() {
  if (!currentUser) return;
  
  try {
    const { data: podcasts, error } = await supabase
      .from('podcasts')
      .select('*')
      .eq('user_id', currentUser.id)
      .order('created_at', { ascending: false })
      .limit(5);
    
    if (error) throw error;
    
    document.getElementById('total-count').textContent = podcasts?.length || 0;
    
    const container = document.getElementById('recent-podcasts');
    if (!podcasts || podcasts.length === 0) {
      container.innerHTML = '<p>No podcasts yet. <a href="create.html">Create your first podcast!</a></p>';
    } else {
      container.innerHTML = podcasts.map(podcast => `
        <div class="podcast-card">
          <h4>${podcast.topic}</h4>
          <p style="color: #3b82f6; font-size: 0.8rem;">${new Date(podcast.created_at).toLocaleDateString()}</p>
          <button onclick="viewPodcast(${podcast.id})" class="btn-outline" style="margin-top: 0.5rem;">View Details</button>
        </div>
      `).join('');
    }
  } catch (error) {
    console.error('Error loading podcasts:', error);
  }
}

// Load stats
async function loadStats() {
  if (!currentUser) return;
  
  try {
    const { data: podcasts, error } = await supabase
      .from('podcasts')
      .select('*')
      .eq('user_id', currentUser.id);
    
    if (error) throw error;
    
    const totalMinutes = podcasts?.length * 5 || 0; // Assume 5 min per podcast
    document.getElementById('total-minutes').textContent = totalMinutes;
    document.getElementById('total-listeners').textContent = Math.floor(Math.random() * 100) + 10; // Mock data
  } catch (error) {
    console.error('Error loading stats:', error);
  }
}

window.viewPodcast = (id) => {
  window.location.href = `create.html?id=${id}`;
};

// Tab switching
const urlParams = new URLSearchParams(window.location.search);
const activeTab = urlParams.get('tab') || 'overview';

function switchTab(tabId) {
  window.history.pushState({}, '', `?tab=${tabId}`);
  
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
    if (btn.getAttribute('data-tab') === tabId) {
      btn.classList.add('active');
    }
  });
  
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
  });
  
  const activeContent = document.getElementById(tabId);
  if (activeContent) activeContent.classList.add('active');
}

// Initialize
initDashboard();