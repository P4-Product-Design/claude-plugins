# Figma recipes for a reskin

These scripts were tested on the MN Product Row reskin in November 2026. Load `figma-use` before every `use_figma` call, and the generic `figma-generate-library` skill before writes. Replace the `UPPER_CASE` placeholders with real IDs from earlier calls. Run calls one after another, never in parallel.

## Traps from the MN run

| Trap | What to do |
|---|---|
| Swapping an instance invalidates the IDs of every node inside it (`node … does not exist`). | Collect the IDs of instances that have no INSTANCE ancestor **before** any swap. Swap only those, and re-fetch each one by ID. |
| A script error rolls back the whole script. | Read the canvas before you retry. |
| `importComponentByKeyAsync` fails for components in unpublished or unsubscribed libraries. | Get the main component from an existing instance in the destination kit, using `getNodeByIdAsync` and then `getMainComponentAsync`. |
| Text with mixed fonts fails on `loadFontAsync(t.fontName)`. | Load each segment's font from `getStyledTextSegments(['fontName'])`. |
| A spacing token with the same name has a different value in each brand (MC `spacing/xs` = 16, MN `spacing/xs` = 12). | Rebind spacing and radius **by value**, never by name. |
| A swapped button keeps the source instance's width, and non-auto-layout destination buttons clip their label. | Restore `layoutSizingHorizontal`. If the destination main component has `layoutMode` NONE, resize the instance to the main component's size. |
| Hidden button instances can come out of a swap with no text layer. | Flag them as a follow-up. Don't invent labels. |
| A destination kit component can change while the run is in progress (MN Tertiary went from a gray fill to an outline). | Before reporting, re-read the destination components you swapped to. Report any that changed. |
| `.header` is often the same shared P4 component in both kits (same key). | Compare keys and swap only when they differ. Partners always get swapped. |
| The pasted main components arrive as **local** components. Only their nested parts stay linked to the source library. | Edit them in place. Never rebuild them. |

## 1. Inventory of the pasted frame (read-only)

```js
const page = await figma.getNodeByIdAsync('DEST_PAGE_ID');
await figma.setCurrentPageAsync(page);
const root = await figma.getNodeByIdAsync('PASTED_FRAME_ID');
const vars={}, textStyles={}, fillStyles={}, rawColors={}, radii={}, comps={}, fonts={};
const hex = c => '#'+[c.r,c.g,c.b].map(v=>Math.round(v*255).toString(16).padStart(2,'0')).join('');
const vc={}; async function vName(id){ if(!(id in vc)){const v=await figma.variables.getVariableByIdAsync(id); vc[id]=v?`${v.name}${v.remote?' [remote]':''}`:'?';} return vc[id]; }
async function sName(id){ if(!id||typeof id!=='string') return null; const s=await figma.getStyleByIdAsync(id); return s?s.name+(s.remote?' [remote]':''):null; }
async function walk(n){
  if (n.boundVariables) for (const [p,b] of Object.entries(n.boundVariables)) for (const a of (Array.isArray(b)?b:[b])) if (a&&a.id){const k=await vName(a.id);(vars[k]=vars[k]||new Set()).add(p);}
  for (const key of ['fills','strokes']) if (key in n && Array.isArray(n[key])) for (const p of n[key]) if (p.type==='SOLID') {
    if (p.boundVariables&&p.boundVariables.color){const k=await vName(p.boundVariables.color.id);(vars[k]=vars[k]||new Set()).add(key);}
    else if (!n[key==='fills'?'fillStyleId':'strokeStyleId']) {const h=hex(p.color); rawColors[h]=(rawColors[h]||0)+1;}
  }
  const fs = await sName(n.fillStyleId); if (fs) fillStyles[fs]=(fillStyles[fs]||0)+1;
  const ss = await sName(n.strokeStyleId); if (ss) fillStyles[ss]=(fillStyles[ss]||0)+1;
  if (n.type==='TEXT') { const ts=await sName(n.textStyleId); if (ts) textStyles[ts]=(textStyles[ts]||0)+1; else { const f=typeof n.fontName==='symbol'?'mixed':`${n.fontName.family} ${n.fontName.style} ${String(n.fontSize)}`; fonts[f]=(fonts[f]||0)+1; } }
  if ('cornerRadius' in n && typeof n.cornerRadius==='number' && n.cornerRadius>0) radii[n.cornerRadius]=(radii[n.cornerRadius]||0)+1;
  if (n.type==='INSTANCE'){const mc=await n.getMainComponentAsync(); if(mc){const k=`${mc.parent&&mc.parent.type==='COMPONENT_SET'?mc.parent.name+' / ':''}${mc.name} ${mc.remote?'[remote '+mc.key+']':'[local '+mc.id+']'}`; comps[k]=(comps[k]||0)+1;}}
  if ('children' in n) for (const c of n.children) await walk(c);
}
await walk(root);
const s=o=>Object.fromEntries(Object.entries(o).map(([k,v])=>[k,v instanceof Set?[...v].join(','):v]));
return { vars:s(vars), textStyles, fillStyles, fonts, rawColors, radii, comps };
```

