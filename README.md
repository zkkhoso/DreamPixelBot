# Cricket Live Score Website 🏏

A modern, responsive cricket live score website that provides real-time updates for cricket matches around the world.

## ✨ Features

### 🔴 Live Score Updates
- **Real-time score updates** every 30 seconds
- **Live match indicators** with pulsing animations
- **Multiple match formats** - Test, ODI, T20
- **Detailed match information** including current batsmen, bowlers, and recent overs

### 🎨 Modern UI/UX
- **Responsive design** that works on all devices
- **Beautiful gradient backgrounds** and glassmorphism effects
- **Smooth animations** and hover effects
- **Interactive match cards** with detailed modals
- **Clean, modern typography** using Inter font

### 📊 Match Information
- **Current match status** and session details
- **Team scores** with overs and wickets
- **Venue information** and toss details
- **Recent ball-by-ball** updates
- **Upcoming fixtures** with schedules

### 🚀 Interactive Features
- **Click to view detailed match information** in a modal
- **Refresh button** to manually update scores
- **Navigation menu** for different sections
- **Notification system** for updates
- **Lazy loading** for performance optimization

## 🛠️ Technologies Used

- **HTML5** - Semantic markup and structure
- **CSS3** - Modern styling with Flexbox, Grid, and animations
- **Vanilla JavaScript** - Dynamic functionality and live updates
- **Font Awesome** - Icons and visual elements
- **Google Fonts** - Inter font family

## 🚀 How to Run

### Option 1: Simple File Server
1. Open your terminal/command prompt
2. Navigate to the project directory
3. Run a simple HTTP server:

**Python 3:**
```bash
python -m http.server 8000
```

**Python 2:**
```bash
python -m SimpleHTTPServer 8000
```

**Node.js (if you have it installed):**
```bash
npx http-server -p 8000
```

4. Open your browser and go to `http://localhost:8000`

### Option 2: Direct File Opening
Simply open the `index.html` file directly in your web browser by double-clicking it.

## 📱 Features Breakdown

### Live Matches Section
- **Test Matches**: Shows day/session information
- **ODI Matches**: Displays innings and overs
- **T20 Matches**: Real-time run rate and required runs

### Match Cards Include:
- Match type (Test/ODI/T20)
- Live status indicator
- Team names with flags
- Current scores
- Venue information
- Match status/session

### Detailed Match Modal:
- Complete match scorecard
- Current batsmen and their scores
- Current bowler information
- Recent overs with ball-by-ball details
- Toss information
- Match venue and status

### Upcoming Matches:
- Scheduled matches with timings
- Venue information
- Match formats

## 🎯 Simulated Live Updates

The website simulates real cricket match scenarios:
- **Realistic score progression** based on match format
- **Random but logical** score updates
- **Different update frequencies** for different formats
- **Authentic cricket terminology** and scenarios

## 📱 Responsive Design

The website is fully responsive and optimized for:
- **Desktop computers** (1200px+)
- **Tablets** (768px - 1199px)
- **Mobile phones** (up to 767px)

## 🔧 Customization

### Adding New Matches
Edit the `generateMockData()` function in `script.js` to add more matches:

```javascript
{
    id: 4,
    type: "ODI",
    status: "Live",
    teams: {
        team1: { name: "Team A", code: "TA", score: "200/5", overs: "35.2" },
        team2: { name: "Team B", code: "TB", score: "yet to bat", overs: "" }
    },
    currentInfo: "1st Innings",
    venue: "Your Stadium",
    toss: "Team A won the toss and elected to bat first",
    isLive: true,
    currentBatsmen: ["Player 1 (50*)", "Player 2 (25*)"],
    currentBowler: "Player 3",
    recentOvers: ["4", "1", "2", "0", "6", "1"]
}
```

### Styling Customization
- Edit `style.css` to change colors, fonts, or layout
- The main color scheme uses `#667eea` (blue) and `#764ba2` (purple)
- All animations and transitions can be modified in the CSS

### Update Frequency
Change the live update interval in `script.js`:
```javascript
// Update every 30 seconds (current)
this.updateInterval = setInterval(() => {
    this.updateLiveScores();
}, 30000); // Change this value (milliseconds)
```

## 🌟 Future Enhancements

Potential features that could be added:
- Integration with real cricket APIs
- User authentication and favorites
- Match predictions and statistics
- Social sharing functionality
- Push notifications
- Dark/light theme toggle
- Multiple language support

## 📞 Support

If you encounter any issues or have suggestions for improvements, please check the console for any JavaScript errors and ensure all files are properly loaded.

---

**Enjoy your cricket live score experience! 🏏**