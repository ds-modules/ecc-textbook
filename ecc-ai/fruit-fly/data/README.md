# Classroom excerpt of MaleCNS v1.0

These two CSV files are a small excerpt for an El Camino College notebook. They are not the full connectome. The full connection table is about 1.1 GB and is not stored in this repository.

## What was kept

Six neurons, chosen by type name:

| Type | How many | Why this type is in the excerpt |
|---|---|---|
| `DNp01` | 2 | The giant fiber descending neurons. Their instance names are `DNp01(GF)_L` and `DNp01(GF)_R`. |
| `TTMn` | 2 | The tergotrochanteral motor neurons, one on each side. |
| `PSI` | 2 | The neurons named PSI (peripherally synapsing interneuron), one on each side. |

Every `ConnectsTo` link with both ends inside that set was kept. Weak links were not deleted. The excerpt has 6 neurons and 16 connections.

This is one male fruit fly central nervous system (brain and nerve cord), dataset **MaleCNS v1.0**. It is not the female FlyWire brain.

## Where the rows came from

Queried on 27 September 2026 from the public neuPrint server:

- Server: `https://neuprint.janelia.org/api/custom/custom`
- Dataset sent in the request: `male-cns:v1.0`
- The server rewrote neuron labels to `male-cns_Neuron`
- No account and no API token were sent
- The `Meta` node returned dataset name `male-cns`, uuid `4b2087c0fbe046bfaf0d60bc970e3e5d`, and a last database edit that includes `2026-06-08`, the MaleCNS v1.0 release date listed on [male-cns.janelia.org](https://male-cns.janelia.org/)

Neuron query:

```cypher
MATCH (n:Neuron)
WHERE n.type IN ['DNp01', 'TTMn', 'PSI']
RETURN n.bodyId, n.type, n.instance, n.status, n.statusLabel,
       n.superclass, n.subclass, n.pre, n.post, n.vfbId
ORDER BY n.bodyId
```

Connection query:

```cypher
MATCH (a:Neuron)-[c:ConnectsTo]->(b:Neuron)
WHERE a.type IN ['DNp01', 'TTMn', 'PSI']
  AND b.type IN ['DNp01', 'TTMn', 'PSI']
RETURN a.bodyId, a.instance, b.bodyId, b.instance, c.weight
ORDER BY c.weight DESC, a.bodyId, b.bodyId
```

`synapse_count` is neuPrint's `ConnectsTo.weight`. `presynaptic_sites` and `postsynaptic_sites` are neuPrint's `pre` and `post`.

## Cross-check against the official bulk files

Identity columns were checked against the official annotation file, downloaded once and not committed:

`gs://flyem-male-cns/v1.0/connectome-data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather`

Public HTTPS copy:

`https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather`

- Size: 14,483,314 bytes
- MD5: `50a7718770c57220f160ba4f431ab89e` (matches the bucket listing)

For all six body IDs, `type`, `instance`, `status`, `statusLabel`, `superclass`, `subclass`, and `vfbId` matched that file. The `synonyms` value `Kennedy and Broadie 2018: GF` for both DNp01 neurons is from that file. TTMn and PSI have no synonym there.

`presynaptic_sites` was also checked against `total_nt_predictions` in:

`body-neurotransmitters-male-cns-v1.0.feather` (43,282,834 bytes, MD5 `3d842b12fe5c49eefade528d7dd24a1f`)

The six presynaptic counts match. That neurotransmitter file was not copied into the CSV. For TTMn, the per-neuron `predicted_nt` and the type-level `consensus_nt` are not the same (`TTMn_R` is predicted histamine, while the TTMn consensus is glutamate). Leaving those columns out avoids presenting one of those numbers as if it were the only official value.

Connection weights were read from neuPrint. They were not re-checked against `connectome-weights-male-cns-v1.0-minconf-0.5.feather` (about 1.1 GB). `weightHR`, `weightHP`, and `roiInfo` were not copied.

## Files

- `neurons.csv` — one row per neuron in the excerpt
- `connections.csv` — one row per directed connection inside the excerpt

## License and attribution

The Male CNS connectome is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

This excerpt is an adaptation: it keeps six neuron types and the connections among them, drops the rest of the graph, and drops columns that were not needed in class. The values that remain were not edited.

Please cite the dataset and the paper:

Berg, S., et al. (2026). Sexual dimorphism in the complete connectome of the Drosophila male central nervous system. *Cell*, 189, 5504–5526. https://doi.org/10.1016/j.cell.2026.08.015

The paper is published by Elsevier under CC BY 4.0 (© 2026 MRC Laboratory of Molecular Biology).

Data producers: FlyEM at HHMI Janelia Research Campus, the University of Cambridge Department of Zoology, the MRC Laboratory of Molecular Biology, and Google Research.

Project pages:

- https://male-cns.janelia.org/
- https://male-cns.janelia.org/download/
- https://neuprint.janelia.org/ (dataset `male-cns:v1.0`)

This classroom excerpt does not imply endorsement by those groups.