## 2. Destination kit tokens (read-only, page-independent)

```js
const hex = c => '#'+[c.r,c.g,c.b].map(v=>Math.round(v*255).toString(16).padStart(2,'0')).join('');
const out={};
for (const c of await figma.variables.getLocalVariableCollectionsAsync()) {
  const list=[]; for (const id of c.variableIds){ const v=await figma.variables.getVariableByIdAsync(id); let val=v.valuesByMode[c.modes[0].modeId];
    if (val&&val.type==='VARIABLE_ALIAS'){const a=await figma.variables.getVariableByIdAsync(val.id); val='→'+(a?a.name:'?');} else if (val&&typeof val==='object'&&'r' in val) val=hex(val);
    list.push(`${v.name}=${val}`);} out[c.name]=list; }
const ts=(await figma.getLocalTextStylesAsync()).map(s=>`${s.name} | ${s.fontName.family} ${s.fontName.style} ${s.fontSize}/${s.lineHeight.unit==='PIXELS'?s.lineHeight.value:s.lineHeight.unit}`);
const ps=(await figma.getLocalPaintStylesAsync()).map(s=>`${s.name}=${s.paints[0]&&s.paints[0].type==='SOLID'?hex(s.paints[0].color):s.paints[0]&&s.paints[0].type}`);
return { variables:out, textStyles:ts, paintStyles:ps, effectStyles:(await figma.getLocalEffectStylesAsync()).map(s=>s.name) };
```

To read the Button set, open the destination Buttons page. For each variant, list its name, fill, stroke, radius, label color, size and `layoutMode`.

## 3. Local copies of source-only components, then relink

List components leaf-first: icons and cursors, then stars, then pills and tags, then price, then parent cards. A variant set becomes `{set, items:[[key, variantName], …]}`, and a single component becomes `{single, key}`.

```js
const page = await figma.getNodeByIdAsync('DEST_PAGE_ID'); await figma.setCurrentPageAsync(page);
const root = await figma.getNodeByIdAsync('PASTED_FRAME_ID');
for (const f of await figma.listAvailableFontsAsync()) if (FONT_FAMILIES.includes(f.fontName.family)) { try { await figma.loadFontAsync(f.fontName); } catch(e){} }
const spec = SPEC; // leaf → up
function hasInstAncestor(n){ let p=n.parent; while(p&&p.type!=='PAGE'){ if(p.type==='INSTANCE') return true; p=p.parent; } return false; }
const remoteByKey={}, topLevel=[];
for (const inst of page.findAllWithCriteria({types:['INSTANCE']})) { const mc=await inst.getMainComponentAsync(); if(!mc) continue; if(mc.remote&&!remoteByKey[mc.key]) remoteByKey[mc.key]=mc; if(!hasInstAncestor(inst)) topLevel.push({id:inst.id,key:mc.remote?mc.key:null}); }
const holder = figma.createAutoLayout('VERTICAL',{name:'.BRANDSubcomponents',itemSpacing:48});
holder.paddingTop=holder.paddingBottom=holder.paddingLeft=holder.paddingRight=40; holder.fills=[];
page.appendChild(holder); holder.x=root.x+root.width+200; holder.y=root.y;
const localByKey={}, created=[], missing=[];
function makeLocal(key,name){ const mc=remoteByKey[key]; if(!mc){missing.push(name);return null;} const i=mc.createInstance(); page.appendChild(i); const c=figma.createComponentFromNode(i.detachInstance()); c.name=name; localByKey[key]=c; return c; }
for (const s of spec) {
  if (s.single) { const c=makeLocal(s.key,s.single); if(c){holder.appendChild(c); created.push({name:s.single,id:c.id});} }
  else { const comps=s.items.map(([k,n])=>makeLocal(k,n)).filter(Boolean); if(!comps.length) continue;
    const cs=figma.combineAsVariants(comps,holder); cs.name=s.set; let x=0; for(const c of cs.children){c.x=x;c.y=0;x+=c.width+24;}
    cs.resizeWithoutConstraints(Math.max(1,x-24),Math.max(...cs.children.map(c=>c.height))); created.push({name:s.set,id:cs.id}); }
}
for (const inst of holder.findAllWithCriteria({types:['INSTANCE']})) { if(hasInstAncestor(inst)) continue; const mc=await inst.getMainComponentAsync(); topLevel.push({id:inst.id,key:mc&&mc.remote?mc.key:null}); }
let swapped=0; for (const t of topLevel) { if(!t.key||!localByKey[t.key]) continue; const inst=await figma.getNodeByIdAsync(t.id); if(!inst) continue; inst.swapComponent(localByKey[t.key]); swapped++; }
return { holder:holder.id, created, missing, swapped };
```

