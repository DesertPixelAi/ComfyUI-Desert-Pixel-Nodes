import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { DPThemes } from "./dp_themes.js";

function isDPNode(node) {
    if (!node || !node.comfyClass) return false;
    
    return node.comfyClass.startsWith("DP_") || 
           node.comfyClass.startsWith("DP ") ||
           (node.title && node.title.replace(/^[🐵🦧🐶🦖🐞🐢🦆🐸🐠💎✨🌞🐌🍬🍫🧁🍉🍄🧨⚡🌟⭐🌞🌝🛸🚀👽👾🤖💀👊🤘🤙👌🖖💋🙈🙉🙊]\s*/, '').startsWith("DP "));
}

function addThemeMenuToNode(node) {
    if (node._dpThemeMenuAdded) return;
    node._dpThemeMenuAdded = true;

    const originalGetExtraMenuOptions = node.getExtraMenuOptions;
    node.getExtraMenuOptions = function(_, options) {
        if (originalGetExtraMenuOptions) {
            originalGetExtraMenuOptions.call(this, _, options);
        }
        
        options.push(null);
        options.push({
            content: "DP Color Themes",
            has_submenu: true,
            callback: (value, options, e, menu, node) => {
                const submenu = new LiteGraph.ContextMenu(
                    [
                        {
                            content: "Preset Themes",
                            has_submenu: true,
                            callback: (value, options, e, menu) => {
                                new LiteGraph.ContextMenu(
                                    Object.keys(DPThemes.themes),
                                    {
                                        event: e,
                                        callback: (theme) => {
                                            const colors = DPThemes.getThemeColors(theme);
                                            node.color = colors.title;
                                            node.bgcolor = colors.body;
                                            node.properties = node.properties || {};
                                            node.properties._dpColors = colors;
                                            node.setDirtyCanvas(true, true);
                                        },
                                        parentMenu: menu,
                                        node: node
                                    }
                                );
                            }
                        },
                        {
                            content: "Title Color",
                            has_submenu: true,
                            callback: (value, options, e, menu) => {
                                new LiteGraph.ContextMenu(
                                    DPThemes.getTitleColors(),
                                    {
                                        event: e,
                                        callback: (item) => {
                                            node.color = item.value;
                                            node.properties = node.properties || {};
                                            node.properties._dpColors = {
                                                title: item.value,
                                                body: node.bgcolor
                                            };
                                            node.setDirtyCanvas(true, true);
                                        },
                                        parentMenu: menu,
                                        node: node
                                    }
                                );
                            }
                        },
                        {
                            content: "Body Color",
                            has_submenu: true,
                            callback: (value, options, e, menu) => {
                                new LiteGraph.ContextMenu(
                                    DPThemes.getBodyColors(),
                                    {
                                        event: e,
                                        callback: (item) => {
                                            node.bgcolor = item.value;
                                            node.properties = node.properties || {};
                                            node.properties._dpColors = {
                                                title: node.color,
                                                body: item.value
                                            };
                                            node.setDirtyCanvas(true, true);
                                        },
                                        parentMenu: menu,
                                        node: node
                                    }
                                );
                            }
                        },
                        null,
                        {
                            content: "Save As Favorite",
                            callback: () => {
                                const currentTheme = {
                                    title: node.color || "#121317",
                                    body: node.bgcolor || "#006994"
                                };
                                DPThemes.saveFavoriteTheme(currentTheme);
                                alert("Theme saved as favorite! 🎨");
                            }
                        },
                        {
                            content: "Apply Favorite Theme",
                            callback: () => {
                                const favorite = DPThemes.loadFavoriteTheme();
                                if (favorite && favorite.colors) {
                                    node.color = favorite.colors.title;
                                    node.bgcolor = favorite.colors.body;
                                    node.properties = node.properties || {};
                                    node.properties._dpColors = favorite.colors;
                                    node.setDirtyCanvas(true, true);
                                } else {
                                    alert("No favorite theme saved yet");
                                }
                            }
                        },
                        {
                            content: "Reset to Default",
                            callback: () => {
                                const colors = DPThemes.getThemeColors(DPThemes.defaultTheme);
                                node.color = colors.title;
                                node.bgcolor = colors.body;
                                node.properties = node.properties || {};
                                node.properties._dpColors = colors;
                                node.setDirtyCanvas(true, true);
                            }
                        }
                    ],
                    {
                        event: e,
                        parentMenu: menu,
                        node: node
                    }
                );
            }
        });
    };
}

app.registerExtension({
    name: "DP.ThemeHandler",
    async setup() {
        // Ensure theme menu is added after graph is loaded
        app.graph.onNodeAdded = function(node) {
            // Apply default theme only to DP nodes
            if (isDPNode(node)) {
                // Only add icon if the title doesn't already have one
                if (!node.title.match(/^[🐵🦧🐶🦖🐞🐢🦆🐸🐠💎✨🌞🐌🍬🍫🧁🍉🍄🧨⚡🌟⭐🌞🌝🛸🚀👽👾🤖💀👊🤘🤙👌🖖💋🙈🙉🙊]/)) {
                    const icon = DPThemes.getRandomIcon();
                    node.title = icon + node.title;
                }

                // Check for node-specific theme first
                const nodeSpecificTheme = DPThemes.nodeSpecificThemes[node.comfyClass];
                if (nodeSpecificTheme) {
                    node.color = nodeSpecificTheme.title;
                    node.bgcolor = nodeSpecificTheme.body;
                    node.properties = node.properties || {};
                    node.properties._dpColors = nodeSpecificTheme;
                } else if (node.properties?._dpColors) {
                    node.color = node.properties._dpColors.title;
                    node.bgcolor = node.properties._dpColors.body;
                } else {
                    const colors = DPThemes.getThemeColors(DPThemes.defaultTheme);
                    node.color = colors.title;
                    node.bgcolor = colors.body;
                    node.properties = node.properties || {};
                    node.properties._dpColors = colors;
                }
            }
            // Add theme menu to ALL nodes
            addThemeMenuToNode(node);
        };

        // Add menu to existing nodes after refresh
        const graphLoaded = () => {
            app.graph._nodes.forEach(node => {
                // Add theme menu to ALL nodes
                addThemeMenuToNode(node);
                
                // But only restore DP colors for DP nodes
                if (isDPNode(node)) {
                    // Only add icon if the title doesn't already have one
                    if (!node.title.match(/^[🐵🦧🐶🦖🐞🐢🦆🐸🐠💎✨🌞🐌🍬🍫🧁🍉🍄🧨⚡🌟⭐🌞🌝🛸🚀👽👾🤖💀👊🤘🤙👌🖖💋🙈🙉🙊]/)) {
                        const icon = DPThemes.getRandomIcon();
                        node.title = icon + node.title;
                    }
                    
                    if (node.properties?._dpColors) {
                        node.color = node.properties._dpColors.title;
                        node.bgcolor = node.properties._dpColors.body;
                    }
                }
            });
        };

        // Listen for graph load events
        api.addEventListener("graphLoaded", graphLoaded);
        
        // Also handle initial load
        if (app.graph._nodes.length > 0) {
            graphLoaded();
        }

        // Handle node serialization
        const origSerialize = LGraphNode.prototype.serialize;
        LGraphNode.prototype.serialize = function() {
            const data = origSerialize.call(this);
            if (this.properties?._dpColors) {
                data.properties = data.properties || {};
                data.properties._dpColors = this.properties._dpColors;
            }
            return data;
        };
    }
});