// Cricket Live Score Website JavaScript
class CricketLiveScore {
    constructor() {
        this.matches = [];
        this.upcomingMatches = [];
        this.updateInterval = null;
        this.init();
    }

    init() {
        this.generateMockData();
        this.renderMatches();
        this.renderUpcomingMatches();
        this.startLiveUpdates();
    }

    generateMockData() {
        // Current live matches
        this.matches = [
            {
                id: 1,
                type: "Test",
                status: "Live",
                teams: {
                    team1: {
                        name: "India",
                        code: "IND",
                        score: "287/4",
                        overs: "68.3"
                    },
                    team2: {
                        name: "Australia",
                        code: "AUS",
                        score: "445",
                        overs: "138.4"
                    }
                },
                currentInfo: "Day 3 - 2nd Session",
                venue: "Melbourne Cricket Ground",
                toss: "Australia won the toss and elected to bat first",
                isLive: true,
                currentBatsmen: ["Virat Kohli (45*)", "Ajinkya Rahane (23*)"],
                currentBowler: "Pat Cummins",
                recentOvers: ["1", "0", "4", "W", "1", "2"]
            },
            {
                id: 2,
                type: "ODI",
                status: "Live",
                teams: {
                    team1: {
                        name: "England",
                        code: "ENG",
                        score: "234/7",
                        overs: "47.2"
                    },
                    team2: {
                        name: "Pakistan",
                        code: "PAK",
                        score: "yet to bat",
                        overs: ""
                    }
                },
                currentInfo: "1st Innings",
                venue: "Lord's Cricket Ground",
                toss: "England won the toss and elected to bat first",
                isLive: true,
                currentBatsmen: ["Jos Buttler (34*)", "Chris Woakes (12*)"],
                currentBowler: "Shaheen Afridi",
                recentOvers: ["6", "1", "4", "0", "2", "1"]
            },
            {
                id: 3,
                type: "T20",
                status: "Live",
                teams: {
                    team1: {
                        name: "South Africa",
                        code: "SA",
                        score: "156/8",
                        overs: "20.0"
                    },
                    team2: {
                        name: "New Zealand",
                        code: "NZ",
                        score: "89/3",
                        overs: "12.4"
                    }
                },
                currentInfo: "2nd Innings - NZ need 68 runs in 44 balls",
                venue: "Eden Park, Auckland",
                toss: "New Zealand won the toss and elected to field first",
                isLive: true,
                currentBatsmen: ["Kane Williamson (28*)", "Glenn Phillips (15*)"],
                currentBowler: "Kagiso Rabada",
                recentOvers: ["8", "6", "4", "1", "W", "4"]
            }
        ];

        // Upcoming matches
        this.upcomingMatches = [
            {
                teams: "India vs Sri Lanka",
                time: "Tomorrow 2:30 PM",
                venue: "Wankhede Stadium, Mumbai",
                type: "ODI"
            },
            {
                teams: "Australia vs West Indies",
                time: "Dec 28, 10:00 AM",
                venue: "Gabba, Brisbane",
                type: "Test"
            },
            {
                teams: "England vs Bangladesh",
                time: "Dec 29, 7:30 PM",
                venue: "The Oval, London",
                type: "T20"
            },
            {
                teams: "Pakistan vs Afghanistan",
                time: "Dec 30, 3:00 PM",
                venue: "National Stadium, Karachi",
                type: "ODI"
            }
        ];
    }

    renderMatches() {
        const matchesGrid = document.getElementById('matchesGrid');
        
        if (this.matches.length === 0) {
            matchesGrid.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
            return;
        }

        matchesGrid.innerHTML = this.matches.map(match => this.createMatchCard(match)).join('');
    }

