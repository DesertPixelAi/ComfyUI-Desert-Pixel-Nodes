import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "dp.line.cycler",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "DP Line Cycler") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Handle WebSocket messages
                api.addEventListener("update_line_cycler", ({ detail }) => {
                    if (detail.node_id === this.id) {
                        const widget = this.widgets.find(w => w.name === "Line_Index");
                        if (widget) {
                            widget.value = detail.index_value;
                            widget.callback(widget.value);
                        }
                    }
                });
                
                return result;
            };
        }
    }
}); 