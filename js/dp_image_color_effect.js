import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "dp_image_color_effect",
    
    async setup() {
        // Listen for node updates
        api.addEventListener("update_node", (event) => {
            const { node_id, random_value, color, index_value } = event.detail;
            
            // Find the node instance
            const node = app.graph._nodes_by_id[node_id];
            if (!node) return;
            
            // Update index widget if present
            if (index_value !== undefined) {
                const indexWidget = node.widgets?.find(w => w.name === "index");
                if (indexWidget) {
                    indexWidget.value = index_value;
                    if (indexWidget.callback) {
                        indexWidget.callback(index_value);
                    }
                    node.onWidgetChanged?.(indexWidget.name, indexWidget.value, index_value, indexWidget);
                }
            }
            
            // Update random_max widget
            const widget = node.widgets?.find(w => w.name === "random_max");
            if (widget) {
                widget.value = random_value;
                if (widget.callback) {
                    widget.callback(random_value);
                }
                // Force widget to update its value in the UI
                widget.value = random_value;
                
                // Trigger widget change event
                node.onWidgetChanged?.(widget.name, widget.value, random_value, widget);
            }
            
            // Update info widget
            const infoWidget = node.widgets?.find(w => w.name === "info");
            if (infoWidget && event.detail.info_text) {
                infoWidget.value = event.detail.info_text;
                if (infoWidget.callback) {
                    infoWidget.callback(infoWidget.value);
                }
                node.onWidgetChanged?.(infoWidget.name, infoWidget.value, infoWidget.value, infoWidget);
            }
            
            // Update node color
            if (color) {
                node.color = color;
                node.bgcolor = color;
            }
            
            // Force canvas update
            node.setDirtyCanvas(true, true);
            app.graph.setDirtyCanvas(true);
        });
    }
});