    createMatchCard(match) {
        const team1 = match.teams.team1;
        const team2 = match.teams.team2;
        
        return `
            <div class="match-card" onclick="openMatchModal(${match.id})">
                <div class="match-header">
                    <span class="match-type">${match.type}</span>
                    <span class="match-status">${match.status}</span>
                </div>
                
                <div class="teams">
                    <div class="team">
                        <div class="team-name">
                            <div class="team-flag"></div>
                            ${team1.name}
                        </div>
                        <div class="team-score">${team1.score}</div>
                    </div>
                    <div class="team">
                        <div class="team-name">
                            <div class="team-flag"></div>
                            ${team2.name}
                        </div>
                        <div class="team-score">${team2.score}</div>
                    </div>
                </div>
                
                <div class="match-info">
                    <span class="current-info">${match.currentInfo}</span>
                    <span class="venue-info">${match.venue}</span>
                </div>
            </div>
        `;
    }

    renderUpcomingMatches() {
        const upcomingContainer = document.getElementById('upcomingMatches');
        
        upcomingContainer.innerHTML = this.upcomingMatches.map(match => `
            <div class="upcoming-card">
                <div class="upcoming-teams">${match.teams}</div>
                <div class="upcoming-time">${match.time}</div>
                <div class="upcoming-venue">${match.venue}</div>
                <div class="match-type" style="margin-top: 0.5rem; display: inline-block;">${match.type}</div>
            </div>
        `).join('');
    }

    startLiveUpdates() {
        // Update scores every 30 seconds
        this.updateInterval = setInterval(() => {
            this.updateLiveScores();
        }, 30000);
    }

    updateLiveScores() {
        this.matches.forEach(match => {
            if (match.isLive) {
                this.simulateScoreUpdate(match);
            }
        });
        this.renderMatches();
    }

    simulateScoreUpdate(match) {
        const team1 = match.teams.team1;
        const team2 = match.teams.team2;
        
        // Simulate random score updates
        const updateProbability = Math.random();
        
        if (updateProbability > 0.7) {
            if (match.type === "T20") {
                this.updateT20Score(match);
            } else if (match.type === "ODI") {
                this.updateODIScore(match);
            } else if (match.type === "Test") {
                this.updateTestScore(match);
            }
        }
    }

    updateT20Score(match) {
        const runs = Math.floor(Math.random() * 7); // 0-6 runs
        const currentTeam = match.teams.team2.score.includes("need") ? "team2" : "team1";
        
        if (currentTeam === "team2") {
            // Update chasing team score
            const currentScore = match.teams.team2.score.split('/');
            const newRuns = parseInt(currentScore[0].split(' ')[0]) + runs;
            const wickets = currentScore[1];
            
            match.teams.team2.score = `${newRuns}/${wickets}`;
            
            // Update required runs
            const target = parseInt(match.teams.team1.score.split('/')[0]) + 1;
            const required = target - newRuns;
            const ballsLeft = (20 * 6) - this.convertOversToDeliveries(match.teams.team2.overs);
            
            match.currentInfo = `2nd Innings - NZ need ${required} runs in ${ballsLeft} balls`;
        }
        
        // Update recent overs
        match.recentOvers.shift();
        match.recentOvers.push(runs.toString());
    }

    updateODIScore(match) {
        const runs = Math.floor(Math.random() * 5); // 0-4 runs
        const currentScore = match.teams.team1.score.split('/');
        const newRuns = parseInt(currentScore[0]) + runs;
        
        match.teams.team1.score = `${newRuns}/${currentScore[1]}`;
        
        // Update recent overs
        match.recentOvers.shift();
        match.recentOvers.push(runs.toString());
    }

    updateTestScore(match) {
        const runs = Math.floor(Math.random() * 4); // 0-3 runs
        const currentScore = match.teams.team1.score.split('/');
        const newRuns = parseInt(currentScore[0]) + runs;
        
        match.teams.team1.score = `${newRuns}/${currentScore[1]}`;
        
        // Update recent overs
        match.recentOvers.shift();
        match.recentOvers.push(runs.toString());
    }

    convertOversToDeliveries(overs) {
        const parts = overs.split('.');
        return parseInt(parts[0]) * 6 + (parts[1] ? parseInt(parts[1]) : 0);
    }

    getMatchById(id) {
        return this.matches.find(match => match.id === parseInt(id));
    }

