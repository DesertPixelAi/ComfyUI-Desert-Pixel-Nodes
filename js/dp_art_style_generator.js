import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "dp.art.style.generator",

    async nodeCreated(node) {
        if (node.comfyClass !== "DP_Art_Style_Generator") return;

        // Store references to widgets
        const styleNameWidget = node.widgets.find(w => w.name === "style_name");
        const indexWidget = node.widgets.find(w => w.name === "index");
        const modeWidget = node.widgets.find(w => w.name === "style_index_control");

        if (!styleNameWidget || !indexWidget || !modeWidget) return;

        // Handle style name selection
        const originalStyleCallback = styleNameWidget.callback;
        styleNameWidget.callback = function (value) {
            if (value !== "None" && modeWidget.value === "fixed") {
                // Find index of selected style
                const styleIndex = styleNameWidget.options.findIndex(opt => opt === value);
                if (styleIndex >= 0) {
                    indexWidget.value = styleIndex;
                }
            }

            if (originalStyleCallback) {
                return originalStyleCallback.call(this, value);
            }
        };

        // Handle mode changes
        const originalModeCallback = modeWidget.callback;
        modeWidget.callback = function (value) {
            // When switching to fixed mode, update index based on current style
            if (value === "fixed" && styleNameWidget.value !== "None") {
                const styleIndex = styleNameWidget.options.findIndex(opt => opt === styleNameWidget.value);
                if (styleIndex >= 0) {
                    indexWidget.value = styleIndex;
                }
            }

            if (originalModeCallback) {
                return originalModeCallback.call(this, value);
            }
        };
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