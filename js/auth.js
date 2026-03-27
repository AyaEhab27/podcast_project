// ============================================================
// auth.js — PodCraft AI Authentication
// ============================================================

// التحقق من وجود supabase
if (typeof supabase === 'undefined') {
  console.error('Supabase not initialized!');
}

// ---- Password Strength ----
function checkPasswordStrength(password) {
  let score = 0;
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++;

  const capped = Math.min(score, 5);
  const messages = ['', 'Too weak', 'Weak', 'Fair', 'Strong', 'Very strong!'];
  return { strength: capped, message: messages[capped] || '', percent: (capped / 5) * 100 };
}

// ---- Password Toggle ----
function setupPasswordToggle(inputId, buttonId) {
  const input = document.getElementById(inputId);
  const button = document.getElementById(buttonId);
  if (!input || !button) return;

  const eyeOpen = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`;
  const eyeClosed = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>`;

  button.innerHTML = eyeOpen;

  button.addEventListener('click', () => {
    const isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';
    button.innerHTML = isPassword ? eyeClosed : eyeOpen;
  });
}

// ---- Set button loading state ----
function setButtonLoading(btn, loading, originalText) {
  if (!btn) return;
  if (loading) {
    btn.disabled = true;
    btn.dataset.originalText = btn.textContent;
    btn.innerHTML = `<span class="spinner"></span> Please wait...`;
  } else {
    btn.disabled = false;
    btn.textContent = originalText || btn.dataset.originalText || 'Submit';
  }
}

// ============================================================
// SIGN UP PAGE
// ============================================================
const signupForm = document.getElementById('signup-form');
if (signupForm) {
  setupPasswordToggle('password', 'toggle-password');
  setupPasswordToggle('confirm-password', 'toggle-confirm-password');

  const passwordInput = document.getElementById('password');
  if (passwordInput) {
    passwordInput.addEventListener('input', (e) => {
      const { percent, message } = checkPasswordStrength(e.target.value);
      const bar = document.getElementById('strength-bar-fill');
      const text = document.getElementById('strength-text');

      if (bar) {
        bar.style.width = `${percent}%`;
        bar.style.background = percent < 40 ? '#ef4444' : percent < 70 ? '#f59e0b' : '#22c55e';
      }
      if (text) text.textContent = message;
    });
  }

  signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fullname = document.getElementById('fullname')?.value?.trim();
    const email = document.getElementById('email')?.value?.trim();
    const password = document.getElementById('password')?.value;
    const confirmPassword = document.getElementById('confirm-password')?.value;
    const termsChecked = document.getElementById('terms')?.checked;

    if (!fullname || !email || !password) {
      showToast('Please fill in all required fields.', 'warning');
      return;
    }
    if (!termsChecked) {
      showToast('Please accept the Terms & Conditions.', 'warning');
      return;
    }
    if (password !== confirmPassword) {
      showToast('Passwords do not match.', 'error');
      return;
    }

    const submitBtn = signupForm.querySelector('[type="submit"]');
    setButtonLoading(submitBtn, true);

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: { data: { full_name: fullname } }
      });

      if (error) throw error;

      if (data?.user) {
        try {
          await supabase.from('profiles').upsert([{
            id: data.user.id,
            email: email,
            full_name: fullname,
            created_at: new Date().toISOString()
          }]);
        } catch (profileErr) {
          console.warn('Profile creation warning:', profileErr);
        }
      }

      showToast('Account created! Please check your email to confirm.', 'success', 5000);
      setTimeout(() => { window.location.href = 'signin.html'; }, 3000);

    } catch (err) {
      console.error('SignUp error:', err);
      const msg = err.message?.includes('already registered')
        ? 'This email is already registered.'
        : err.message || 'Could not create account.';
      showToast(msg, 'error');
    } finally {
      setButtonLoading(submitBtn, false, 'Create Account');
    }
  });
}

// ============================================================
// SIGN IN PAGE
// ============================================================
const signinForm = document.getElementById('signin-form');
if (signinForm) {
  setupPasswordToggle('password', 'toggle-password');

  signinForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email')?.value?.trim();
    const password = document.getElementById('password')?.value;

    if (!email || !password) {
      showToast('Please enter email and password.', 'warning');
      return;
    }

    const submitBtn = signinForm.querySelector('[type="submit"]');
    setButtonLoading(submitBtn, true);

    try {
      const { data, error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) throw error;

      showToast(`Welcome back! 👋`, 'success');
      setTimeout(() => { window.location.href = 'dashboard.html'; }, 1500);

    } catch (err) {
      console.error('SignIn error:', err);
      showToast('Incorrect email or password.', 'error');
    } finally {
      setButtonLoading(submitBtn, false, 'Sign In');
    }
  });
}

// ============================================================
// FORGOT PASSWORD - Redirect to separate page
// ============================================================
// ============================================================
// FORGOT PASSWORD - Redirect to separate page
// ============================================================
const forgotPasswordLink = document.getElementById('forgot-password');
if (forgotPasswordLink) {
  forgotPasswordLink.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = 'forgot-password.html';
  });
}