Afterwards, look for remote instances that still point at a copied key. These are nested overrides. Swap them to the local variant.

## 4. Buttons and doc chrome

`MAP` maps each source main-component key to the destination component node. Get destination buttons by node ID from the kit's Button set. For a shared component like `.Section`, take the main component from an instance on another destination page.

```js
// inside the page context; fonts loaded as above
const cands=[]; for (const inst of page.findAllWithCriteria({types:['INSTANCE']})) { if(hasInstAncestor(inst)) continue; const mc=await inst.getMainComponentAsync(); if(mc&&mc.remote&&MAP[mc.key]) cands.push(inst.id); }
for (const id of cands) {
  const inst=await figma.getNodeByIdAsync(id); if(!inst) continue;
  const label=(inst.findAll(n=>n.type==='TEXT'&&n.visible)[0]||{}).characters;
  const parentAL=inst.parent&&'layoutMode' in inst.parent&&inst.parent.layoutMode!=='NONE';
  const sH=inst.layoutSizingHorizontal, w=inst.width; const mc=await inst.getMainComponentAsync(); const target=MAP[mc.key];
  inst.swapComponent(target);
  const t=inst.findOne(n=>n.type==='TEXT'&&n.visible);
  if (t && label) { for (const s of t.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(s.fontName); t.characters=label; }
  if (inst.layoutMode==='NONE') inst.resize(target.width,target.height);
  else if (parentAL) { inst.layoutSizingHorizontal=sH; if(sH==='FIXED') inst.resize(w,inst.height); }
}
```

## 5. Rebind colors, text, radius and spacing

Build each map from the inventory and the destination tokens:
- `fillMap`: source style name → destination paint-style name.
- `hexMap`: raw hex → destination style.
- `leftoverVarMap`: SO-era variables → destination style.
- `textMap`: source text style → destination text style.
- `spaceByVal` and `radiusMap`: value → destination variable.

Work in this order:
1. **Component definitions first:** the sub-components holder, then the component sets inside the frame, then the rest of the frame. Skip nodes inside instances.
2. **Overrides inside instances:** a second pass that only touches nodes still referencing the source.

The rules that keep this working:
- Skip the subtrees of destination-kit Button instances and of shared doc chrome.
- Only set a style when the current style is **remote**. Never touch the destination's local styles.
- Map text **per segment**, with `getStyledTextSegments(['textStyleId','fillStyleId','fontName','fills'])` + `setRangeTextStyleIdAsync` / `setRangeFillStyleIdAsync`. Load every segment's font first.
- For paint styles on nodes, use `setFillStyleIdAsync` / `setStrokeStyleIdAsync`. For a fill bound to a variable with no destination equivalent, unbind it with `figma.variables.setBoundVariableForPaint(p,'color',null)` and reassign the fills array.
- For radius, set all four corners to the destination value, then `setBoundVariable(corner, var)`. Leave instances' own radius alone.
- For spacing, read the property's current number and bind the destination variable with that **value**. If no variable has that value, unbind and flag it.
- Leave Figma's doc chrome alone: the purple `#8a38f5` dashed component-set borders and the black on-canvas labels. They aren't brand tokens.

