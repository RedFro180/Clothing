from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

wb = Workbook()
F = "Arial"
blue = Font(name=F, color="0000FF")
black = Font(name=F)
bold = Font(name=F, bold=True)
title = Font(name=F, bold=True, size=14)
green = Font(name=F, color="008000")
yellow = PatternFill("solid", fgColor="FFFF00")
hdr = PatternFill("solid", fgColor="D9D9D9")
USD = '$#,##0.00;($#,##0.00);-'
USD0 = '$#,##0;($#,##0);-'
PCT = '0.0%;(0.0%);-'

ws = wb.active
ws.title = "Inputs"
ws["A1"] = "Hoodie margin model: inputs"; ws["A1"].font = title
ws["A2"] = "Edit only blue cells. Yellow = biggest swing assumptions, replace with real quotes. All $ are USD, estimates as of Nov 2026."
ws["A2"].font = Font(name=F, italic=True)
ws.append([])
rows = [
 ("PER-UNIT MATERIALS", None, None, None),
 ("Body fleece yards per hoodie (incl. cutting waste)", 2.0, "yd", "Estimate for a boxy hoodie on ~60in fabric; get the real figure from your sewer's marker."),
 ("Body fleece price per yard", 14.00, "$/yd", "Kinderel hemp/cotton fleece from $9.95/yd; Nature's Fabrics 280 GSM $13.99/yd; Lyrical 'Fern' $20.50/yd."),
 ("Rib yards per hoodie (cuffs + hem)", 0.25, "yd", "Estimate."),
 ("Rib price per yard (100% organic cotton)", 22.45, "$/yd", "Organic Cotton Plus Medium 1x1 Rib, $22.45/yd."),
 ("Cotton thread per hoodie", 1.00, "$", "Estimate; 100% cotton or wood-pulp thread costs more than polyester."),
 ("Drawcord + metal aglets", 1.00, "$", "Estimate; set 0 for no drawcord."),
 ("Labels (fiber, origin, care, brand)", 0.75, "$", "Estimate for small-run woven or printed cotton labels."),
 ("Freight: fabric to sewer + finished goods back, per unit", 3.00, "$", "Estimate."),
 ("PER-UNIT MAKING", None, None, None),
 ("Sewing labor (cut-make-trim), per piece", 30.00, "$", "US CMT benchmark $8-15/pc at volume (apexfashionlab); small runs and cotton thread cost more. Get quotes."),
 ("Natural dye materials per hoodie (home dyeing)", 4.00, "$", "Estimate for extract + mordant. Dye house alternative: Green Matters listed $35/garment wholesale (2023 page)."),
 ("Print materials per hoodie (paste, thickener, mordant)", 1.50, "$", "Estimate."),
 ("Your hours per hoodie (dye, print, steam, wash, pack)", 1.00, "hr", "Estimate; time yourself on the first 10."),
 ("Your hourly rate", 20.00, "$/hr", "Your choice. Set 0 to see cash-only margin."),
 ("PER-ORDER", None, None, None),
 ("Packaging (paper mailer, tissue, 988 card)", 1.50, "$", "Estimate."),
 ("Shipping label cost", 10.00, "$", "USPS Ground Advantage 2 lb ~$7.40 Zone 1 commercial; far zones higher."),
 ("Shipping charged to customer", 0.00, "$", "0 = free shipping."),
 ("Payment fee %", 0.029, "%", "Shopify Payments Basic online 2.9% + 30c."),
 ("Payment fee fixed", 0.30, "$", "Shopify Payments Basic."),
 ("Returns, refunds and unsellable seconds (% of units made)", 0.08, "%", "Estimate; natural dye and hand print raise the seconds rate."),
 ("Marketing per unit made (ads, giveaways, samples to creators)", 10.00, "$", "Estimate."),
 ("ONE-TIME DEVELOPMENT (per style)", None, None, None),
 ("Pattern making + grading", 800.00, "$", "Ranges $150-2,000+ per style (Innblac, Dutch Label Shop, Modaknits)."),
 ("Fit samples (about 2 rounds) + size set", 600.00, "$", "Estimate; ask if sample cost is credited to production."),
 ("Fabric for samples and tests", 200.00, "$", "Estimate."),
 ("Dye and wash-fastness trials", 150.00, "$", "Estimate."),
 ("YEAR-ONE FIXED COSTS", None, None, None),
 ("LLC filing (Ohio $99; Florida $125 + $138.75/yr)", 99.00, "$", "Third-party summaries; verify on state sites."),
 ("Shopify Basic (12 months at $39, or $29 if billed yearly)", 468.00, "$", "Shopify pricing pages, 2026."),
 ("Domain + email", 80.00, "$", "Estimate."),
 ("General liability insurance (incl. product)", 500.00, "$", "Guides put small apparel sellers at ~$350-750/yr."),
 ("Screen printing setup (screens, squeegees, exposure, press)", 600.00, "$", "Estimate for basic home setup."),
 ("Dye setup (stainless pots, scale, burner, steamer, PPE)", 400.00, "$", "Estimate."),
 ("Other (RN free, samples of trims, misc.)", 200.00, "$", "Estimate."),
 ("SELF-SEWN OPTION (you sew instead of a sewer)", None, None, None),
 ("Your sewing hours per hoodie (after practice)", 2.0, "hr", "Beginners 3-6 hrs per pullover; pros 1-2 hrs on industrial machines (Modaknits, Peekaboo). Time your first 10."),
 ("Sewing equipment (serger + coverstitch, one-time)", 900.00, "$", "Entry sergers ~$250-350; coverstitch extra. Verify prices."),
 ("Pattern for self-sewn (indie pattern + alterations)", 150.00, "$", "Estimate; a patternmaker draft + grade is $150-2,000."),
]
names = {}
r0 = 4
ws["A4"]="Item"; ws["B4"]="Value"; ws["C4"]="Unit"; ws["D4"]="Source / note"
for c in "ABCD": ws[f"{c}4"].font = bold; ws[f"{c}4"].fill = hdr
r = 5
keys = ["fab_yd","fab_px","rib_yd","rib_px","thread","cord","labels","freight",
        "cmt","dye","print","hrs","rate","pack","ship","shipchg","feepct","feefix","ret","mkt",
        "pattern","samples","samplefab","trials","llc","shopify","domain","ins","screen","dyeeq","other","sewhrs","sewequip","sewpattern"]