// ============================================================
// LOGOUT
// ============================================================
window.logout = async function () {
  try {
    await supabase.auth.signOut();
    showToast('Logged out successfully!', 'info');
    setTimeout(() => { window.location.href = 'index.html'; }, 1200);
  } catch (err) {
    showToast('Logout failed.', 'error');
  }
};

// ============================================================
// CHECK AUTH STATE
// ============================================================
async function checkAuth() {
  try {
    // التحقق من وجود supabase
    if (!supabase || !supabase.auth) {
      console.error('Supabase auth not available');
      return;
    }
    
    const { data: { user }, error } = await supabase.auth.getUser();
    
    if (error) {
      console.warn('Auth check warning:', error.message);
    }

    const navMenu = document.getElementById('nav-menu');
    const navButtons = document.getElementById('nav-buttons');
    const currentPath = window.location.pathname;
    const isIndex = currentPath.includes('index.html') || currentPath === '/' || currentPath.endsWith('/');
    const isProtected = currentPath.includes('dashboard.html') || currentPath.includes('create.html');
    const isAuthPage = currentPath.includes('signin.html') || currentPath.includes('signup.html') || currentPath.includes('forgot-password.html');

    if (user) {
      // User is logged in
      const displayName = user.user_metadata?.full_name || user.email?.split('@')[0] || 'User';

      if (navMenu && isIndex) {
        navMenu.innerHTML = `
          <li><a href="dashboard.html">Dashboard</a></li>
          <li><a href="create.html">Create New</a></li>
           <li><a href="personas.html">Personas</a></li>
          <li><a href="dashboard.html?tab=library">My Library</a></li>
          <li><a href="dashboard.html?tab=settings">Settings</a></li>
        `;
      }
      if (navButtons && isIndex) {
        navButtons.innerHTML = `
          <span style="color: rgba(255,255,255,0.8); font-size: 0.875rem;">👋 ${displayName}</span>
          <button onclick="logout()" class="btn-outline">Logout</button>
        `;
      }

      if (isAuthPage && !currentPath.includes('forgot-password.html')) {
        window.location.href = 'dashboard.html';
      }

    } else {
      // User is not logged in
      if (navMenu && isIndex) {
        navMenu.innerHTML = `
          <li><a href="index.html">Home</a></li>
          <li><a href="#features">Features</a></li>
          <li><a href="#how-it-works">How it works</a></li>
          <li><a href="signup.html">Get Started</a></li>
        `;
      }
      if (navButtons && isIndex) {
        navButtons.innerHTML = `
          <a href="signin.html" class="btn-outline">Sign In</a>
          <a href="signup.html" class="btn-primary">Get Started Free</a>
        `;
      }

      if (isProtected) {
        window.location.href = 'signin.html';
      }
    }
  } catch (err) {
    console.error('checkAuth error:', err);
  }
}

// Newsletter subscription
const newsletterForm = document.getElementById('newsletter-form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = newsletterForm.querySelector('input[type="email"]');
    const email = input?.value?.trim();
    if (!email) {
      showToast('Please enter a valid email.', 'warning');
      return;
    }

    try {
      const { error } = await supabase.from('subscribers').insert([{
        email: email,
        subscribed_at: new Date().toISOString()
      }]);

      if (error) {
        if (error.code === '23505') {
          showToast('You are already subscribed! 🎉', 'info');
          return;
        }
        throw error;
      }

      showToast('Subscribed successfully! 🚀', 'success');
      newsletterForm.reset();
    } catch (err) {
      console.error('Newsletter error:', err);
      showToast('Subscription failed. Please try again.', 'error');
    }
  });
}

// Run on page load - تأكد من تحميل supabase أولاً
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', checkAuth);
} else {
  checkAuth();
}
// +++++++++++++++
// ============================================================
// SOCIAL LOGIN — Google
// ============================================================
async function handleGoogleSign() {
  try {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/dashboard.html`,
        queryParams: {
          access_type: 'offline',
          prompt: 'consent',
        }
      }
    });
    if (error) throw error;
  } catch (err) {
    console.error('Google sign-in error:', err);
    showToast(err.message || 'Google sign-in failed. Please try again.', 'error');
  }
}

// ============================================================
// SOCIAL LOGIN — GitHub
// ============================================================
async function handleGitHubSign() {
  try {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: {
        redirectTo: `${window.location.origin}/dashboard.html`
      }
    });
    if (error) throw error;
  } catch (err) {
    console.error('GitHub sign-in error:', err);
    showToast(err.message || 'GitHub sign-in failed. Please try again.', 'error');
  }
}

// Bind social buttons - تأكد من وجود الأزرار
document.addEventListener('DOMContentLoaded', () => {
  const googleSignin = document.getElementById('google-signin');
  const googleSignup = document.getElementById('google-signup');
  const githubSignin = document.getElementById('github-signin');
  const githubSignup = document.getElementById('github-signup');
  
  if (googleSignin) googleSignin.addEventListener('click', handleGoogleSign);
  if (googleSignup) googleSignup.addEventListener('click', handleGoogleSign);
  if (githubSignin) githubSignin.addEventListener('click', handleGitHubSign);
  if (githubSignup) githubSignup.addEventListener('click', handleGitHubSign);
});