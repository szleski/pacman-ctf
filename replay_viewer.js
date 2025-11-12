// Pacman CTF Replay Viewer JavaScript

class ReplayViewer {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.replayData = null;
        this.currentFrame = 0;
        this.isPlaying = false;
        this.playInterval = null;
        this.gameStates = [];
        this.fps = 5;
        this.cellSize = 20;
        
        this.initControls();
        this.loadReplayList();
    }
    
    initControls() {
        document.getElementById('load-btn').addEventListener('click', () => this.loadReplay());
        document.getElementById('first-btn').addEventListener('click', () => this.goToFrame(0));
        document.getElementById('prev-btn').addEventListener('click', () => this.previousFrame());
        document.getElementById('play-btn').addEventListener('click', () => this.togglePlay());
        document.getElementById('next-btn').addEventListener('click', () => this.nextFrame());
        document.getElementById('last-btn').addEventListener('click', () => this.goToFrame(this.gameStates.length - 1));
        
        document.getElementById('frame-slider').addEventListener('input', (e) => {
            this.goToFrame(parseInt(e.target.value));
        });
        
        document.getElementById('speed-control').addEventListener('input', (e) => {
            this.fps = parseInt(e.target.value);
            document.getElementById('speed-value').textContent = `${this.fps} fps`;
            if (this.isPlaying) {
                this.stopPlay();
                this.startPlay();
            }
        });
    }
    
    async loadReplayList() {
        try {
            const response = await fetch('/api/replays');
            const replays = await response.json();
            const select = document.getElementById('replay-select');
            select.innerHTML = replays.map(r => `<option value="${r}">${r}</option>`).join('');
        } catch (error) {
            console.error('Error loading replay list:', error);
            document.getElementById('replay-select').innerHTML = '<option>Error loading replays</option>';
        }
    }
    
    async loadReplay() {
        const select = document.getElementById('replay-select');
        const replayFile = select.value;
        if (!replayFile) return;
        
        try {
            const response = await fetch(`/api/replay/${replayFile}`);
            this.replayData = await response.json();
            this.processReplay();
            this.enableControls();
            this.render();
        } catch (error) {
            console.error('Error loading replay:', error);
            alert('Error loading replay file');
        }
    }
    
    processReplay() {
        // Initialize game state
        const layout = this.replayData.layout;
        
        // Resize canvas based on layout
        this.canvas.width = layout.width * this.cellSize;
        this.canvas.height = layout.height * this.cellSize + 40; // Extra space for score
        
        // Build game states from actions
        this.gameStates = [];
        let state = this.createInitialState();
        this.gameStates.push(JSON.parse(JSON.stringify(state)));
        
        for (const [agentIndex, action] of this.replayData.actions) {
            state = this.applyAction(state, agentIndex, action);
            this.gameStates.push(JSON.parse(JSON.stringify(state)));
        }
        
        // Update UI
        document.getElementById('red-team-name').textContent = this.replayData.redTeamName;
        document.getElementById('blue-team-name').textContent = this.replayData.blueTeamName;
        document.getElementById('frame-slider').max = this.gameStates.length - 1;
        this.currentFrame = 0;
        this.updateFrameInfo();
    }
    
    createInitialState() {
        const layout = this.replayData.layout;
        const agents = [];
        
        // Find starting positions (scan for initial agent positions)
        // Red team starts on left side, blue on right
        let agentId = 0;
        for (let x = 0; x < layout.width; x++) {
            for (let y = 0; y < layout.height; y++) {
                if (!layout.walls[x][y] && layout.food[x][y] && agentId < 4) {
                    if ((x < layout.width / 2 && agentId < 2) || 
                        (x >= layout.width / 2 && agentId >= 2)) {
                        agents.push({
                            x: x,
                            y: y,
                            isPacman: x >= layout.width / 2 ? agentId < 2 : agentId >= 2,
                            team: agentId < 2 ? 'red' : 'blue',
                            scared: false
                        });
                        agentId++;
                    }
                }
            }
        }
        
        // If we didn't find 4 positions, create default ones
        while (agents.length < 4) {
            const team = agents.length < 2 ? 'red' : 'blue';
            const x = team === 'red' ? 1 : layout.width - 2;
            const y = 1 + agents.length;
            agents.push({
                x: x,
                y: y,
                isPacman: team === 'blue',
                team: team,
                scared: false
            });
        }
        
        return {
            agents: agents,
            food: JSON.parse(JSON.stringify(layout.food)),
            capsules: [...layout.capsules],
            redScore: 0,
            blueScore: 0
        };
    }
    
    applyAction(state, agentIndex, actionStr) {
        const newState = JSON.parse(JSON.stringify(state));
        const agent = newState.agents[agentIndex];
        
        // Parse action (North, South, East, West, Stop)
        const dx = { 'East': 1, 'West': -1, 'North': 0, 'South': 0, 'Stop': 0 }[actionStr] || 0;
        const dy = { 'East': 0, 'West': 0, 'North': -1, 'South': 1, 'Stop': 0 }[actionStr] || 0;
        
        const newX = agent.x + dx;
        const newY = agent.y + dy;
        
        // Check if valid move
        if (newX >= 0 && newX < this.replayData.layout.width && 
            newY >= 0 && newY < this.replayData.layout.height &&
            !this.replayData.layout.walls[newX][newY]) {
            agent.x = newX;
            agent.y = newY;
            
            // Check food eating
            if (newState.food[newX][newY]) {
                newState.food[newX][newY] = false;
                if (agent.team === 'red') newState.redScore++;
                else newState.blueScore++;
            }
            
            // Check capsule eating
            const capsuleIndex = newState.capsules.findIndex(c => c[0] === newX && c[1] === newY);
            if (capsuleIndex >= 0) {
                newState.capsules.splice(capsuleIndex, 1);
            }
        }
        
        return newState;
    }
    
    render() {
        const ctx = this.ctx;
        const state = this.gameStates[this.currentFrame];
        const layout = this.replayData.layout;
        
        // Clear canvas
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw walls
        ctx.fillStyle = '#0033ff';
        for (let x = 0; x < layout.width; x++) {
            for (let y = 0; y < layout.height; y++) {
                if (layout.walls[x][y]) {
                    ctx.fillRect(x * this.cellSize, y * this.cellSize, 
                               this.cellSize, this.cellSize);
                }
            }
        }
        
        // Draw food
        ctx.fillStyle = '#fff';
        for (let x = 0; x < layout.width; x++) {
            for (let y = 0; y < layout.height; y++) {
                if (state.food[x][y]) {
                    ctx.beginPath();
                    ctx.arc(x * this.cellSize + this.cellSize / 2, 
                          y * this.cellSize + this.cellSize / 2, 
                          2, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
        }
        
        // Draw capsules
        ctx.fillStyle = '#fff';
        for (const [cx, cy] of state.capsules) {
            ctx.beginPath();
            ctx.arc(cx * this.cellSize + this.cellSize / 2, 
                  cy * this.cellSize + this.cellSize / 2, 
                  5, 0, Math.PI * 2);
            ctx.fill();
        }
        
        // Draw center line
        ctx.strokeStyle = '#444';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(layout.width * this.cellSize / 2, 0);
        ctx.lineTo(layout.width * this.cellSize / 2, layout.height * this.cellSize);
        ctx.stroke();
        
        // Draw agents
        for (let i = 0; i < state.agents.length; i++) {
            const agent = state.agents[i];
            const color = agent.team === 'red' ? '#ff0000' : '#00aaff';
            
            ctx.fillStyle = color;
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 2;
            
            const cx = agent.x * this.cellSize + this.cellSize / 2;
            const cy = agent.y * this.cellSize + this.cellSize / 2;
            const radius = this.cellSize * 0.4;
            
            if (agent.isPacman) {
                // Draw Pacman
                ctx.beginPath();
                ctx.arc(cx, cy, radius, 0.2 * Math.PI, 1.8 * Math.PI);
                ctx.lineTo(cx, cy);
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
            } else {
                // Draw Ghost
                ctx.beginPath();
                ctx.arc(cx, cy - radius * 0.3, radius * 0.7, Math.PI, 0);
                ctx.lineTo(cx + radius * 0.7, cy + radius);
                ctx.lineTo(cx + radius * 0.4, cy + radius * 0.7);
                ctx.lineTo(cx, cy + radius);
                ctx.lineTo(cx - radius * 0.4, cy + radius * 0.7);
                ctx.lineTo(cx - radius * 0.7, cy + radius);
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
                
                // Eyes
                ctx.fillStyle = '#fff';
                ctx.beginPath();
                ctx.arc(cx - radius * 0.3, cy - radius * 0.2, radius * 0.2, 0, Math.PI * 2);
                ctx.arc(cx + radius * 0.3, cy - radius * 0.2, radius * 0.2, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        
        // Update score display
        document.getElementById('red-score').textContent = state.redScore;
        document.getElementById('blue-score').textContent = state.blueScore;
        
        this.updateFrameInfo();
    }
    
    updateFrameInfo() {
        document.getElementById('frame-info').textContent = 
            `${this.currentFrame} / ${this.gameStates.length - 1}`;
        document.getElementById('frame-slider').value = this.currentFrame;
        
        if (this.currentFrame === this.gameStates.length - 1) {
            const state = this.gameStates[this.currentFrame];
            const winner = state.redScore > state.blueScore ? 'Red' : 
                          state.blueScore > state.redScore ? 'Blue' : 'Tie';
            document.getElementById('game-status').textContent = `Game Over - ${winner} wins!`;
        } else {
            document.getElementById('game-status').textContent = `Playing...`;
        }
    }
    
    goToFrame(frame) {
        if (frame >= 0 && frame < this.gameStates.length) {
            this.currentFrame = frame;
            this.render();
        }
    }
    
    nextFrame() {
        if (this.currentFrame < this.gameStates.length - 1) {
            this.currentFrame++;
            this.render();
        } else {
            this.stopPlay();
        }
    }
    
    previousFrame() {
        if (this.currentFrame > 0) {
            this.currentFrame--;
            this.render();
        }
    }
    
    togglePlay() {
        if (this.isPlaying) {
            this.stopPlay();
        } else {
            this.startPlay();
        }
    }
    
    startPlay() {
        this.isPlaying = true;
        document.getElementById('play-btn').textContent = '⏸️ Pause';
        this.playInterval = setInterval(() => this.nextFrame(), 1000 / this.fps);
    }
    
    stopPlay() {
        this.isPlaying = false;
        document.getElementById('play-btn').textContent = '▶️ Play';
        if (this.playInterval) {
            clearInterval(this.playInterval);
            this.playInterval = null;
        }
    }
    
    enableControls() {
        document.getElementById('first-btn').disabled = false;
        document.getElementById('prev-btn').disabled = false;
        document.getElementById('play-btn').disabled = false;
        document.getElementById('next-btn').disabled = false;
        document.getElementById('last-btn').disabled = false;
        document.getElementById('frame-slider').disabled = false;
    }
}

// Initialize viewer when page loads
window.addEventListener('DOMContentLoaded', () => {
    new ReplayViewer();
});