ki = 0
for label,val,unit,note in rows:
    ws.cell(r,1,label)
    if val is None:
        ws.cell(r,1).font = bold
    else:
        c = ws.cell(r,2,val); c.font = blue
        c.number_format = PCT if unit=="%" else ('0.00' if unit in ("yd","hr") else USD)
        ws.cell(r,3,unit).font = black
        ws.cell(r,4,note).font = black
        names[keys[ki]] = f"Inputs!$B${r}"; ki += 1
        ws.cell(r,1).font = black
    r += 1
for k in ["fab_px","cmt","pattern","samples","ret","mkt"]:
    ws[names[k].split("!")[1].replace("$","")].fill = yellow
ws.column_dimensions["A"].width = 58; ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 7; ws.column_dimensions["D"].width = 95

# Scenarios
s = wb.create_sheet("Scenarios")
N = names
s["A1"] = "Per-unit cost and scenario results"; s["A1"].font = title
s["A3"] = "Per-unit cost (excludes one-time and fixed costs)"; s["A3"].font = bold
lines = [
 ("Fabric", f"={N['fab_yd']}*{N['fab_px']}+{N['rib_yd']}*{N['rib_px']}"),
 ("Trims (thread, cord, labels)", f"={N['thread']}+{N['cord']}+{N['labels']}"),
 ("Freight", f"={N['freight']}"),
 ("Sewing labor", f"={N['cmt']}"),
 ("Dye + print materials", f"={N['dye']}+{N['print']}"),
 ("Your labor", f"={N['hrs']}*{N['rate']}"),
 ("Packaging", f"={N['pack']}"),
 ("Marketing", f"={N['mkt']}"),
]
rr = 4
for lab,f in lines:
    s.cell(rr,1,lab).font=black
    c=s.cell(rr,2,f); c.font=green; c.number_format=USD; rr+=1