## 6. Renames and descriptions

```js
for (const n of [root, ...root.findAll(()=>true), holder, ...holder.findAll(()=>true)]) {
  if (hasInstAncestor(n)) continue;
  const nn = n.name.replace(/\bSRC\b/g,'DST').replace(/^\.srcLower(?=[A-Z])/,'.dstLower');
  if (nn!==n.name) n.name=nn;
}
for (const n of page.findAllWithCriteria({types:['COMPONENT','COMPONENT_SET']})) {
  if (n.type==='COMPONENT' && n.parent && n.parent.type==='COMPONENT_SET') { if (n.description) n.description=''; continue; }
  // set n.description to a neutral one-to-two sentence summary written for this component, or '' if there is nothing to say
}
```

## 7. Final audit (read-only)

```js
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('DEST_PAGE_ID'));
const roots = [await figma.getNodeByIdAsync('PASTED_FRAME_ID'), await figma.getNodeByIdAsync('HOLDER_ID')];
const PARTNER = IS_PARTNER;               // true for AARP / NCOA / FOR
const TERMS = SCRUB_TERMS;                // array of strings from brands.md, minus the destination's own
const re = new RegExp('(^|[^A-Za-z0-9])(' + TERMS.map(t=>t.replace(/[.*+?^${}()|[\]\\\/]/g,'\\$&')).join('|') + ')(?=$|[^A-Za-z0-9])', 'i');
const sc={}; async function st(id){ if(!id||typeof id!=='string') return null; if(!(id in sc)){const s=await figma.getStyleByIdAsync(id); sc[id]=s?{n:s.name,r:s.remote}:null;} return sc[id]; }
const vc={}; async function vi(id){ if(!(id in vc)){const v=await figma.variables.getVariableByIdAsync(id); vc[id]=v?{n:v.name,r:v.remote}:null;} return vc[id]; }
const bad={}, fonts={}, scrub=[];
const add=k=>bad[k]=(bad[k]||0)+1;
async function visit(n){
  if (n.type==='INSTANCE'){ const mc=await n.getMainComponentAsync(); if(mc&&mc.remote){ const chrome=['.header','.Section','.section'].includes(mc.name); if(chrome&&!PARTNER) return; add('remote component: '+mc.name); } }
  for (const k of ['fillStyleId','strokeStyleId','textStyleId']) if (k in n){ const s=await st(n[k]); if(s&&s.r) add('remote style: '+s.n); }
  if (n.boundVariables) for (const b of Object.values(n.boundVariables)) for (const a of (Array.isArray(b)?b:[b])) if(a&&a.id){ const v=await vi(a.id); if(v&&v.r) add('remote variable: '+v.n); }
  for (const k of ['fills','strokes']) if (k in n && Array.isArray(n[k])) for (const p of n[k]) if (p.boundVariables&&p.boundVariables.color){ const v=await vi(p.boundVariables.color.id); if(v&&v.r) add('remote variable: '+v.n); }
  if (n.type==='TEXT' && typeof n.fontName!=='symbol') fonts[n.fontName.family]=(fonts[n.fontName.family]||0)+1;
  if (PARTNER) {
    if (re.test(n.name)) scrub.push({where:'name', id:n.id, text:n.name});
    if (n.type==='TEXT' && re.test(n.characters)) scrub.push({where:'text', id:n.id, text:n.characters.slice(0,80)});
    if ((n.type==='COMPONENT'||n.type==='COMPONENT_SET') && re.test(n.description||'')) scrub.push({where:'description', id:n.id, text:n.description.slice(0,80)});
  }
  if ('children' in n) for (const c of n.children) await visit(c);
}
for (const r of roots) if (r) await visit(r);
return { remaining: bad, fonts, scrubHits: scrub.slice(0,50), scrubCount: scrub.length };
```
Every count of remote source-brand items must be 0. Fonts must be the destination's families only. Inter is allowed on the doc labels when the destination's own pages use it there.
