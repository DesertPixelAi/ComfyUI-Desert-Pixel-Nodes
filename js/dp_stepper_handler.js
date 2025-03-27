import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "dp.stepper",
    async nodeCreated(node) {
        if (node.type === "DP_Lora_Strength_Stepper") {
            // Add current value widget if it doesn't exist
            const currentWidget = node.widgets?.find(w => w.name === "current");
            if (!currentWidget) {
                const widget = node.addWidget("number", "current", 1.2, null);
                widget.inputEl.readOnly = true;
                widget.inputEl.style.opacity = "0.7";
            }
        }
    },

    async setup() {
        // Handle theme updates for visual feedback
        api.addEventListener("update_theme", ({ detail }) => {
            const node = app.graph._nodes_by_id[detail.node_id];
            if (!node || node.type !== "DP_Lora_Strength_Stepper") return;

            // Update node colors
            if (detail.title_color) node.color = detail.title_color;
            if (detail.body_color) node.bgcolor = detail.body_color;

            // Reset colors after a delay
            setTimeout(() => {
                node.color = "#121317";
                node.bgcolor = "#006994";
                node.setDirtyCanvas(true, true);
            }, 200);

            node.setDirtyCanvas(true, true);
        });

        // Handle node updates
        api.addEventListener("update_node", ({ detail }) => {
            const node = app.graph._nodes_by_id[detail.node_id];
            if (!node || node.type !== "DP_Lora_Strength_Stepper") return;

            // Update current value if provided
            if (detail.widget_values?.current !== undefined) {
                const currentWidget = node.widgets?.find(w => w.name === "current");
                if (currentWidget) {
                    currentWidget.value = detail.widget_values.current;
                    node.setDirtyCanvas(true, true);
                }
            }
        });
    }
});