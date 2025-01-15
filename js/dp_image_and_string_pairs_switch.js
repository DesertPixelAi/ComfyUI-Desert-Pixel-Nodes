import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "dp.image.and.string.pairs.switch",
    
    async nodeCreated(node) {
        if (node.comfyClass !== "DP_Image_And_String_Pairs_Switch") return;
    }
});

// Listen for pair updates from server
api.addEventListener("dp_pair_update", (event) => {
    const { node_id, index } = event.detail;
    
    const node = app.graph.getNodeById(node_id);
    if (!node) return;

    // Update index widget
    const indexWidget = node.widgets.find(w => w.name === "index");
    if (indexWidget) {
        indexWidget.value = index;
    }

    node.setDirtyCanvas(true);
}); 