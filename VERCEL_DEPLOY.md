# 🚀 Deploying StanChatBot to Vercel (Free)

This guide will help you deploy your StanChatBot to Vercel's free hosting platform.

## ⚠️ Important Limitations

**Before deploying to Vercel, understand these limitations:**

### 🚫 What Won't Work on Vercel Free:
- **Persistent Database**: SQLite and ChromaDB won't persist between deployments
- **Memory Across Sessions**: Conversations won't be remembered after serverless function restarts
- **File Storage**: No permanent file storage on serverless functions

### ✅ What Will Work:
- **Real-time Chat**: AI responses via Gemini API
- **Username Validation**: Client-side validation still works
- **Modern UI**: All frontend features work perfectly
- **Responsive Design**: Full mobile and desktop support

## 📁 Files Created for Vercel

I've created the following Vercel-optimized files:

```
Project/
├── api/
│   └── chat.py              # Serverless Python function
├── vercel.json              # Vercel configuration
├── requirements-vercel.txt  # Minimal Python dependencies
└── index.html              # Vercel-optimized frontend
```

## 🚀 Step-by-Step Deployment

### 1. **Get Your Google Gemini API Key**
```bash
# Visit: https://makersuite.google.com/app/apikey
# Create a new API key and copy it
```

### 2. **Prepare Your Repository**
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/StanChatBot.git
git branch -M main
git push -u origin main
```

### 3. **Deploy to Vercel**

**Option A: Using Vercel Dashboard**
1. Visit [vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Click **"New Project"**
4. Import your GitHub repository
5. Vercel will auto-detect the configuration

**Option B: Using Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project directory
vercel

# Follow the prompts:
# ? Set up and deploy "Project"? Y
# ? Which scope? [Your username]
# ? Link to existing project? N
# ? What's your project's name? stanchatbot
# ? In which directory is your code located? ./
```

### 4. **Set Environment Variables**
In Vercel Dashboard:
1. Go to your project → **Settings** → **Environment Variables**
2. Add: 
   - **Name**: `GEMINI_API_KEY`
   - **Value**: `your_actual_gemini_api_key_here`
3. Click **Save**

### 5. **Redeploy**
After setting environment variables:
```bash
vercel --prod
```

## 🎯 What's Different in Vercel Version

### **Frontend Changes (`index.html`)**
- **API Endpoint**: Changed from `http://127.0.0.1:5000/chat` to `/api/chat`
- **Notice Banner**: Added info about serverless deployment
- **No Persistent Memory**: Local storage only (no cross-session memory)

### **Backend Changes (`api/chat.py`)**
- **Serverless Function**: Uses `BaseHTTPRequestHandler` instead of Flask
- **Minimal Dependencies**: Only Gemini AI and basic libraries
- **No Database**: Removed SQLite and ChromaDB dependencies
- **CORS Headers**: Built-in CORS support for web requests

### **Configuration (`vercel.json`)**
- **Python Runtime**: Uses `@vercel/python` for serverless functions
- **Static Files**: Serves HTML directly
- **Environment Variables**: Secure API key handling
- **Routes**: Maps `/api/chat` to Python function

## 🧪 Testing Your Deployment

Once deployed, test these features:

### ✅ **Should Work:**
1. **Chat Interface**: Click robot button to open chat
2. **Username Validation**: Enter username (3+ characters)
3. **AI Responses**: Send messages and get Gemini AI replies
4. **Real-time Features**: Typing indicators, animations
5. **Mobile Responsive**: Test on different screen sizes

### ❌ **Won't Persist:**
1. **Conversation History**: Refreshing page clears chat
2. **Cross-Session Memory**: No memory between visits
3. **User Data**: No permanent user storage

## 💰 Vercel Free Tier Limits

- **Function Execution**: 100GB-hours per month
- **Function Duration**: 10 seconds max per request
- **Function Memory**: 1024MB max
- **Bandwidth**: 100GB per month
- **Domains**: Custom domains supported

## 🔧 Alternative Deployment Options

If you need persistent storage, consider:

### **1. Railway (Free Tier)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway new
railway up
```

### **2. Render (Free Tier)**
- Supports full Flask apps
- PostgreSQL database available
- 750 hours/month free

### **3. Heroku (Paid)**
- Full app hosting
- Add-on ecosystem
- PostgreSQL support

## 🐛 Troubleshooting

### **Common Issues:**

**1. API Key Not Working**
```bash
# Check environment variable in Vercel Dashboard
# Redeploy after setting variables
vercel --prod
```

**2. Function Timeout**
```bash
# Increase timeout in vercel.json (max 30s on free tier)
"functions": {
  "api/chat.py": {
    "maxDuration": 30
  }
}
```

**3. CORS Errors**
- Check if API endpoint is `/api/chat` not `/chat`
- Verify CORS headers in `api/chat.py`

**4. 404 Errors**
- Ensure `vercel.json` routes are correct
- Check file structure matches configuration

## 📈 Monitoring & Analytics

Vercel provides:
- **Function Logs**: View in Dashboard → Functions tab
- **Analytics**: Usage statistics and performance
- **Error Tracking**: Runtime error monitoring

## 🔄 Updates & Redeployment

To update your deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Vercel auto-deploys on git push
# Or manually redeploy:
vercel --prod
```

## 📝 Production Considerations

For a production-ready version:

1. **Database**: Use Vercel's database integrations
2. **Authentication**: Add user authentication
3. **Rate Limiting**: Implement request throttling  
4. **Error Handling**: Comprehensive error logging
5. **Security**: Input sanitization and validation
6. **Analytics**: User behavior tracking

## 🎉 Success!

Your StanChatBot should now be live at:
`https://your-project-name.vercel.app`

Share the link and enjoy your free AI chatbot deployment! 🤖✨

---

**Need help?** Check the [Vercel Documentation](https://vercel.com/docs) or create an issue in your repository.
