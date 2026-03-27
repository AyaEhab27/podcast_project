// // Supabase Configuration
// // استبدلي هذه البيانات ببيانات مشروعك من Supabase Dashboard
// const SUPABASE_URL = 'https://ynkpduwusonljopudzhy.supabase.co';  // من Project Settings -> API
// const SUPABASE_ANON_KEY = 'sb_publishable_qFD67bP1oHfulSgfo4enag_hpAuHjxW';  // من Project Settings -> API

// // Initialize Supabase client
// const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// // Helper functions
// const supabaseAuth = {
//     // Sign Up
//     signUp: async (email, password, fullname) => {
//         const { data, error } = await supabase.auth.signUp({
//             email: email,
//             password: password,
//             options: {
//                 data: {
//                     full_name: fullname
//                 }
//             }
//         });
        
//         if (error) throw error;
        
//         // Create user profile in database
//         if (data.user) {
//             await supabase
//                 .from('profiles')
//                 .insert([
//                     {
//                         id: data.user.id,
//                         email: email,
//                         full_name: fullname,
//                         created_at: new Date().toISOString()
//                     }
//                 ]);
//         }
        
//         return data;
//     },
    
//     // Sign In
//     signIn: async (email, password, remember = false) => {
//         const { data, error } = await supabase.auth.signInWithPassword({
//             email: email,
//             password: password
//         });
        
//         if (error) throw error;
//         return data;
//     },
    
//     // Sign In with Google
//     signInWithGoogle: async () => {
//         const { data, error } = await supabase.auth.signInWithOAuth({
//             provider: 'google',
//             options: {
//                 redirectTo: window.location.origin + '/dashboard.html'
//             }
//         });
        
//         if (error) throw error;
//         return data;
//     },
    
//     // Sign In with GitHub
//     signInWithGitHub: async () => {
//         const { data, error } = await supabase.auth.signInWithOAuth({
//             provider: 'github',
//             options: {
//                 redirectTo: window.location.origin + '/dashboard.html'
//             }
//         });
        
//         if (error) throw error;
//         return data;
//     },
    
//     // Sign Out
//     signOut: async () => {
//         const { error } = await supabase.auth.signOut();
//         if (error) throw error;
//     },
    
//     // Get Current User
//     getCurrentUser: async () => {
//         const { data: { user }, error } = await supabase.auth.getUser();
//         if (error) throw error;
//         return user;
//     },
    
//     // Reset Password
//     resetPassword: async (email) => {
//         const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
//             redirectTo: window.location.origin + '/reset-password.html'
//         });
//         if (error) throw error;
//         return data;
//     }
// };

// // Database operations
// const supabaseDB = {
//     // Save podcast
//     savePodcast: async (podcast, userId) => {
//         const { data, error } = await supabase
//             .from('podcasts')
//             .insert([
//                 {
//                     user_id: userId,
//                     topic: podcast.topic,
//                     script: podcast.script,
//                     host_voice: podcast.hostVoice,
//                     guest_voice: podcast.guestVoice,
//                     created_at: new Date().toISOString(),
//                     type: podcast.type
//                 }
//             ]);
        
//         if (error) throw error;
//         return data;
//     },
    
//     // Get user podcasts
//     getUserPodcasts: async (userId) => {
//         const { data, error } = await supabase
//             .from('podcasts')
//             .select('*')
//             .eq('user_id', userId)
//             .order('created_at', { ascending: false });
        
//         if (error) throw error;
//         return data;
//     },
    
//     // Get single podcast
//     getPodcast: async (podcastId) => {
//         const { data, error } = await supabase
//             .from('podcasts')
//             .select('*')
//             .eq('id', podcastId)
//             .single();
        
//         if (error) throw error;
//         return data;
//     },
    
//     // Delete podcast
//     deletePodcast: async (podcastId) => {
//         const { error } = await supabase
//             .from('podcasts')
//             .delete()
//             .eq('id', podcastId);
        
//         if (error) throw error;
//     },
    
//     // Subscribe to newsletter
//     subscribeNewsletter: async (email) => {
//         const { data, error } = await supabase
//             .from('subscribers')
//             .insert([{ email: email, subscribed_at: new Date().toISOString() }]);
        
//         if (error) throw error;
//         return data;
//     },
    
