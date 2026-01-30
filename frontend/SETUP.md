# Setup Instructions

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed
```

### 3. Start Development Server

```bash
npm run dev
```

Open http://localhost:3000 in your browser.

## Default Credentials

For testing, you can:
1. Click "Create New Account" on the login page
2. Fill in the registration form
3. After registration, login with your credentials

## Features

### ✅ Implemented

- Login page with beautiful glassmorphism design
- Sign up page with password strength indicator
- Forgot password page with email verification
- Dashboard layout with header, sidebar, and footer
- Dark mode toggle
- Responsive design for all devices
- Real-time dashboard with metrics
- Toast notifications
- Smooth animations and transitions

### 🚧 Coming Soon

- Detailed metrics pages
- Instance management
- Alert configuration
- Analytics dashboard
- User settings

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Project Structure

```
src/
├── components/
│   ├── Auth/           # Authentication pages
│   ├── Layout/         # Layout components
│   ├── Dashboard/      # Dashboard components
│   └── Charts/         # Chart components
├── services/
│   └── api.js          # API client
├── App.jsx             # Main app
├── main.jsx            # Entry point
└── index.css           # Global styles
```

## Customization

### Colors

Edit `tailwind.config.js` to customize colors:

```javascript
colors: {
  primary: { ... },
  secondary: { ... },
  // Add your custom colors
}
```

### Theme

The app supports dark mode by default. Toggle using the moon/sun icon in the header.

## Deployment

### Docker

```bash
docker build -t cloud-monitor-frontend .
docker run -p 3000:80 cloud-monitor-frontend
```

### Production Build

```bash
npm run build
# Deploy the dist/ folder to your hosting service
```

## Troubleshooting

### Port Already in Use

If port 3000 is busy:
```bash
# Edit vite.config.js and change the port number
server: {
  port: 3001  // Use a different port
}
```

### API Connection Issues

1. Ensure backend is running on http://localhost:8000
2. Check VITE_API_URL in .env file
3. Check browser console for errors

### Dark Mode Not Working

Clear localStorage and refresh:
```javascript
localStorage.clear();
location.reload();
```

## Support

For issues or questions:
- Check the README.md
- Review the code comments
- Check browser console for errors

---

**Happy Coding! 🚀**