s.cell(rr,1,"Cost to make + market one hoodie").font=bold
c=s.cell(rr,2,f"=SUM(B4:B{rr-1})"); c.font=bold; c.number_format=USD
unitrow = rr  # B12
rr += 1
s.cell(rr,1,"One-time development (per style)").font=bold
c=s.cell(rr,2,f"={N['pattern']}+{N['samples']}+{N['samplefab']}+{N['trials']}"); c.font=green; c.number_format=USD0
devrow = rr; rr+=1
s.cell(rr,1,"Year-one fixed costs").font=bold
c=s.cell(rr,2,f"={N['llc']}+{N['shopify']}+{N['domain']}+{N['ins']}+{N['screen']}+{N['dyeeq']}+{N['other']}"); c.font=green; c.number_format=USD0
fixrow = rr; rr+=2

s.cell(rr,1,"Scenario levers (blue = edit)").font=bold; rr+=1
s.cell(rr,1,"Units made →").font=bold
units=[25,50,150]
for j,u in enumerate(units):
    c=s.cell(rr,2+j,u); c.font=blue
urow=rr; rr+=1
s.cell(rr,1,"Retail prices ↓ (edit in column A rows below)").font=Font(name=F,italic=True); rr+=1

def block(metric_label, formula_fn, fmt):
    global rr
    s.cell(rr,1,metric_label).font=bold; s.cell(rr,1).fill=hdr
    for j in range(3): s.cell(rr,2+j).fill=hdr
    rr+=1
    for p in [120,150,180]:
        pc = s.cell(rr,1,p); pc.font=blue; pc.number_format=USD0
        for j in range(3):
            col = "BCD"[j]
            c=s.cell(rr,2+j,formula_fn(f"$A{rr}", f"{col}${urow}")); c.number_format=fmt; c.font=black
        rr+=1
    rr+=1

sold = lambda U: f"{U}*(1-{N['ret']})"
rev = lambda P,U: f"{sold(U)}*({P}+{N['shipchg']})"
var = lambda P,U: (f"{U}*$B${unitrow}+{sold(U)}*({N['ship']}+{N['feefix']})+{rev(P,U)}*{N['feepct']}")
block("Revenue ($)", lambda P,U: f"={rev(P,U)}", USD0)
block("Profit on run, before one-time dev and fixed costs ($)", lambda P,U: f"={rev(P,U)}-({var(P,U)})", USD0)
block("Contribution margin % (same basis)", lambda P,U: f"=IF({rev(P,U)}=0,0,({rev(P,U)}-({var(P,U)}))/({rev(P,U)}))", PCT)
block("Profit on run after one-time dev ($)", lambda P,U: f"={rev(P,U)}-({var(P,U)})-$B${devrow}", USD0)
block("Profit for year one if this is your only run (after dev + fixed) ($)", lambda P,U: f"={rev(P,U)}-({var(P,U)})-$B${devrow}-$B${fixrow}", USD0)

s.cell(rr,1,"Break-even units for one style (dev + fixed ÷ profit per unit made)").font=bold; s.cell(rr,1).fill=hdr; rr+=1
for p in [120,150,180]:
    pc=s.cell(rr,1,p); pc.font=blue; pc.number_format=USD0
    per = f"((1-{N['ret']})*({p_ref}+{N['shipchg']})*(1-{N['feepct']})-$B${unitrow}-(1-{N['ret']})*({N['ship']}+{N['feefix']}))".replace("{p_ref}","$A"+str(rr)) if False else None
    P=f"$A{rr}"
    per = f"((1-{N['ret']})*({P}+{N['shipchg']})*(1-{N['feepct']})-$B${unitrow}-(1-{N['ret']})*({N['ship']}+{N['feefix']}))"
    c=s.cell(rr,2,f'=IF({per}<=0,"never",ROUNDUP(($B${devrow}+$B${fixrow})/{per},0))'); c.number_format='0'
    rr+=1
rr+=1
s.cell(rr,1,"Notes: sales tax is collected and passed to the state, so it is excluded. 'Your labor' is a cost; set your rate to 0 on Inputs to see cash-only results. Returns % reduces units sold, but you still pay to make them.").font=Font(name=F,italic=True)
s.column_dimensions["A"].width=70
for c in "BCD": s.column_dimensions[c].width=14

