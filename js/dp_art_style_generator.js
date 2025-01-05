import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "dp.art.style.generator",
    async setup() {
        // Store queued values for each node
        const queuedValues = new Map();

        // Handle style updates
        api.addEventListener("update_art_style", ({ detail }) => {
            const node = app.graph._nodes_by_id[detail.node_id];
            if (!node) return;

            // Store values for queuing
            if (!queuedValues.has(node.id)) {
                queuedValues.set(node.id, []);
            }
            queuedValues.get(node.id).push({
                style_name: detail.style_name,
                index: detail.index,
                color: detail.color,
                bgcolor: detail.bgcolor
            });

            // Update widgets only if not queuing
            if (!app.ui.isQueueing) {
                updateNodeUI(node, detail);
            }
        });

        // Function to update node UI
        function updateNodeUI(node, values) {
            const styleNameWidget = node.widgets.find(w => w.name === "style_name");
            const indexWidget = node.widgets.find(w => w.name === "index");
            
            if (styleNameWidget) {
                styleNameWidget.value = values.style_name;
            }
            
            if (indexWidget) {
                indexWidget.value = values.index;
                if (indexWidget.callback) {
                    indexWidget.callback(values.index);
                }
            }

            // Update node colors
            if (values.color) node.color = values.color;
            if (values.bgcolor) node.bgcolor = values.bgcolor;

            node.setDirtyCanvas(true);
        }

        // Add widget callbacks
        const onNodeCreated = (node) => {
            if (node.comfyClass !== "DP Art Style Generator") return;

            // Add callback for index changes
            const indexWidget = node.widgets.find(w => w.name === "index");
            if (indexWidget) {
                indexWidget.callback = (value) => {
                    node.widgets_values[node.widgets.indexOf(indexWidget)] = value;
                    // Trigger node update on index change
                    app.graph.setDirtyCanvas(true);
                };
            }
        };

        // Register node creation callback
        app.registerExtension({
            name: "dp.art.style.generator.node",
            nodeCreated: onNodeCreated
        });

        // Handle queue start
        app.addEventListener("queue", () => {
            // Reset queued values
            queuedValues.clear();
        });

        // Handle before prompt execution
        app.addEventListener("execution_start", (data) => {
            // Update UI with next queued value if available
            for (const [nodeId, values] of queuedValues.entries()) {
                const node = app.graph._nodes_by_id[nodeId];
                if (node && values.length > 0) {
                    const nextValue = values.shift();
                    updateNodeUI(node, nextValue);
                }
            }
        });
    }
}); 