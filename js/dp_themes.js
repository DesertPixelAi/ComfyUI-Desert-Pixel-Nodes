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

    // Add specific node themes using theme names
    nodeSpecificThemes: {
        "DP_Load_Image_Minimal": "black",
        "DP Save Preview Image": "obsidian",
        "DP Image Color Analyzer": "deep_purple",
        "DP Load Image Effects": "black",
        "DP Load Image Effects Small": "black",
        "DP Image Effect Processor": "black",
        "DP Five Lora": "deep_purple",
        "DP Lora Strength Controller": "deep_purple",
        "DP Five Lora Random": "purple",
        "DP Lora Random Strength Controller": "purple",
    },

    // Add method to get theme colors from name
    getNodeSpecificTheme(nodeName) {
        const themeName = this.nodeSpecificThemes[nodeName];
        if (!themeName) return null;
        
        // If the theme name exists in our themes, use it
        if (this.themes[themeName]) {
            return this.themes[themeName];
        }
        // If it's a direct color object, return it (for backward compatibility)
        if (typeof themeName === 'object') {
            return themeName;
        }
        return null;
    },

    // Add this to the DPThemes object
    dpNodeTypes: [
        "DP Animation Calculator 5 Inputs",
        "DP Animation Calculator 10 Inputs",
        "DP Transition Frames Selector",
        "DP Diff Int 8step Selector",
        "DP Draggable Int 1step",
        "DP Draggable Int 4step",
        "DP Draggable Int 8step",
        "DP Big Letters",
        "DP Broken Token",
        "DP Clean Prompt",
        "DP Clean Prompt Travel",
        "DP Create Json File",
        "DP Random Crazy Prompt Generator",
        "DP Draggable Floats 1",
        "DP Draggable Floats 2",
        "DP Draggable Floats 3",
        "DP Fast Slow Motion",
        "DP Five Lora",
        "DP Five Lora Random",
        "DP Image Color Analyzer",
        "DP Image Color Analyzer Small",
        "DP Image Color Effect",
        "DP Image Effect Processor",
        "DP Image Effect Processor Small",
        "DP Image Empty Latent Switch Flux",
        "DP Image Empty Latent Switch SDXL",
        "DP Image Slide Show",
        "DP Image Strip",
        "DP Strip Edge Masks",
        "DP Load Image Effects",
        "DP Load Image Effects Small",
        "DP Load Image Minimal",
        "DP Logo Animator",
        "DP Lora Strength Controller",
        "DP Lora Random Strength Controller",
        "DP Prompt Styler",
        "DP Prompt Manager Small",
        "DP Prompt Mode Controller",
        "DP Set New Model Folder Link",
        "DP Random Character",
        "DP Random Min Max",
        "DP Save Preview Image",
        "DP Aspect Ratio Picker",
        "DP Custom Aspect Ratio",
        "DP String Text",
        "DP String Text With Sdxl Weight",
        "DP 2 String Switch",
        "DP Switch Controller",
        "DP Text Preview",
        "DP Video Effect Sender",
        "DP Video Effect Receiver",
        "DP Video Flicker",
        "DP Video Looper",
        "DP Video Transition",
        "DP Prompt Token Compressor",
        "DP Random Logo Style Generator",
        "DP Random Superhero Prompt Generator",
        "DP Random Psychedelic Punk Generator",
        "DP Crazy Prompt Mixer",
        "DP Prompt Inverter",
        "DP Random Mode Switch",
        "DP Random Mode Controller",
        "DP Image And String Pairs Switch",
        "DP Art Style Generator",
        "DP Add Weight To String Sdxl",
        "DP Advanced Weight String Sdxl",
        "DP Random Vehicle Generator",
        "DP Line Cycler",
        "DP 5 Find And Replace",
        "DP Mask Settings",
        "DP Sampler With Info",
        "DP ControlNet Apply Advanced",
        "DP Load Controlnet Model With Name",
        "DP Load Checkpoint With Info",
        "DP Load UNET With Info",
        "DP Load Dual CLIP With Info",
        "DP Add Background To Png",
        "DP 10 Images Switch Or Batch",
        "DP 3 Images Switch Or Batch",
        "DP 5 Images Switch Or Batch",
        "DP Latent Split",
        "DP Condition Switch",
        "DP 10 String Switch Or Connect",
        "DP 3 String Switch Or Connect",
        "DP 5 String Switch Or Connect",
        "DP Advanced Sampler",
        "DP Float Stepper",
        "DP Prompt Travel Prompt"
    ]
};