import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

// Centralized theme configuration
export const DPThemes = {
    // Common color palette for both title and body
    colors: {
        dark_gray: "#121317",
        charcoal: "#1a1a1d",
        navy_blue: "#191970",
        ocean_blue: "#006994",
        royal_blue: "#4169e1",
        purple: "#800080",
        deep_purple: "#483d8b",
        indigo: "#4b0082",
        dark_blue: "#182f41",
        bright_red: "#cc0000",
        burgundy: "#800020",
        wine_red: "#722f37",
        mahogany: "#c04000",
        orange: "#ff6600",
        golden: "#ffd700",
        forest_green: "#228b22",
        emerald: "#50c878",
        olive: "#556b2f",
        teal: "#008080",
        slate_gray: "#708090",
        graphite: "#383838",
        ice_blue: "#a5c9ca",
        obsidian: "#1d1e1e"
    },

    // Theme combinations
    themes: {
        "dp_ocean": { title: "#121317", body: "#006994" },
        "black": { title: "#1a1a1d", body: "#121317" },
        "purple": { title: "#121317", body: "#800080" },
        "royal_blue": { title: "#121317", body: "#4169e1" },
        "forest": { title: "#121317", body: "#228b22" },
        "bright_red": { title: "#121317", body: "#cc0000" },
        "orange": { title: "#121317", body: "#ff6600" },
        "golden": { title: "#121317", body: "#ffd700" },
        "midnight": { title: "#121317", body: "#191970" },
        "burgundy": { title: "#121317", body: "#800020" },
        "deep_purple": { title: "#121317", body: "#483d8b" },
        "charcoal": { title: "#121317", body: "#36454f" },
        "emerald": { title: "#121317", body: "#50c878" },
        "slate": { title: "#121317", body: "#708090" },
        "wine": { title: "#121317", body: "#722f37" },
        "teal": { title: "#121317", body: "#008080" },
        "indigo": { title: "#121317", body: "#4b0082" },
        "graphite": { title: "#121317", body: "#383838" },
        "ice": { title: "#121317", body: "#a5c9ca" },
        "mahogany": { title: "#121317", body: "#c04000" },
        "obsidian": { title: "#121317", body: "#1d1e1e" },
        "olive": { title: "#121317", body: "#556b2f" }
    },

    // Get theme colors
    getThemeColors(themeName) {
        return this.themes[themeName] || this.themes[this.defaultTheme];
    },

    // Extract unique title colors
    getTitleColors() {
        return Object.entries(this.colors).map(([name, color]) => ({
            content: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            value: color
        }));
    },

    // Extract unique body colors
    getBodyColors() {
        return Object.entries(this.colors).map(([name, color]) => ({
            content: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            value: color
        }));
    },

    // Rest of the existing code...
    defaultTheme: "dp_ocean",
    nodeIcons: {
        default: "🌵 ",
    },
    iconList: ["🐵 ", "🦧 ", "🐶 ", "🦖 ", "🐞 ", "🐢 ", "🦆 ", "🐸 ", "🐠 ", "💎 ", "✨ ", "🌞 ", "🐌 ", 
               "🍬 ", "🍫 ", "🧁 ", "🍉 ", "🍄 ", "🧨 ", "⚡ ", "🌟 ", "⭐ ", "🌞 ", "🌝 ", "🛸 ", "🚀 ", 
               "👽 ", "👾 ", "🤖 ", "💀 ", "👊 ", "🤘 ", "🤙 ", "👌 ", "🖖 ", "💋 ", "🙈 ", "🙉 ", "🙊 "],

    getRandomIcon() {
        const randomIndex = Math.floor(Math.random() * this.iconList.length);
        return this.iconList[randomIndex];
    },
    
    getNodeTitle(title) {
        const hasIcon = this.iconList.some(icon => title.startsWith(icon.trim()));
        if (hasIcon) {
            return title;
        }
        const icon = this.getRandomIcon();
        return icon + title;
    },

    // Add default ComfyUI colors
    defaultComfyColors: {
        title: "#355",    // Default ComfyUI title color
        body: "#233"      // Default ComfyUI body color
    },

    // Add method to get ComfyUI's current default node colors
    getCurrentDefaultColors() {
        // Try to get user's default theme first
        const userDefault = this.loadUserDefault();
        if (userDefault) {
            return userDefault;
        }
        // Otherwise return ComfyUI default colors
        return this.defaultComfyColors;
    },

    // Enhanced save method to handle both preset themes and custom colors
    saveAsDefault(colors, themeName = null) {
        try {
            const themeData = {
                colors: colors,
                themeName: themeName
            };
            localStorage.setItem('dp_default_theme', JSON.stringify(themeData));
        } catch (e) {
            console.warn("Could not save default theme");
        }
    },

    loadUserDefault() {
        try {
            const saved = localStorage.getItem('dp_default_theme');
            if (!saved) return this.themes[this.defaultTheme];
            
            const themeData = JSON.parse(saved);
            return themeData.colors || this.themes[this.defaultTheme];
        } catch (e) {
            console.warn("Could not load default theme");
            return this.themes[this.defaultTheme];
        }
    },

    // Method to reset nodes to their appropriate defaults
    getDefaultColorsForNode(node) {
        // Check for node-specific theme first
        if (this.nodeSpecificThemes[node.comfyClass]) {
            return this.nodeSpecificThemes[node.comfyClass];
        }
        // Fall back to regular theme selection
        if (node.comfyClass?.startsWith("DP_")) {
            return this.themes[this.defaultTheme];
        }
        return this.defaultComfyColors;
    },

    // Simplified save/load for favorite themes
    saveFavoriteTheme(colors, name = "My Favorite") {
        try {
            const favorite = {
                name: name,
                colors: colors
            };
            localStorage.setItem('dp_favorite_theme', JSON.stringify(favorite));
        } catch (e) {
            console.warn("Could not save favorite theme");
        }
    },

    loadFavoriteTheme() {
        try {
            const saved = localStorage.getItem('dp_favorite_theme');
            return saved ? JSON.parse(saved) : null;
        } catch (e) {
            console.warn("Could not load favorite theme");
            return null;
        }
    },

    // Add storage key for node states
    nodeStateKey: "dp_node_states",

    // Add methods to manage node states
    loadNodeStates() {
        try {
            const saved = localStorage.getItem(this.nodeStateKey);
            return saved ? JSON.parse(saved) : {};
        } catch (e) {
            console.warn("Could not load node states");
            return {};
        }
    },

    saveNodeStates(states) {
        try {
            localStorage.setItem(this.nodeStateKey, JSON.stringify(states));
        } catch (e) {
            console.warn("Could not save node states");
        }
    },

    // Add specific node themes
    nodeSpecificThemes: {
        "DP Save Preview Image": { title: "#121317", body: "#1d1e1e" }  // Using obsidian theme colors
    },

    // Add this to the DPThemes object
    dpNodeTypes: [
        "DP Animation Calculator 5 Inputs",
        "DP Transition Frames Selector",
        "DP Diff Int 8step Selector",
        "DP Big Letters",
        "DP Broken Token",
        "DP Clean Prompt",
        "DP Combo Controller",
        "DP Create Json File",
        "DP Random Crazy Prompt Generator",
        "DP Draggable Floats 1",
        "DP Draggable Floats 2",
        "DP Draggable Floats 3",
        "DP Draggable Floats 5",
        "DP Fast Slow Motion",
        "DP Five Lora",
        "DP Five Lora Random",
        "DP Image Color Analyzer",
        "DP Image Color Effect",
        "DP Image Effect Processor",
        "DP Image Empty Latent Switch Flux",
        "DP Image Empty Latent Switch SDXL",
        "DP Image Slide Show",
        "DP Load Image Effects",
        "DP Load Image Effects Small",
        "DP Logo Animator",
        "DP Logo Animator Advanced",
        "DP Lora Strength Controller",
        "DP Lora Random Strength Controller",
        "DP Prompt Styler",
        "DP My Prompt Manager",
        "DP Prompt Mode Controller",
        "DP Set New Model Folder Link",
        "DP Random Character",
        "DP Random Min Max",
        "DP Save Preview Image",
        "DP Aspect Ratio Picker",
        "DP String With Switch",
        "DP 2 String Switch",
        "DP String Text",
        "DP Switch Controller",
        "DP Text Preview",
        "DP Video Effect Sender",
        "DP Video Effect Receiver",
        "DP Video Flicker",
        "DP Video Looper",
        "DP Video Transition",
        "DP Animation Calculator 10 Inputs"
    ]
};

// Keep the icon handling
const origDrawNode = LGraphCanvas.prototype.drawNode;
LGraphCanvas.prototype.drawNode = function(node, ctx) {
    // Check for node-specific theme first
    const nodeSpecificTheme = DPThemes.nodeSpecificThemes[node.comfyClass];
    if (nodeSpecificTheme) {
        node.color = nodeSpecificTheme.title;
        node.bgcolor = nodeSpecificTheme.body;
        node.properties = node.properties || {};
        node.properties._dpColors = nodeSpecificTheme;
    }
    return origDrawNode.apply(this, arguments);
};