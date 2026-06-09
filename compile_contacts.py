"""
Compiles contacts from 4 Google Sheets into linkedin_results.csv
Sources:
  - Beth Israel Lahey Health Systems
  - Mass General Brigham
  - Alberta Primary Care Networks
  - British Columbia Primary Care Networks
"""

import csv
import os

# Each entry: (name, title, company, linkedin, source)
RAW = [
    # ─── BETH ISRAEL LAHEY HEALTH SYSTEMS ───
    ("Megan Smith", "Behavioral Health Clinician", "Beth Israel Lahey Health Primary Care - 1000 Broadway", "https://www.linkedin.com/in/megan-j-smith-lcsw/", "BILH"),
    ("Pamela A. Fox", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - 1000 Broadway", "https://www.linkedin.com/in/pamela-fox-np-450b264/", "BILH"),
    ("Lauren Marie Kennedy", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - 1000 Broadway", "https://www.linkedin.com/in/lauren-kennedy-58586a1a0/", "BILH"),
    ("Peter Shorett", "SEVP and Chief Operating Officer", "Beth Israel Lahey Health Systems", "https://www.linkedin.com/in/peter-shorett-1604344/", "BILH"),
    ("Mallory Toomey", "Nurse Practitioner", "Beth Israel Lahey Health Systems", "https://www.linkedin.com/in/mallory-toomey-683972106/", "BILH"),
    ("Laura Elizabeth Varrasso", "Nurse Practitioner", "Beth Israel Lahey Health Systems", "https://www.linkedin.com/in/laura-varrasso-28a18295/", "BILH"),
    ("Kuon S. Lo", "Clinical Faculty", "Beth Israel Lahey Health Primary Care - 1100 Washington", "https://www.linkedin.com/in/kuon-lo-7a1b6629/", "BILH"),
    ("Dat T. Le", "Family Medicine Physician", "Beth Israel Lahey Health Primary Care - 1100 Washington", "https://www.linkedin.com/in/dat-le-a43a19aa/", "BILH"),
    ("Linh X. Huynh", "Physician Assistant", "Beth Israel Lahey Health Primary Care - 1100 Washington", "https://www.linkedin.com/in/linh-huynh-a15b81b6/", "BILH"),
    ("Emily R. Gorman-Melo", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - 1st Floor, Addison Gilbert Hospital", "https://www.linkedin.com/in/emily-gorman-melo-2ba529a4/", "BILH"),
    ("Amy Bonner Esdale", "Family Medicine Specialist", "Beth Israel Lahey Health Primary Care - 1st Floor, Addison Gilbert Hospital", "", "BILH"),
    ("Kathryn J. Hollett", "Family Medicine Physician", "Beth Israel Lahey Health Primary Care - 1st Floor, Addison Gilbert Hospital", "", "BILH"),
    ("Meredith Peabody Veneziano", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Family Medicine Associates - Manchester", "https://www.linkedin.com/in/meredith-veneziano-peabody-876bb46b/", "BILH"),
    ("Molly Jean Klinka", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - Family Medicine Associates - Manchester", "", "BILH"),
    ("Rachel Katherine Hilshey", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Family Medicine Associates - Manchester", "", "BILH"),
    ("Angela Kaptsan", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - Andrew Avenue", "", "BILH"),
    ("Lauren Nicole Fitzharris", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Andrew Avenue", "https://www.linkedin.com/in/laurendamico27/", "BILH"),
    ("Deborah J. Riester", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Andrew Avenue", "", "BILH"),
    ("Elizabeth Welsh Thidemann", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Belmont Medical Associates", "https://www.linkedin.com/in/elizabeth-thidemann/", "BILH"),
    ("Anna Ost", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - Belmont Medical Associates", "", "BILH"),
    ("Nancy H. Tran", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Belmont Medical Associates", "https://www.linkedin.com/in/nancy-tran-677b8b8/", "BILH"),
    ("Amy Xiong", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - Bedford Street", "https://www.linkedin.com/in/amyyxiong/", "BILH"),
    ("Helen Chan", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Bedford Street", "", "BILH"),
    ("Xiaohui L. Wang", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Bedford Street", "https://www.linkedin.com/in/xiaohui-wang-78291632/", "BILH"),
    ("Sharone Moverman", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 372 Washington", "https://www.linkedin.com/in/sharone-moverman-513b698a/", "BILH"),
    ("Brittanie McCabe", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 372 Washington", "https://www.linkedin.com/in/brittaniedillon/", "BILH"),
    ("Edward V. Shashoua", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 372 Washington", "https://www.linkedin.com/in/ed-shashoua-a0423810/", "BILH"),
    ("Olivia O'Shea", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - 625 Mount Auburn Street", "", "BILH"),
    ("Hamna Umar", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 625 Mount Auburn Street", "", "BILH"),
    ("Robert C. Scaffidi", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 625 Mount Auburn Street", "https://www.linkedin.com/in/robert-scaffidi-b3a335398/", "BILH"),
    ("Yana M. Urman", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 714 Beacon", "", "BILH"),
    ("Alice I. Lin", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 714 Beacon", "", "BILH"),
    ("Kari E. Emsbo", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 714 Beacon", "", "BILH"),
    ("Kerry M. Kilban", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Family Care Center Stoneham", "https://www.linkedin.com/in/kkilban", "BILH"),
    ("Rose S. Weld", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Family Care Center Stoneham", "https://www.linkedin.com/in/rose-weld-7072443a/", "BILH"),
    ("Arantxa Lewis", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Family Care Center Stoneham", "", "BILH"),
    ("Samantha Kerrins", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Brookline Family Medicine", "https://www.linkedin.com/in/samantha-kerrins-msn-fnp-bc-50a18b116/", "BILH"),
    ("Allie Win Collignon", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Brookline Family Medicine", "https://www.linkedin.com/in/alliecollignon/", "BILH"),
    ("Linya Yang", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Brookline Family Medicine", "", "BILH"),
    ("Jacqueline Vittum", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - Chestnut Street", "https://www.linkedin.com/in/jackie-vittum-dnp-fnp-bc-291313169/", "BILH"),
    ("Nora Garrity Burke", "Physician Assistant", "Beth Israel Lahey Health Primary Care - Chestnut Street", "https://www.linkedin.com/in/nora-garrity-burke-4b2aa1154/", "BILH"),
    ("Steven V. Lord", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Chestnut Street", "", "BILH"),
    ("Cathy D'Augusta", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Concord Street", "https://www.linkedin.com/in/cathy-d-augusta-40a9027b", "BILH"),
    ("Kerry Eaton", "Physician Assistant", "Beth Israel Lahey Health Primary Care - Concord Street", "https://www.linkedin.com/in/kerry-eaton/", "BILH"),
    ("Mariellen T. Rodman", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Concord Street", "https://www.linkedin.com/in/mariellen-rodman-9247a828/", "BILH"),
    ("Leah Scialo Walsh", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 900 Cummings", "", "BILH"),
    ("Holly Elice Roberts", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 900 Cummings", "", "BILH"),
    ("Sarah Elizabeth Tsouvalas", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - 900 Cummings", "https://www.linkedin.com/in/sarah-tsouvalas-msn-fnp-c-4235761a/", "BILH"),
    ("Chloe Fish", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - General Internal Medicine, Lahey Medical Center, Peabody", "https://www.linkedin.com/in/chloe-fish/", "BILH"),
    ("Michelle Nelson", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - General Internal Medicine, Lahey Medical Center, Peabody", "", "BILH"),
    ("Katherine Rosanne Alonso", "Nurse Practitioner", "Beth Israel Lahey Health Primary Care - General Internal Medicine, Lahey Medical Center, Peabody", "", "BILH"),
    ("Kasey Ryan Moffat", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Hartwell Avenue", "https://www.linkedin.com/in/kasey-moffat-msn-fnp-bc-4451261b/", "BILH"),
    ("Kathryn E. Liziewski", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Hartwell Avenue", "https://www.linkedin.com/in/kliziewski/", "BILH"),
    ("Samantha Lillian Borrelli", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Hartwell Avenue", "https://www.linkedin.com/in/samantha-borrelli-32abb6b4/", "BILH"),
    ("Alison P. Valsky", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Market Crossing", "", "BILH"),
    ("Andrea B. Day", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Market Crossing", "", "BILH"),
    ("Brian P. Fitzpatrick", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Market Crossing", "", "BILH"),
    ("Anna E. Read", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Lynnfield", "https://www.linkedin.com/in/anna-read-982561157/", "BILH"),
    ("Amy Nicole O'Brien", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Lynnfield", "", "BILH"),
    ("Amanda May Coffey", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Lynnfield", "https://www.linkedin.com/in/amanda-coffey-4a77a0283/", "BILH"),
    ("Laura Katherine Marcinkowski", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Hayden Avenue", "", "BILH"),
    ("Jessica Ann Krass", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Hayden Avenue", "https://www.linkedin.com/in/jessica-krass-81915a147/", "BILH"),
    ("Indranil Bhattacharya", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Hayden Avenue", "https://www.linkedin.com/in/indranil-bhattacharya-a52720202", "BILH"),
    ("Shikha S. Merchia", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - John Mahar Highway", "https://www.linkedin.com/in/shikha-merchia-46535b9/", "BILH"),
    ("Mohamed A. Elgeziry", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - John Mahar Highway", "", "BILH"),
    ("Biljana Vitanova", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Lowney Medical Associates", "https://www.linkedin.com/in/biljana-vitanova-a12767319/", "BILH"),
    ("Jessica AS Santiccioli", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Lowney Medical Associates", "", "BILH"),
    ("Susan Judge Burns", "Primary Care Practitioner", "Beth Israel Lahey Health Primary Care - Lowney Medical Associates", "https://www.linkedin.com/in/susan-judge-burns-9062332b/", "BILH"),

    # ─── MASS GENERAL BRIGHAM ───
    ("Barbara Holbert", "Medical Director", "Mass General Downtown Primary Care", "", "MGB"),
    ("Leah Rose Giunta", "Nurse Practitioner", "Mass General Downtown Primary Care", "", "MGB"),
    ("Lauren Abbate", "Primary Care Physician", "Mass General Downtown Primary Care", "https://www.linkedin.com/in/lauren-abbate-70107034/", "MGB"),
    ("Anne Klibanski", "President and Chief Executive Officer", "Mass General Brigham", "https://www.linkedin.com/in/anne-klibanski-m-d-72844416", "MGB"),
    ("Ron M. Walls", "Chief Operating Officer", "Mass General Brigham", "https://www.linkedin.com/in/ron-walls-6473a916/", "MGB"),
    ("Chris Coburn", "Chief Innovation Officer", "Mass General Brigham", "https://www.linkedin.com/in/ccoburn", "MGB"),
    ("O'Neil Britton", "Chief Integration Officer, Executive Vice President", "Mass General Brigham", "https://www.linkedin.com/in/o-neil-britton/", "MGB"),
    ("Mark Bohen", "Chief Marketing and Communications Officer", "Mass General Brigham", "https://www.linkedin.com/in/markbohenbrands/", "MGB"),
    ("Tom Sequist", "Chief Medical Officer", "Mass General Brigham", "https://www.linkedin.com/in/thomas-sequist-7798a784/", "MGB"),
    ("Amanda Berling", "Medical Director", "Brigham and Women's Phyllis Jen Center for Primary Care", "", "MGB"),
    ("Christina Meade", "Clinical Staff", "Brigham and Women's Phyllis Jen Center for Primary Care", "https://www.linkedin.com/in/christina-meade-18640555/", "MGB"),
    ("Kaitlin Fitzpatrick", "Primary Care Doctor", "Mass General Beacon Hill Primary Care", "", "MGB"),
    ("Diana Cornell", "Primary Care Doctor", "Mass General Beacon Hill Primary Care", "", "MGB"),
    ("Susan Topley", "Administrative Manager", "Massachusetts General Hospital", "https://www.linkedin.com/in/susan-topley-94152666/", "MGB"),
    ("Michaela Mitrano", "MHA, Operations Program Manager", "Massachusetts General Hospital", "https://www.linkedin.com/in/michaela-mitrano-mha-16887713b/", "MGB"),
    ("Chin Ho Fung", "Primary Care Physician", "Mass General Bulfinch Medical Group", "https://www.linkedin.com/in/chin-ho-fung-a7371626/", "MGB"),

    # ─── ALBERTA PRIMARY CARE NETWORKS ───
    ("Lori (Delores) Apostal", "", "Wood Buffalo PCN / Aspen PCN", "https://www.linkedin.com/in/loriapostal/", "Alberta PCN"),
    ("Donna Berwick", "", "Aspen PCN", "https://www.linkedin.com/in/donna-berwick-b0710aa5/", "Alberta PCN"),
    ("Elizabeth Anne Weninger", "", "Bighorn PCN", "", "Alberta PCN"),
    ("Gerri Abraham", "", "Bonnyville PCN", "https://www.linkedin.com/in/gerri-abraham-8b2a6410a/", "Alberta PCN"),
    ("Rhonda Scott", "", "Borealis PCN", "https://www.linkedin.com/in/rhonda-scott-19137793/", "Alberta PCN"),
    ("Sheryl McCormick", "", "Cold Lake PCN", "https://www.linkedin.com/in/sheryl-mccormick-74b234158/", "Alberta PCN"),
    ("Jenna Macsween", "", "Cold Lake PCN", "https://www.linkedin.com/in/jenna-macsween-9353b4149/", "Alberta PCN"),
    ("Leonie Pieterse", "", "Grande Prairie PCN", "https://www.linkedin.com/in/leonie-pieterse-32137a161/", "Alberta PCN"),
    ("Angela Barreth", "", "Grande Prairie PCN", "", "Alberta PCN"),
    ("Chaitanya Bandaru", "", "Lakeland PCN", "https://www.linkedin.com/in/chaitanya-bandaru-bcom-mba-pgdca-pcp-aca-prosci-727b9591/", "Alberta PCN"),
    ("Njideke Aneke", "", "McLeod River PCN", "https://www.linkedin.com/in/njideka-aneke-39a29627b/", "Alberta PCN"),
    ("Shelley Dickson", "", "McLeod River PCN", "https://www.linkedin.com/in/shelley-dickson-8bb87b164/", "Alberta PCN"),
    ("Anna Foley", "", "Wood Buffalo PCN", "https://www.linkedin.com/in/anna-foley-mn-bn-rn-4aa67739/", "Alberta PCN"),
    ("Rajeanne Bianca", "", "Wood Buffalo PCN", "https://www.linkedin.com/in/rajeanne-bianca-a3a49340/", "Alberta PCN"),
    ("Lorianne Edwards", "", "St. Albert and Sturgeon Primary Care Network", "https://www.linkedin.com/in/lorianne-edwards-1260647a/", "Alberta PCN"),
    ("Melissa D.", "", "St. Albert and Sturgeon Primary Care Network", "https://www.linkedin.com/in/melissa-d-458aa02ab/", "Alberta PCN"),
    ("Duncan Maguire", "", "St. Albert and Sturgeon Primary Care Network", "https://www.linkedin.com/in/duncan-maguire-07468b156/", "Alberta PCN"),
    ("Cathy Morse", "", "St. Albert and Sturgeon Primary Care Network", "https://www.linkedin.com/in/cathy-morse-aaa70711/", "Alberta PCN"),
    ("Parminder Singh", "", "St. Albert and Sturgeon Primary Care Network", "https://www.linkedin.com/in/parminder-singh-21129157/", "Alberta PCN"),
    ("Farah Albert", "", "Sherwood Park Strathcona PCN", "https://www.linkedin.com/in/farah-albert-cpa-ca/", "Alberta PCN"),
    ("Johnson Fatokun", "", "Sherwood Park Strathcona PCN", "https://www.linkedin.com/in/johnson-fatokun-40467526/", "Alberta PCN"),
    ("Tanya Romaniuk", "", "Sherwood Park Strathcona PCN", "https://www.linkedin.com/in/tanya-romaniuk-339068135/", "Alberta PCN"),
    ("Jason Sheehy", "", "Edmonton O-Day'min PCN / Leduc Beaumont Devon PCN", "https://www.linkedin.com/in/jasonjsheehy/", "Alberta PCN"),
    ("John Mah", "", "Edmonton O-Day'min PCN", "https://www.linkedin.com/in/john-mah-2ab1717a/", "Alberta PCN"),
    ("Kelly Parker", "", "Edmonton O-Day'min PCN", "https://www.linkedin.com/in/kelly-parker-9048a3208/", "Alberta PCN"),
    ("Adrienne Barclay", "", "Edmonton O-Day'min PCN", "https://www.linkedin.com/in/adrienne-barclay-84503221/", "Alberta PCN"),
    ("Erin Hay", "", "Edmonton O-Day'min PCN", "https://www.linkedin.com/in/erin-hay-73a20813b/", "Alberta PCN"),
    ("Trevor Haynes", "", "Edmonton O-Day'min PCN", "https://www.linkedin.com/in/trevor-haynes-18572a215/", "Alberta PCN"),
    ("Mustansar Nadeem", "", "Edmonton North PCN", "https://www.linkedin.com/in/mustansar-nadeem/", "Alberta PCN"),
    ("Yetunde Adesina", "", "Edmonton North PCN", "", "Alberta PCN"),
    ("Jaret Farris", "", "Edmonton North PCN", "https://www.linkedin.com/in/jaretfarris/", "Alberta PCN"),
    ("Krystal Tom", "", "Edmonton North PCN", "https://www.linkedin.com/in/krystal-tom-b27a98238/", "Alberta PCN"),
    ("Jagat Pandya", "", "Edmonton North PCN", "", "Alberta PCN"),
    ("Lea Zeltserman", "", "Edmonton North PCN", "", "Alberta PCN"),
    ("Nicole Whitaker", "", "WestView PCN", "https://www.linkedin.com/in/nicole-whitaker-51772168/", "Alberta PCN"),
    ("Nicole Cuyler", "", "WestView PCN", "https://www.linkedin.com/in/ncc-bs/", "Alberta PCN"),
    ("Michelle Enright", "", "WestView PCN", "https://www.linkedin.com/in/michelle-enright-373a1226/", "Alberta PCN"),
    ("Christine Schuster", "", "WestView PCN", "https://www.linkedin.com/in/christine-schuster-819660274/", "Alberta PCN"),
    ("Marti Pickett", "", "Edmonton West PCN", "https://www.linkedin.com/in/martipickett/", "Alberta PCN"),
    ("Shahiem Hartley", "", "Edmonton West PCN", "https://www.linkedin.com/in/shahiem-hartley-08795864/", "Alberta PCN"),
    ("Leeca Sonnema", "", "Edmonton West PCN", "https://www.linkedin.com/in/leeca-sonnema-991baa64/", "Alberta PCN"),
    ("Christina Galluzzo", "", "Edmonton West PCN", "https://www.linkedin.com/in/christina-galluzzo-6180b896/", "Alberta PCN"),
    ("Megan Rogers", "", "Edmonton West PCN", "https://www.linkedin.com/in/megan-rogers-mackey-37a20877/", "Alberta PCN"),
    ("Sanjeet Sandhu", "", "Edmonton West PCN", "https://www.linkedin.com/in/sanjeet-sandhu-822b90194/", "Alberta PCN"),
    ("Andrea Atkins", "", "Edmonton Southside PCN", "https://www.linkedin.com/in/andrea-atkins-1a328587/", "Alberta PCN"),
    ("Kacey Keyko", "", "Edmonton Southside PCN", "https://www.linkedin.com/in/kacey-keyko-2a13037b/", "Alberta PCN"),
    ("Karoline Kiddine", "", "Edmonton Southside PCN", "https://www.linkedin.com/in/karoline-kiddine-10765055/", "Alberta PCN"),
    ("Shanna Kurylo", "", "Edmonton Southside PCN", "", "Alberta PCN"),

    # ─── BRITISH COLUMBIA PRIMARY CARE NETWORKS ───
    ("Tomas Reyes", "", "Surrey-North Delta (SND) Division", "", "BC PCN"),
    ("April Bonise", "", "Surrey-North Delta (SND) Division", "https://www.linkedin.com/in/april-bonise-52a318b0/", "BC PCN"),
    ("Victoria Rotaru", "", "Surrey-North Delta (SND) Division", "https://www.linkedin.com/in/victoria-rotaru-b7240622/", "BC PCN"),
    ("Nidhi Gupta", "", "Surrey-North Delta (SND) Division", "https://www.linkedin.com/in/nidhigk/", "BC PCN"),
    ("Chris Brown", "", "Surrey-North Delta (SND) Division", "https://www.linkedin.com/in/christopheranthonybrown/", "BC PCN"),
    ("Gurveen Dhaliwal", "", "Surrey-North Delta (SND) Division", "", "BC PCN"),
    ("Daphne McRae", "", "Chilliwack Division of Family Practice", "https://www.linkedin.com/in/daphne-mcrae-b8433193/", "BC PCN"),
    ("Marilyn Booth", "", "Chilliwack Division of Family Practice", "https://www.linkedin.com/in/marilyn-booth-3029a0229/", "BC PCN"),
    ("Meghan Helmer", "", "Chilliwack Division of Family Practice", "", "BC PCN"),
    ("Heidi Massie", "", "Chilliwack Division of Family Practice", "", "BC PCN"),
    ("Preet Toor", "", "Chilliwack Division of Family Practice", "https://www.linkedin.com/in/preet-toor/", "BC PCN"),
    ("Karley Holley", "", "Chilliwack Division of Family Practice", "https://www.linkedin.com/in/karley-holley/", "BC PCN"),
    ("Angel Elias", "", "Langley Division of Family Practice", "", "BC PCN"),
    ("Kaitlin Frost", "", "Langley Division of Family Practice", "", "BC PCN"),
    ("Glaiza Ponce", "", "Langley Division of Family Practice", "https://www.linkedin.com/in/glaiza-ponce-741350243/", "BC PCN"),
    ("Manita Dhaliwal", "", "Langley Division of Family Practice", "https://www.linkedin.com/in/manita-dhaliwal-3b9551178/", "BC PCN"),
    ("Valerie Diaz", "", "Langley Division of Family Practice", "", "BC PCN"),
    ("Kyla Davies", "", "Langley Division of Family Practice", "", "BC PCN"),
    ("Sheri Josephson", "", "Abbotsford Division of Family Practice", "https://www.linkedin.com/in/sheri-josephson-80ab2814a/", "BC PCN"),
    ("Kylie Clarke", "", "Abbotsford Division of Family Practice", "", "BC PCN"),
    ("Lencee Dupuis-Baker", "", "Abbotsford Division of Family Practice", "https://www.linkedin.com/in/lencee-dupuis-baker-683b0b318/", "BC PCN"),
    ("Jasmine Sekhon", "", "Abbotsford Division of Family Practice", "https://www.linkedin.com/in/jasminesekhon13/", "BC PCN"),
    ("Danielle Andrews", "", "Abbotsford Division of Family Practice", "https://www.linkedin.com/in/danielle-andrews-58b4b62a7/", "BC PCN"),
    ("Sruti Menon", "", "Abbotsford Division of Family Practice", "https://www.linkedin.com/in/srutimenon/", "BC PCN"),
    ("Justin LoChang", "", "Fraser Health", "https://www.linkedin.com/in/justinlochang/", "BC PCN"),
    ("Veronica de Jong", "", "Burnaby Division of Family Practice", "https://www.linkedin.com/in/veronica-de-jong-68b74326/", "BC PCN"),
    ("Huyanne Le", "", "Burnaby Division of Family Practice", "https://www.linkedin.com/in/huyanne-le-4851154b/", "BC PCN"),
    ("Polly Kainth", "", "Fraser Health", "", "BC PCN"),
    ("Pauline Dan", "", "Fraser Health", "https://www.linkedin.com/in/paulinedan/", "BC PCN"),
    ("Laura Liu", "", "Burnaby PCN", "https://www.linkedin.com/in/laura-liu-675b1420b/", "BC PCN"),
    ("Vera Lefranc", "", "Fraser Northwest Division of Family Practice", "https://www.linkedin.com/in/vera-lefranc-74285118/", "BC PCN"),
    ("Michiko Mazloum", "", "Fraser Northwest Division of Family Practice", "https://www.linkedin.com/in/michiko-mazloum-b479912b/", "BC PCN"),
    ("Jessie Mather-Lingley", "", "Fraser Northwest Division of Family Practice", "https://www.linkedin.com/in/jessie-mather-lingley-408401113/", "BC PCN"),
    ("Melanie Asuncion-Narvaez", "", "Fraser Northwest Division of Family Practice", "", "BC PCN"),
    ("David Chung", "", "Fraser Northwest Division of Family Practice", "", "BC PCN"),
    ("Cindy Young", "", "Fraser Northwest Division of Family Practice", "https://www.linkedin.com/in/cindy-young/", "BC PCN"),
    ("Dermot Kelly", "President and CEO", "Fraser Health", "", "BC PCN"),
    ("Natalie McCarthy", "Vice President, Regional Care Integration", "Fraser Health", "", "BC PCN"),
    ("Sharat Chandra", "Vice President, Planning, Transformation and Infrastructure", "Fraser Health", "", "BC PCN"),
]

# Deduplicate by (name_lower, company_lower), keep first occurrence
seen = set()
unique = []
for row in RAW:
    key = (row[0].strip().lower(), row[2].strip().lower())
    if key not in seen:
        seen.add(key)
        unique.append(row)

found     = [r for r in unique if r[3].strip()]
not_found = [r for r in unique if not r[3].strip()]

out_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(out_dir, exist_ok=True)

# ── Main results CSV ─────────────────────────────────────────────────────────
results_path = os.path.join(out_dir, "linkedin_results.csv")
with open(results_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Name", "Title", "Company", "LinkedIn URL", "Source Sheet"])
    for name, title, company, linkedin, source in found:
        w.writerow([name, title, company, linkedin, source])
    # Separator + not-found section
    w.writerow([])
    w.writerow(["=== LINKEDIN NOT FOUND ===", "", "", "", ""])
    w.writerow(["Name", "Title", "Company", "LinkedIn URL", "Source Sheet"])
    for name, title, company, linkedin, source in not_found:
        w.writerow([name, title, company, "NOT FOUND", source])

print(f"Written: {results_path}")
print(f"  LinkedIn found:     {len(found)}")
print(f"  LinkedIn not found: {len(not_found)}")
print(f"  Total unique:       {len(unique)}")