//     // Update user profile
//     updateProfile: async (userId, updates) => {
//         const { data, error } = await supabase
//             .from('profiles')
//             .update(updates)
//             .eq('id', userId);
        
//         if (error) throw error;
//         return data;
//     }
// };
// Supabase Configuration
// Supabase Configuration
// Supabase Configuration
// Supabase Configuration
// Supabase Configuration
// ============================================================
// Supabase Configuration — PodCraft AI
// ============================================================
// ============================================================
// Supabase Configuration — PodCraft AI
// ============================================================
// ============================================================
// Supabase Configuration — PodCraft AI
// ============================================================

// منع إعادة التصريح
// ============================================================
// Supabase Configuration — PodCraft AI
// ============================================================

// منع إعادة التصريح
// if (typeof window._supabaseInitialized === 'undefined') {
  
//   const SUPABASE_URL = 'https://ynkpduwusonljopudzhy.supabase.co';
//   const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlua3BkdXd1c29ubGpvcHVkemh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzODc5MTUsImV4cCI6MjA4OTk2MzkxNX0.g0mo6VpTMnJCqTi23npaanWLZz7i-j--AF6Eme6F9SI';

//   // Initialize Supabase client
//   window.supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
//   window._supabaseInitialized = true;
  
//   console.log('Supabase initialized successfully');
// }

// // ============================================================
// // TOAST NOTIFICATION SYSTEM
// // ============================================================
// (function initToasts() {
//   let container = document.getElementById('toast-container');
//   if (!container) {
//     container = document.createElement('div');
//     container.id = 'toast-container';
//     container.className = 'toast-container';
//     document.body.appendChild(container);
//   }
// })();

// const TOAST_ICONS = {
//   success: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>`,
//   error:   `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`,
//   warning: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
//   info:    `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`
// };

// const TOAST_TITLES = {
//   success: 'Success',
//   error: 'Error',
//   warning: 'Warning',
//   info: 'Info'
// };

// window.showToast = function showToast(message, type = 'info', duration = 5000) {
//   const container = document.getElementById('toast-container');
//   if (!container) return;

//   const toast = document.createElement('div');
//   toast.className = `toast ${type}`;

//   toast.innerHTML = `
//     <div class="toast-icon">${TOAST_ICONS[type] || TOAST_ICONS.info}</div>
//     <div class="toast-body">
//       <div class="toast-title">${TOAST_TITLES[type] || 'Notice'}</div>
//       <div class="toast-message">${message}</div>
//     </div>
//     <button class="toast-close" aria-label="Close">×</button>
//     <div class="toast-progress" style="animation-duration: ${duration}ms"></div>
//   `;

//   container.appendChild(toast);

//   const closeBtn = toast.querySelector('.toast-close');
//   const removeToast = () => {
//     toast.classList.add('removing');
//     setTimeout(() => toast.remove(), 300);
//   };

//   closeBtn.addEventListener('click', removeToast);
//   setTimeout(removeToast, duration);

//   return toast;
// };
// Supabase Configuration
const SUPABASE_URL = 'https://ynkpduwusonljopudzhy.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_qFD67bP1oHfulSgfo4enag_hpAuHjxW';  // Publishable Key

// Initialize Supabase client
window.supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
window._supabaseInitialized = true;

console.log('Supabase initialized successfully');

// ============================================================
// TOAST NOTIFICATION SYSTEM
// ============================================================
(function initToasts() {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
})();

const TOAST_ICONS = {
  success: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>`,
  error:   `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`,
  warning: `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
  info:    `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`
};

const TOAST_TITLES = {
  success: 'Success',
  error: 'Error',
  warning: 'Warning',
  info: 'Info'
};

window.showToast = function showToast(message, type = 'info', duration = 5000) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  toast.innerHTML = `
    <div class="toast-icon">${TOAST_ICONS[type] || TOAST_ICONS.info}</div>
    <div class="toast-body">
      <div class="toast-title">${TOAST_TITLES[type] || 'Notice'}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close" aria-label="Close">×</button>
    <div class="toast-progress" style="animation-duration: ${duration}ms"></div>
  `;

  container.appendChild(toast);

  const closeBtn = toast.querySelector('.toast-close');
  const removeToast = () => {
    toast.classList.add('removing');
    setTimeout(() => toast.remove(), 300);
  };

  closeBtn.addEventListener('click', removeToast);
  setTimeout(removeToast, duration);

  return toast;
};