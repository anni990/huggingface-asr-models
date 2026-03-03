# Audio Transcription - Frontend

Modern, responsive web interface for the Audio Transcription API built with **React**, **Vite**, and **Tailwind CSS** featuring a professional dark theme design.

## 🎨 Features

- ⚡ **React + Vite**: Lightning-fast development with hot module replacement
- 🎨 **Tailwind CSS**: Modern, utility-first CSS framework with dark theme
- 🌑 **Professional Dark Theme**: Minimalist design with perfect alignment and spacing
- 📤 **Drag & Drop**: Intuitive file upload with drag-and-drop support
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- 🎯 **Real-time Feedback**: Live status updates and comprehensive error handling
- 📋 **Copy to Clipboard**: One-click copy of transcription results
- 🔄 **API Status Monitoring**: Real-time API health status display
- 🎛️ **Model Management**: Full model lifecycle management (load, unload, delete)
- ✨ **Smooth Animations**: Professional fade-in and slide-up animations
- 🔔 **Toast Notifications**: Non-intrusive success and error notifications

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # React components
│   │   ├── Header.jsx           # Header with status badge
│   │   ├── TabNavigation.jsx    # Tab switching component
│   │   ├── TranscribeTab.jsx    # Main transcription interface
│   │   ├── ModelsTab.jsx        # Model management interface
│   │   ├── FileUpload.jsx       # File upload with drag-and-drop
│   │   ├── TranscriptionResults.jsx  # Results display
│   │   ├── ModelsList.jsx       # Models list component
│   │   ├── LoadingSpinner.jsx   # Loading state component
│   │   └── Toast.jsx            # Toast notifications
│   ├── services/          # API service layer
│   │   └── api.js              # Axios-based API client
│   ├── App.jsx            # Main application component
│   ├── main.jsx           # Application entry point
│   └── index.css          # Global styles with Tailwind
├── index.html             # HTML entry point
├── package.json           # Dependencies and scripts
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── postcss.config.js      # PostCSS configuration
└── README.md              # This file
```

## 🚀 Setup

### Prerequisites

- **Node.js** 18+ (with npm)
- Audio Transcription API backend running (default: http://localhost:8000)
- Modern web browser with JavaScript enabled

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

   This will install:
   - React 18.2+
   - Vite 5.0+
   - Tailwind CSS 3.4+
   - Axios for API calls
   - Other dev dependencies

## 🏃 Running the Frontend

### Development Mode (Recommended)

**Windows:**
```bash
.\start-frontend.bat
```

**Linux/Mac:**
```bash
./start-frontend.sh
```

**Or manually:**
```bash
cd frontend
npm run dev
```

The development server will start at: **http://localhost:5173**

Features in dev mode:
- ⚡ Hot Module Replacement (HMR)
- 🔄 Instant updates on file changes
- 🐛 Better error messages
- 📊 Performance monitoring

### Production Build

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Preview production build:**
   ```bash
   npm run preview
   ```

The build output will be in the `dist/` directory.

### Running Both Frontend & Backend

**Windows:**
```bash
.\run.bat
```

This will start both servers in separate terminal windows:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🎯 Usage

### 1. Transcription Tab

1. **Check API Status**: The status badge in the header shows if the backend API is online (green) or offline (red)
2. **Select Model**: Choose a loaded model from the dropdown
   - If no models are loaded, go to Model Management tab
3. **Upload Audio**:
   - Click the upload area to browse files
   - Or drag and drop an audio file directly
4. **Transcribe**: Click the "Transcribe" button
5. **View Results**: See transcription with metadata (duration, processing time, character count)
6. **Copy**: Click "Copy" to copy transcription to clipboard

### 2. Model Management Tab

1. **Load New Model**: Enter a HuggingFace model ID or click on recommended models
2. **View Models**: See all registered models with their status (loaded/not loaded)
3. **Model Actions**:
   - **Load**: Download and load a model into memory
   - **Unload**: Remove model from memory (keeps in registry)
   - **Delete**: Completely remove model from registry and memory

## ⚙️ Configuration

### API URL
Edit [src/services/api.js](src/services/api.js) to change the API endpoint:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

For production:
```javascript
const API_BASE_URL = 'https://your-api-domain.com';
```

### Port Configuration
Edit [vite.config.js](vite.config.js) to change the development server port:

```javascript
export default defineConfig({
  server: {
    port: 5173,  // Change to your preferred port
  },
})
```

### Supported Audio Formats
- WAV (.wav)
- MP3 (.mp3)
- FLAC (.flac)
- M4A (.m4a)
- OGG (.ogg)

**Maximum file size:** 25 MB

## 🎨 Design Features

### Dark Theme
- Professional minimalist design
- Optimized color palette for reduced eye strain
- High contrast for better readability
- Consistent spacing and alignment

### Color Scheme
```css
Background: #0f172a (dark-bg)
Cards: #1e293b (dark-card)
Borders: #475569 (dark-border)
Text: #e5e7eb (gray-200)
Accents: Blue (#3b82f6), Green, Purple, Orange
```

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Animations
- **fade-in**: Smooth element appearance
- **slide-up**: Bottom-to-top slide animation
- **spinner**: Rotating loading indicator

## 🔧 Customization

### Styling
Modify [tailwind.config.js](tailwind.config.js) to customize colors, spacing, and animations:

```javascript
theme: {
  extend: {
    colors: {
      dark: {
        bg: '#0f172a',      // Change background color
        card: '#1e293b',    // Change card color
      },
    },
  },
}
```

### Components
All components are in the `src/components/` directory. Each component is self-contained and can be easily modified:

- **Header.jsx**: Header and status badge
- **TabNavigation.jsx**: Tab switching logic
- **TranscribeTab.jsx**: Transcription interface
- **ModelsTab.jsx**: Model management interface
- **FileUpload.jsx**: File upload with drag-and-drop
- **TranscriptionResults.jsx**: Results display
- **ModelsList.jsx**: Models list with actions
- **LoadingSpinner.jsx**: Loading states
- **Toast.jsx**: Notifications

### API Service
Edit [src/services/api.js](src/services/api.js) to add new API endpoints:

```javascript
export const apiService = {
  // Add new endpoint
  getModelInfo: async (modelId) => {
    const response = await api.get(`/api/v1/models/${modelId}`);
    return response.data;
  },
};
```

## 🌐 Browser Compatibility

Tested and working on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

Modern features used:
- ES6+ JavaScript
- React Hooks
- Async/Await
- Fetch API / Axios
- FormData
- Clipboard API
- Drag and Drop API

## 🐛 Troubleshooting

### "API is offline" Error
**Solution**: Ensure the backend server is running at `http://localhost:8000`

Check with:
```bash
curl http://localhost:8000/health
# or
Invoke-WebRequest -Uri http://localhost:8000/health
```

### CORS Errors
**Solution**: Configure CORS in backend `backend/app/core/config.py` or `.env`:
```python
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### Port Already in Use
**Error**: `Port 5173 is already in use`

**Solution**:
1. Stop the process using port 5173
2. Or change the port in `vite.config.js`

### Dependencies Installation Fails
**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Build Errors
**Solution**:
```bash
# Check Node.js version (should be 18+)
node --version

# Update npm
npm install -g npm@latest

# Try rebuilding
npm run build
```

### File Upload Fails
**Possible causes**:
- File format not supported
- File size exceeds 25MB
- API is not responding
- Selected model not loaded

**Solution**: 
- Check browser console (F12 → Console)
- Verify file format and size
- Ensure a model is loaded in Model Management tab

## 📦 Production Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` folder with:
- Minified JavaScript and CSS
- Optimized assets
- Tree-shaking for smaller bundle size
- Source maps for debugging

### Deploy to Static Hosting

**Vercel:**
```bash
npm install -g vercel
vercel --prod
```

**Netlify:**
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

**GitHub Pages:**
1. Build the project: `npm run build`
2. Deploy the `dist/` folder to GitHub Pages

### Environment Variables
Create `.env` file for production:
```env
VITE_API_BASE_URL=https://your-api-domain.com
```

Update [src/services/api.js](src/services/api.js):
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

## 📊 Performance

### Optimization Tips
- ✅ Code splitting with React.lazy()
- ✅ Image optimization
- ✅ Minimize bundle size
- ✅ Use production build for deployment
- ✅ Enable gzip compression on server

### Lighthouse Score Targets
- Performance: 90+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 90+

## 🤝 Contributing

To contribute to the frontend:

1. Make changes to components in `src/components/`
2. Test locally with `npm run dev`
3. Ensure no errors with `npm run lint`
4. Build for production with `npm run build`
5. Submit pull request

## 📝 License

This project is part of the Audio Transcription API system.

## 🔗 Related Documentation

- [Backend API Documentation](../backend/README.md)
- [Project Overview](../README.md)
- [Quick Start Guide](../QUICKSTART.md)

## 💡 Tips

1. **Keep Dependencies Updated**: Run `npm outdated` to check for updates
2. **Use Dev Tools**: React DevTools browser extension for debugging
3. **Monitor Performance**: Use Chrome DevTools Performance tab
4. **Test Responsively**: Use browser responsive design mode
5. **Check Accessibility**: Use axe DevTools extension

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [Vite Guide](https://vitejs.dev)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [Axios Documentation](https://axios-http.com)

---

**Built with ❤️ using React, Vite, and Tailwind CSS**

