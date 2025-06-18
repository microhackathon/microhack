# Fixing Google OAuth Verification Error

## 🔍 **Why This Error Occurs**

The error "microhack has not completed the Google verification process" happens because:

1. **New OAuth apps are in testing mode** by default
2. **Google requires verification** for production apps
3. **Your app needs to be configured** for development use

## ✅ **How to Fix It**

### **Option 1: Add Test Users (Quick Fix)**

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Navigate to OAuth consent screen**:
   - Go to "APIs & Services" > "OAuth consent screen"
3. **Add test users**:
   - Scroll down to "Test users" section
   - Click "Add Users"
   - Add your Google email address
   - Click "Save"

### **Option 2: Configure for Development (Recommended)**

1. **Go to OAuth consent screen**:
   - https://console.cloud.google.com/apis/credentials/consent
2. **Set app information**:
   - App name: "MicroHack Data Pipeline"
   - User support email: Your email
   - Developer contact information: Your email
3. **Configure scopes**:
   - Add scope: `https://www.googleapis.com/auth/drive.readonly`
4. **Add test users**:
   - Add your Google account email
5. **Save changes**

### **Option 3: Use Service Account (Alternative)**

If OAuth continues to be problematic, we can switch to a service account approach.

## 🔧 **Step-by-Step Instructions**

### **Step 1: Access OAuth Consent Screen**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to "APIs & Services" > "OAuth consent screen"

### **Step 2: Configure App Information**
```
App name: MicroHack Data Pipeline
User support email: [your-email@gmail.com]
App logo: (optional)
App domain: (leave blank for now)
Developer contact information: [your-email@gmail.com]
```

### **Step 3: Add Scopes**
1. Click "Add or remove scopes"
2. Find and select: `https://www.googleapis.com/auth/drive.readonly`
3. Click "Update"

### **Step 4: Add Test Users**
1. Scroll to "Test users" section
2. Click "Add Users"
3. Add your Google account email address
4. Click "Save"

### **Step 5: Test Authentication**
After making these changes, try running the authentication again:
```bash
./setup_auth.py
```

## 🚨 **Important Notes**

- **Test users only**: In testing mode, only added test users can authenticate
- **No verification needed**: For development/testing, you don't need Google verification
- **Production use**: If you plan to distribute this app, you'll need Google verification

## 🔄 **Alternative: Service Account**

If OAuth continues to be problematic, we can create a service account instead:

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Download the JSON key file
4. Share your Google Drive folder with the service account email

Would you like me to help you implement the service account approach instead? 