    refreshScores() {
        const refreshBtn = document.querySelector('.refresh-btn i');
        refreshBtn.style.animation = 'spin 1s linear infinite';
        
        // Simulate API call delay
        setTimeout(() => {
            this.updateLiveScores();
            refreshBtn.style.animation = 'none';
        }, 1000);
    }
}

// Global functions
function openMatchModal(matchId) {
    const cricket = window.cricketApp;
    const match = cricket.getMatchById(matchId);
    
    if (!match) return;
    
    const modal = document.getElementById('matchModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h2>${match.teams.team1.name} vs ${match.teams.team2.name}</h2>
        <div class="match-type" style="margin: 1rem 0;">${match.type} Match</div>
        
        <div class="modal-scores">
            <div class="team-detail">
                <h3>${match.teams.team1.name}</h3>
                <div class="score-large">${match.teams.team1.score}</div>
                ${match.teams.team1.overs ? `<div>Overs: ${match.teams.team1.overs}</div>` : ''}
            </div>
            
            <div class="team-detail">
                <h3>${match.teams.team2.name}</h3>
                <div class="score-large">${match.teams.team2.score}</div>
                ${match.teams.team2.overs ? `<div>Overs: ${match.teams.team2.overs}</div>` : ''}
            </div>
        </div>
        
        <div class="match-details">
            <p><strong>Current Status:</strong> ${match.currentInfo}</p>
            <p><strong>Venue:</strong> ${match.venue}</p>
            <p><strong>Toss:</strong> ${match.toss}</p>
            
            ${match.currentBatsmen ? `
                <div class="current-play">
                    <h4>Current Batsmen:</h4>
                    <ul>
                        ${match.currentBatsmen.map(batsman => `<li>${batsman}</li>`).join('')}
                    </ul>
                    <p><strong>Current Bowler:</strong> ${match.currentBowler}</p>
                </div>
            ` : ''}
            
            <div class="recent-overs">
                <h4>Recent Overs:</h4>
                <div class="overs-display">
                    ${match.recentOvers.map(over => `<span class="over-ball">${over}</span>`).join('')}
                </div>
            </div>
        </div>
        
        <style>
            .modal-scores {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
                margin: 2rem 0;
            }
            
            .team-detail {
                text-align: center;
                padding: 1rem;
                background: #f8f9fa;
                border-radius: 10px;
            }
            
            .score-large {
                font-size: 2rem;
                font-weight: bold;
                color: #333;
                margin: 0.5rem 0;
            }
            
            .match-details {
                margin-top: 2rem;
            }
            
            .match-details p {
                margin: 0.5rem 0;
            }
            
            .current-play {
                background: #e8f4fd;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
            }
            
            .current-play ul {
                margin: 0.5rem 0;
                padding-left: 1.5rem;
            }
            
            .overs-display {
                display: flex;
                gap: 0.5rem;
                margin-top: 0.5rem;
                flex-wrap: wrap;
            }
            
            .over-ball {
                background: #667eea;
                color: white;
                padding: 0.3rem 0.6rem;
                border-radius: 50%;
                font-weight: bold;
                min-width: 30px;
                text-align: center;
            }
        </style>
    `;
    
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('matchModal').style.display = 'none';
}

function refreshScores() {
    window.cricketApp.refreshScores();
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('matchModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.cricketApp = new CricketLiveScore();
    
    // Add some interactive features
    const navLinks = document.querySelectorAll('.nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Add notification for live updates
    let notificationShown = false;
    setTimeout(() => {
        if (!notificationShown) {
            showNotification('Live scores are updating automatically every 30 seconds');
            notificationShown = true;
        }
    }, 5000);
});

// Notification system
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #667eea;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 3000;
        animation: slideIn 0.5s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.5s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 4000);
}

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(notificationStyles);

// Performance optimization: Lazy load match details
const observerOptions = {
    threshold: 0.1,
    rootMargin: '50px'
};

const matchObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Apply observer to match cards when they're created
function observeMatchCards() {
    const matchCards = document.querySelectorAll('.match-card');
    matchCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        matchObserver.observe(card);
    });
}

// Call observer after matches are rendered
setTimeout(observeMatchCards, 100);