# Self-sewn comparison
c2 = wb.create_sheet("Self-sewn vs sewer")
c2["A1"] = "Sewing it yourself vs paying a sewer (per hoodie)"; c2["A1"].font = title
c2["A2"] = "Gross margin = (price - cost to make) / price. Cost to make excludes marketing, shipping, card fees and returns."
c2["A2"].font = Font(name=F, italic=True)
hdrs = ["Item","Paid sewer","Self-sewn"]
for j,h in enumerate(hdrs):
    c=c2.cell(4,1+j,h); c.font=bold; c.fill=hdr
mat = f"{N['fab_yd']}*{N['fab_px']}+{N['rib_yd']}*{N['rib_px']}+{N['thread']}+{N['cord']}+{N['labels']}"
items = [
 ("Materials (fabric, rib, thread, cord, labels)", f"={mat}", f"={mat}"),
 ("Freight to/from sewer", f"={N['freight']}", "=0"),
 ("Sewing labor paid out", f"={N['cmt']}", "=0"),
 ("Dye + print materials", f"={N['dye']}+{N['print']}", f"={N['dye']}+{N['print']}"),
 ("Packaging", f"={N['pack']}", f"={N['pack']}"),
 ("Cash cost to make", "=SUM(B5:B9)", "=SUM(C5:C9)"),
 ("Your time: dye/print/pack hours x rate", f"={N['hrs']}*{N['rate']}", f"={N['hrs']}*{N['rate']}"),
 ("Your time: sewing hours x rate", "=0", f"={N['sewhrs']}*{N['rate']}"),
 ("Full cost to make (incl. your time)", "=B10+B11+B12", "=C10+C11+C12"),
]
for i,(lab,a,b) in enumerate(items):
    r_=5+i
    c2.cell(r_,1,lab).font = bold if lab.startswith(("Cash","Full")) else black
    for j,f in enumerate((a,b)):
        c=c2.cell(r_,2+j,f); c.number_format=USD; c.font=green
c2.cell(15,1,"Gross margin at retail price ↓").font=bold
for j in range(3): c2.cell(15,1+j).fill=hdr
rr2=16
for p in (120,150):
    c=c2.cell(rr2,1,p); c.font=blue; c.number_format=USD0
    c2.cell(rr2,4,"cash only (your time free)").font=Font(name=F,italic=True)
    for j,col in enumerate("BC"):
        c=c2.cell(rr2,2+j,f"=($A{rr2}-{col}$10)/$A{rr2}"); c.number_format=PCT
    rr2+=1
    c=c2.cell(rr2,1,p); c.font=blue; c.number_format=USD0
    c2.cell(rr2,4,"with your time paid").font=Font(name=F,italic=True)
    for j,col in enumerate("BC"):
        c=c2.cell(rr2,2+j,f"=($A{rr2}-{col}$13)/$A{rr2}"); c.number_format=PCT
    rr2+=1
c2.cell(rr2+1,1,"One-time for self-sewn: equipment + pattern").font=bold
c=c2.cell(rr2+1,3,f"={N['sewequip']}+{N['sewpattern']}"); c.number_format=USD0; c.font=green
c2.cell(rr2+2,1,"Hoodies per 40-hour week at your sewing hours (sewing only)").font=bold
c=c2.cell(rr2+2,3,f"=IF({N['sewhrs']}=0,0,ROUNDDOWN(40/{N['sewhrs']},0))"); c.number_format='0'
c2.cell(rr2+4,1,"Note: the higher cash margin when self-sewn is mostly your unpaid wages. It also caps how many you can make.").font=Font(name=F,italic=True)
c2.column_dimensions["A"].width=55
for col in "BC": c2.column_dimensions[col].width=14
c2.column_dimensions["D"].width=28

# Legend example note
ws.cell(r+1,1,"Example: if a sewer quotes $38 per piece, type 38 in the 'Sewing labor' blue cell; Scenarios updates automatically.").font=Font(name=F,italic=True)
wb.save("/home/user/Clothing/docs/margin-model.xlsx")
print(unitrow, devrow, fixrow, urow)
