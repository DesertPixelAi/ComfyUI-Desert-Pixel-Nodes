import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { DPThemes } from "./dp_themes.js";

app.registerExtension({
    name: "dp.text.preview",
    async nodeCreated(node) {
        if (node.widgets) {
            const displayWidget = node.widgets.find(w => w.name === "display_text");
            if (displayWidget && displayWidget.inputEl) {
                displayWidget.inputEl.readOnly = true;
                displayWidget.inputEl.style.opacity = "1";
                displayWidget.inputEl.style.color = "#fff";
                displayWidget.inputEl.placeholder = "Preview will appear here...";
                displayWidget.inputEl.style.cursor = "default";
                displayWidget.inputEl.style.userSelect = "text";
                
                if (node.bgcolor) {
                    displayWidget.inputEl.style.backgroundColor = node.bgcolor;
                }
            }
        }
    },
    
    async setup() {
        api.addEventListener("execution_start", () => {
            for (const node of app.graph._nodes) {
                if (node.type === "DP_Text_Preview") {
                    const displayWidget = node.widgets?.find(w => w.name === "display_text");
                    if (displayWidget && displayWidget.inputEl) {
                        displayWidget.inputEl.readOnly = false;
                        if (node.bgcolor) {
                            displayWidget.inputEl.style.backgroundColor = node.bgcolor;
                        }
                    }
                }
            }
        });

        api.addEventListener("update_node", (event) => {
            const { node_id, widget_values } = event.detail;
            
            const node = app.graph._nodes_by_id[node_id];
            if (!node) return;
            
            if (widget_values && widget_values.display_text !== undefined) {
                const displayWidget = node.widgets?.find(w => w.name === "display_text");
                if (displayWidget && displayWidget.inputEl) {
                    displayWidget.value = widget_values.display_text;
                    displayWidget.inputEl.readOnly = true;
                    displayWidget.inputEl.style.opacity = "1";
                    displayWidget.inputEl.style.color = "#fff";
                    displayWidget.inputEl.style.cursor = "default";
                    displayWidget.inputEl.style.userSelect = "text";
                    
                    if (node.bgcolor) {
                        displayWidget.inputEl.style.backgroundColor = node.bgcolor;
                    }
                    
                    if (displayWidget.callback) {
                        displayWidget.callback(widget_values.display_text);
                    }
                }
            }
        });

        const originalGetExtraMenuOptions = LGraphNode.prototype.getExtraMenuOptions;
        LGraphNode.prototype.getExtraMenuOptions = function(_, options) {
            const result = originalGetExtraMenuOptions?.apply(this, arguments);
            
            if (this.type === "DP_Text_Preview") {
                const displayWidget = this.widgets?.find(w => w.name === "display_text");
                if (displayWidget && displayWidget.inputEl && this.bgcolor) {
                    displayWidget.inputEl.style.backgroundColor = this.bgcolor;
                }
            }
            
            return result;
        };
    }
});