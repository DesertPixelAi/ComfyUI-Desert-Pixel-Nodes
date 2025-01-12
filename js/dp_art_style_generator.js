import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "dp.art.style.generator",
    
    async nodeCreated(node) {
        if (node.comfyClass !== "DP_Art_Style_Generator") return;

        // Handle widget changes
        node.widgets.forEach(widget => {
            const originalCallback = widget.callback;
            widget.callback = function(value) {
                if (widget.name === "style_name" && value !== "None") {
                    // Update index widget when style is selected manually
                    const indexWidget = node.widgets.find(w => w.name === "index");
                    if (indexWidget) {
                        // Find index of selected style in the widget's options
                        const styleIndex = widget.options.findIndex(opt => opt === value);
                        if (styleIndex > 0) {  // Ensure we don't select "None"
                            indexWidget.value = styleIndex;
                        }
                    }
                }

                if (originalCallback) {
                    return originalCallback.call(this, value);
                }
            };
        });
    }
});

// Listen for style updates from server
api.addEventListener("dp_style_update", (event) => {
    const { node_id, index, style_name } = event.detail;
    
    const node = app.graph.getNodeById(node_id);
    if (!node) return;

    // Update widgets
    node.widgets.forEach(widget => {
        if (widget.name === "index") {
            widget.value = index;
        } else if (widget.name === "style_name") {
            widget.value = style_name;
        }
    });

    node.setDirtyCanvas(true);
}); 