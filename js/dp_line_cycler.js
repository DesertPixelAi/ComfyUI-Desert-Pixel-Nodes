import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "dp.line.cycler",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "DP Line Cycler") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Handle WebSocket messages
                api.addEventListener("update_node", ({ detail }) => {
                    if (detail.node_id === this.id) {
                        const widget = this.widgets.find(w => w.name === "index");
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