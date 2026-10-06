"""Browser widget that runs the published ChessFly network.

The connectome and FlyNet weights stay on the author's site. The browser
runs the network and sends the readout activity back to Python. This module
does not train the student's scorer.
"""

from __future__ import annotations

import base64

import anywidget
import numpy as np
import traitlets

from fly_scorer import READOUT


class FlyNetwork(anywidget.AnyWidget):
    """Load the real fly network and hold the activity matrix Python can read."""

    _css = """
    .fly-box button { margin: 0 8px 8px 0; }
    .fly-box pre { white-space: pre-wrap; }
    """
    _esm = r"""
    function render({ model, el }) {
      const BASE = "https://mlabonne-chessfly.static.hf.space/";
      el.innerHTML = `
        <div class="fly-box">
          <p>The connectome runs in this browser. Python receives the activity after the run finishes.</p>
          <button id="btn-load" type="button">Load the real network</button>
          <button id="btn-ablate" type="button" hidden>Turn off the first 2,000,000 connections in stored order</button>
          <button id="btn-restore" type="button" hidden>Restore the first 2,000,000 connections in stored order</button>
          <pre id="status"></pre>
        </div>`;
      const statusEl = el.querySelector("#status");
      statusEl.textContent = model.get("status") || "";
      let worker = null;
      let busy = false;
      let graph = "intact";
      const pending = new Map();

      function setStatus(text) {
        statusEl.textContent = text;
        model.set("status", text);
        model.save_changes();
      }
      model.on("change:status", () => {
        const text = model.get("status") || "";
        if (text && text !== statusEl.textContent) statusEl.textContent = text;
      });
      function showAblation() {
        const show = Boolean(model.get("show_ablation"));
        el.querySelector("#btn-ablate").hidden = !show;
        el.querySelector("#btn-restore").hidden = !show;
      }
      showAblation();
      model.on("change:show_ablation", showAblation);

      function mustReplace(src, oldStr, newStr, label) {
        const count = src.split(oldStr).length - 1;
        if (count !== 1) {
          throw new Error(
            "The published worker no longer has the expected code at " + label +
            " (found " + count + "). This notebook will not substitute a different network."
          );
        }
        return src.replace(oldStr, newStr);
      }
      function encodeActivity(matrix) {
        const bytes = new Uint8Array(matrix.buffer, matrix.byteOffset, matrix.byteLength);
        let text = "";
        const chunk = 8192;
        for (let i = 0; i < bytes.length; i += chunk) {
          text += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
        }
        return btoa(text);
      }
      function send(name, extra) {
        const event = Object.assign({
          id: Date.now() + Math.random(),
          name,
          graph,
        }, extra || {});
        model.set("event", event);
        model.save_changes();
      }
      function setBusy(value) {
        busy = value;
        el.querySelectorAll("button").forEach((button) => { button.disabled = value; });
        if (!value) {
          const loaded = Boolean(worker);
          el.querySelector("#btn-load").disabled = false;
          el.querySelector("#btn-ablate").disabled = !loaded || graph !== "intact";
          el.querySelector("#btn-restore").disabled = !loaded || graph !== "ablated";
        }
      }

      el.querySelector("#btn-load").onclick = () => runLoad();
      el.querySelector("#btn-ablate").onclick = () => runGraph("ablate");
      el.querySelector("#btn-restore").onclick = () => runGraph("restore");

      async function runLoad() {
        if (busy) return;
        setBusy(true);
        setStatus("Loading the published connectome and FlyNet weights in the browser (about 148 MB)...");
        try {
          if (worker) worker.terminate();
          const indexHtml = await (await fetch(BASE + "index.html")).text();
          const bundle = indexHtml.match(/assets\/(index-[A-Za-z0-9_-]+\.js)/);
          if (!bundle) throw new Error("app bundle not found");
          const bundleText = await (await fetch(BASE + "assets/" + bundle[1])).text();
          const workerName = bundleText.match(/worker-[A-Za-z0-9_-]+\.js/);
          if (!workerName) throw new Error("worker script not found");
          let src = await (await fetch(BASE + "assets/" + workerName[0])).text();
          src = mustReplace(src, 'try{G=await H.create(T,j)}catch(c){console.warn("[fly] WebGPU unavailable, using the JS backend:",c),G=null}', "G=null;", "force-js");
          src = mustReplace(src, "return{...J(r,M,e),activity:t?h:void 0}", "const __R=n.readout,__rd=new Float32Array(e*__R.length);for(let __p=0;__p<__R.length;__p++){const __s=__R[__p]*e;for(let __i=0;__i<e;__i++)__rd[__i*__R.length+__p]=f[__s+__i]}return{...J(r,M,e),activity:t?h:void 0,readout:__rd}", "readout");
          src = mustReplace(src, "return{winprob:u,candidates:f,activity:e.wantActivity&&a===0?t.activity:void 0}", "return{winprob:u,candidates:f,activity:void 0,readout:t.readout?Array.from(t.readout.subarray(a*(t.readout.length/r.length),(a+1)*(t.readout.length/r.length))):null}", "surface");
          src = mustReplace(src, '))}}catch(r){O({type:"error",message:String(r?.message??r)})}};', '))}else if(n.type==="ablate"){if(!T)throw new Error("fly not loaded");const k=Math.max(0,Math.min(n.count|0,T.weight.length));self.__slice=T.weight.slice(0,k);T.weight.fill(0,0,k);O({type:"ablated",count:k})}else if(n.type==="restore"){if(!self.__slice)throw new Error("nothing to restore");T.weight.set(self.__slice,0);const k=self.__slice.length;self.__slice=null;O({type:"restored",count:k})}}catch(r){O({type:"error",message:String(r?.message??r)})}};', "ablate");
          worker = new Worker(URL.createObjectURL(new Blob([src], {type: "text/javascript"})));
          worker.onmessage = (ev) => {
            const msg = ev.data;
            const reply = msg.type === "ready" ? pending.get("init")
              : msg.type === "evaluated" ? pending.get(msg.id)
              : (msg.type === "ablated" || msg.type === "restored") ? pending.get(msg.type)
              : msg.type === "error" ? pending.get("error")
              : null;
            if (!reply) return;
            if (msg.type === "error") reply(new Error(msg.message));
            else reply(msg);
          };
          worker.onerror = (err) => {
            const fail = pending.get("error");
            if (fail) fail(new Error(err.message || String(err)));
          };
          const ready = new Promise((resolve, reject) => {
            pending.set("init", resolve);
            pending.set("error", reject);
          });
          const t0 = performance.now();
          worker.postMessage({type: "init", base: BASE + "data/"});
          const readyMsg = await ready;
          graph = "intact";
          const pack = await evaluateAll();
          await publishChunks(pack, "loaded", {
            load_s: (performance.now() - t0) / 1000,
            backend: readyMsg.backend,
            neurons: readyMsg.meta.neurons,
            edges: readyMsg.meta.edges,
          });
        } catch (err) {
          setStatus("Stopped: " + err.message);
          worker = null;
        } finally {
          setBusy(false);
        }
      }

      async function evaluateAll() {
        const positions = model.get("positions") || [];
        const blocks = [];
        const fly = [];
        for (let index = 0; index < positions.length; index++) {
          const position = positions[index];
          setStatus("Browser is running position " + (index + 1) + " of " + positions.length + "...");
          const id = "e" + Math.random();
          const done = new Promise((resolve, reject) => {
            pending.set(id, resolve);
            pending.set("error", reject);
          });
          worker.postMessage({
            type: "evaluate",
            id,
            items: [{fen: position.fen, legalUcis: position.legal_uci, wantActivity: false}],
          });
          const msg = await done;
          const result = msg.results[0];
          const readout = result.readout || [];
          if (readout.length !== 41692) throw new Error("readout length " + readout.length);
          for (const value of readout) {
            if (!Number.isFinite(value)) throw new Error("non-finite readout");
          }
          blocks.push(Float32Array.from(readout));
          let sum = 0;
          for (const value of readout) sum += value;
          fly.push({
            row_idx: position.row_idx,
            flynet_move: result.candidates[0] ? result.candidates[0].uci : "",
            activity_sum: sum,
          });
        }
        return {blocks, fly};
      }

      async function publishChunks(pack, name, extra) {
        const width = 41692;
        const group = 6;
        const blocks = pack.blocks;
        for (let start = 0; start < blocks.length; start += group) {
          const slice = blocks.slice(start, start + group);
          const flat = new Float32Array(slice.length * width);
          slice.forEach((row, index) => flat.set(row, index * width));
          const last = start + slice.length >= blocks.length;
          setStatus("Sending activity rows " + (start + 1) + "–" + (start + slice.length) + " to Python...");
          send(name, Object.assign({
            start: start,
            n: blocks.length,
            reset: start === 0,
            final: last,
            activity_b64: encodeActivity(flat),
            fly: pack.fly.slice(start, start + slice.length),
          }, last ? extra : {}));
          await new Promise((resolve) => setTimeout(resolve, 50));
        }
      }

      async function runGraph(kind) {
        if (busy || !worker) return;
        setBusy(true);
        setStatus(kind === "ablate"
          ? "Setting the first 2,000,000 connections in stored order to zero, then running the positions again..."
          : "Restoring the first 2,000,000 connections in stored order, then running the positions again...");
        try {
          const reply = new Promise((resolve, reject) => {
            pending.set(kind === "ablate" ? "ablated" : "restored", resolve);
            pending.set("error", reject);
          });
          worker.postMessage(kind === "ablate" ? {type: "ablate", count: 2000000} : {type: "restore"});
          const msg = await reply;
          graph = kind === "ablate" ? "ablated" : "intact";
          const pack = await evaluateAll();
          await publishChunks(pack, "activity", {touched: msg.count});
        } catch (err) {
          setStatus("Stopped: " + err.message);
        } finally {
          setBusy(false);
        }
      }
    }
    export default { render };
    """

    positions = traitlets.List().tag(sync=True)
    status = traitlets.Unicode("Press Load the real network.").tag(sync=True)
    show_ablation = traitlets.Bool(False).tag(sync=True)
    event = traitlets.Dict().tag(sync=True)

    def __init__(self, examples, **kwargs):
        records = []
        for row in examples.itertuples(index=False):
            records.append(
                {
                    "row_idx": int(row.row_idx),
                    "fen": row.fen,
                    "legal_uci": str(row.legal_uci).split(),
                }
            )
        super().__init__(positions=records, **kwargs)
        self.n_examples = len(records)
        self.activity = None
        self.fly_moves = []
        self.graph = "intact"
        self.backend = None
        self.neurons = None
        self.edges = None
        self._seen = None
        self._rows = None
        self._filled = None
        self._fly_by_index = {}

    @traitlets.observe("event")
    def _on_event(self, change):
        event = change.get("new") or {}
        name = event.get("name")
        if not name or event.get("id") == self._seen:
            return
        self._seen = event.get("id")
        try:
            self._receive(event)
        except Exception as exc:
            self.status = "Stopped while receiving activity in Python: " + str(exc)

    def _receive(self, event):
        if event.get("reset") or self._rows is None:
            self._rows = np.empty((self.n_examples, READOUT), dtype=np.float32)
            self._filled = np.zeros(self.n_examples, dtype=bool)
            self._fly_by_index = {}
        raw = base64.b64decode(event["activity_b64"])
        values = np.frombuffer(raw, dtype="<f4").copy()
        start = int(event.get("start", 0))
        count = values.size // READOUT
        if count < 1 or values.size != count * READOUT:
            raise ValueError(f"Activity chunk at row {start} has {values.size} values.")
        if start + count > self.n_examples:
            raise ValueError(f"Activity chunk {start}:{start + count} does not fit {self.n_examples} rows.")
        if not np.isfinite(values).all():
            raise ValueError("The transferred activity has a non-finite value.")
        self._rows[start : start + count] = values.reshape(count, READOUT)
        self._filled[start : start + count] = True
        for offset, item in enumerate(event.get("fly") or []):
            self._fly_by_index[start + offset] = item
        got = int(self._filled.sum())
        if got < self.n_examples or not event.get("final"):
            self.status = f"Python received {got} of {self.n_examples} activity rows."
            return
        self.activity = self._rows.copy()
        self.fly_moves = [self._fly_by_index.get(index) for index in range(self.n_examples)]
        self.graph = event.get("graph") or "intact"
        if event.get("name") == "loaded":
            self.backend = event.get("backend")
            self.neurons = int(event.get("neurons"))
            self.edges = int(event.get("edges"))
            self.status = (
                f"Python received the activity matrix. Shape {self.activity.shape}. "
                f"Browser backend {self.backend}. "
                f"{self.neurons:,} neurons, {self.edges:,} connections. "
                f"Load plus every position took {float(event.get('load_s')):.1f} s. "
                "The student's scorer has not been created yet."
            )
        elif self.graph == "ablated":
            self.status = (
                f"Python received a new activity matrix with shape {self.activity.shape}. "
                f"The first {int(event.get('touched')):,} connections in stored order are zero in the browser. "
                "Student model weights were not changed."
            )
        else:
            self.status = (
                f"Python received the restored activity matrix with shape {self.activity.shape}. "
                f"The first {int(event.get('touched')):,} connections in stored order were written back. "
                "Student model weights were not changed."
            )

    def get_activity(self):
        """Return a copy of the readout matrix. Raises if the browser has not sent it."""
        if self.activity is None:
            raise RuntimeError(
                "Python does not have the fly activity yet. "
                "Press Load the real network and wait until the status says Python received the activity matrix."
            )
        return self.activity.copy()
