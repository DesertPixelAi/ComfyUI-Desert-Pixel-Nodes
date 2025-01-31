import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { DPThemes } from "./dp_themes.js";

api.addEventListener("update_node", ({ node_id, widget_name, value }) => {
    const node = app.graph.getNodeById(node_id);
    if (!node) return;

    // Store current theme
    const currentTheme = {
        color: node.color,
        bgcolor: node.bgcolor,
        properties: node.properties?._dpColors
    };

    // Find and update the widget
    const widget = node.widgets?.find(w => w.name === widget_name);
    if (widget) {
        widget.value = value;
        if (widget.callback) {
            widget.callback(value);
        }
    }

    // Restore theme
    node.color = currentTheme.color;
    node.bgcolor = currentTheme.bgcolor;
    if (currentTheme.properties) {
        node.properties = node.properties || {};
        node.properties._dpColors = currentTheme.properties;
    }
    
    node.setDirtyCanvas(true, true);
});

api.addEventListener("letter.update", ({ node: nodeId, index, letter, preserve_theme }) => {
    const node = app.graph.getNodeById(nodeId);
    if (!node) return;

    // Store current theme
    const currentTheme = {
        color: node.color,
        bgcolor: node.bgcolor,
        properties: node.properties?._dpColors
    };

    // Find index widget
    const indexWidget = node.widgets?.find(w => w.name === "index");
    if (indexWidget) {
        indexWidget.value = index;
        if (indexWidget.callback) {
            indexWidget.callback(index);
        }
    }

    // If preserve_theme is true, restore the theme
    if (preserve_theme) {
        node.color = currentTheme.color;
        node.bgcolor = currentTheme.bgcolor;
        if (currentTheme.properties) {
            node.properties = node.properties || {};
            node.properties._dpColors = currentTheme.properties;
        }
    }

    node.setDirtyCanvas(true, true);
});

api.addEventListener("dp_preserve_theme", ({ node_id }) => {
    const node = app.graph.getNodeById(node_id);
    if (!node) return;

    // Store current theme
    if (!node._preserved_theme) {
        node._preserved_theme = {
            color: node.color,
            bgcolor: node.bgcolor,
            properties: node.properties?._dpColors
        };
    }

    // Restore theme after execution
    const onExecuted = () => {
        if (node._preserved_theme) {
            node.color = node._preserved_theme.color;
            node.bgcolor = node._preserved_theme.bgcolor;
            if (node._preserved_theme.properties) {
                node.properties = node.properties || {};
                node.properties._dpColors = node._preserved_theme.properties;
            }
            node.setDirtyCanvas(true, true);
            delete node._preserved_theme;
        }
        app.removeEventListener("executed", onExecuted);
    };

    app.addEventListener("executed", onExecuted);
});

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
        app.graph.onNodeAdded = function(node) {
            if (isDPNode(node)) {
                // Only add icon if needed
                if (!node.title.match(/^[🐵🦧🐶🦖🐞🐢🦆🐸🐠💎✨🌞🐌🍬🍫🧁🍉🍄🧨⚡🌟⭐🌞🌝🛸🚀👽👾🤖💀👊🤘🤙👌🖖💋🙈🙉🙊]/)) {
                    const icon = DPThemes.getRandomIcon();
                    node.title = icon + node.title;
                }

                // Only apply specific theme if colors haven't been set before
                if (!node.properties?._dpColors) {
                    const nodeSpecificTheme = DPThemes.getNodeSpecificTheme(node.comfyClass);
                    if (nodeSpecificTheme) {
                        node.color = nodeSpecificTheme.title;
                        node.bgcolor = nodeSpecificTheme.body;
                        node.properties = node.properties || {};
                        node.properties._dpColors = nodeSpecificTheme;
                    } else {
                        const colors = DPThemes.getThemeColors(DPThemes.defaultTheme);
                        node.color = colors.title;
                        node.bgcolor = colors.body;
                        node.properties = node.properties || {};
                        node.properties._dpColors = colors;
                    }
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

        // Add this new event listener
        api.addEventListener("update_index", ({ node: nodeId, index, preserve_state }) => {
            const node = app.graph.getNodeById(nodeId);
            if (!node) return;

            // Find the index widget
            const widget = node.widgets?.find(w => w.name === "index");
            if (!widget) return;

            // Store current state
            const currentState = {
                color: node.color,
                bgcolor: node.bgcolor,
                properties: node.properties?._dpColors
            };

            // Update the widget value
            widget.value = index;
            
            // If preserve_state is true, restore the state
            if (preserve_state) {
                node.color = currentState.color;
                node.bgcolor = currentState.bgcolor;
                if (currentState.properties) {
                    node.properties = node.properties || {};
                    node.properties._dpColors = currentState.properties;
                }
            }
            
            widget.callback?.(index);
            node.setDirtyCanvas(true, true);
        });
    }
});

app.registerExtension({
    name: "DP.BigLetterAdvanced",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "DP Big Letter Advanced") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);
                
                // Find the cycle mode and index widgets
                const cycleModeWidget = this.widgets?.find(w => w.name === "cycle_mode");
                const indexWidget = this.widgets?.find(w => w.name === "index");
                
                if (cycleModeWidget && indexWidget) {
                    // Store original callback
                    const originalCallback = indexWidget.callback;
                    
                    // Override callback to handle both value change and theme preservation
                    indexWidget.callback = function(value) {
                        if (originalCallback) {
                            originalCallback(value);
                        }
                        
                        // Update the display
                        this.value = value;
                        node.setDirtyCanvas(true, true);
                    };
                }
                
                return r;
            };
        }
    }
});