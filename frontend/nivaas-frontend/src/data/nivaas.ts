export type Answers = {
    name: string;
    /** Monthly rent the person is comfortable with, in rupees. */
    budget?: BudgetKey;
    /** Free text — an office, campus, area or "remote". */
    workArea?: string;
    priorities: PriorityKey[];
    lifestyle?: LifestyleKey;
};

export type PriorityKey =
    | "affordable"
    | "quiet"
    | "choices"
    | "spacious"
    | "furnished"
    | "active";
export type LifestyleKey = "student" | "professional" | "couple" | "family";
export type BudgetKey = "under15" | "15to25" | "25to40" | "40to60" | "60plus";

export const budgetSlider = {
    min: 8000,
    max: 80000,
    step: 1000,
} as const;

export const budgetOptions: { key: BudgetKey; label: string; value: number }[] = [
    { key: "under15", label: "Under ₹15k", value: 15000 },
    { key: "15to25", label: "₹15k – ₹25k", value: 25000 },
    { key: "25to40", label: "₹25k – ₹40k", value: 40000 },
    { key: "40to60", label: "₹40k – ₹60k", value: 60000 },
    { key: "60plus", label: "₹60k+", value: 80000 },
];

export function budgetFeel(v: number): string {
    if (v <= 14000) return "Careful with rent, and happy to be.";
    if (v <= 24000) return "Sensible. Space matters more than the address.";
    if (v <= 40000) return "Comfortable — you'd like the walk to be nice too.";
    if (v <= 60000) return "You'd rather live where the evenings happen.";
    return "You want the home to be the easy part.";
}

export const priorityOptions: { key: PriorityKey; label: string }[] = [
    { key: "affordable", label: "Affordable rent" },
    { key: "quiet", label: "Quiet neighbourhood" },
    { key: "choices", label: "More rental options" },
    { key: "spacious", label: "Spacious homes" },
    { key: "furnished", label: "Furnished, move-in ready" },
    { key: "active", label: "Active local life" },
];

export const lifestyleOptions: { key: LifestyleKey; label: string }[] = [
    { key: "student", label: "Student" },
    { key: "professional", label: "Young professional" },
    { key: "couple", label: "Couple" },
    { key: "family", label: "Family" },
];


export type Locality = {
    id: string;
    name: string;
    district: string;
    blurb: string;
    longBlurb: string;
    avgRent: number;
    rentRange: string;
    listings: number;
    overallScore?: number;
    inventoryScore?: number;
    densityScore?: number;
    availability: "Limited" | "Steady" | "Strong" | "Very strong";
    propertyTypes: { label: string; share: number }[];
    furnishing: { label: string; share: number }[];
    bhkMix: { label: string; share: number }[];
    lifestyleFit: LifestyleKey[];
    traits: PriorityKey[];
    nearby: string[];
    coords: { x: number; y: number };
    clusters: { label: string; x: number; y: number }[];
    dayInLife: { morning: string; workday: string; evening: string; weekend: string };
    imagine: string[];
};

export const localities: Locality[] = [
    {
        id: "hsr-layout",
        name: "HSR Layout",
        district: "South-east Bangalore",
        blurb: "A balanced neighbourhood with strong rental availability and excellent value.",
        longBlurb:
            "Sector streets that stay walkable after dark, a rental market that always has something opening up, and just enough café noise to feel like a city.",
        avgRent: 32000,
        rentRange: "₹18,000 – ₹52,000",
        listings: 1840,
        availability: "Very strong",
        propertyTypes: [
            { label: "Apartments", share: 62 },
            { label: "Independent floors", share: 26 },
            { label: "Villas & row houses", share: 12 },
        ],
        furnishing: [
            { label: "Semi-furnished", share: 54 },
            { label: "Fully furnished", share: 28 },
            { label: "Unfurnished", share: 18 },
        ],
        bhkMix: [
            { label: "1 BHK", share: 22 },
            { label: "2 BHK", share: 46 },
            { label: "3 BHK", share: 32 },
        ],
        lifestyleFit: ["professional", "couple", "family"],
        traits: ["choices", "active", "furnished"],
        nearby: ["Koramangala", "Bellandur", "BTM Layout", "Sarjapur Road"],
        coords: { x: 58, y: 68 },
        clusters: [
            { label: "Sector 2 · 1–2 BHK", x: 54, y: 64 },
            { label: "Sector 7 · 2–3 BHK", x: 62, y: 71 },
            { label: "27th Main · furnished", x: 60, y: 62 },
        ],
        dayInLife: {
            morning: "Filter coffee at a corner bakery, joggers looping the sector park.",
            workday: "Fifteen quiet minutes to most south-east offices, laptops open in café corners.",
            evening: "27th Main lights up — bookshops, dosa counters, slow cycling.",
            weekend: "Farmers' market mornings, long brunches, nothing that requires a highway.",
        },
        imagine: [
            "Morning coffee two lanes away.",
            "A commute you never dread.",
            "Something always available when your lease ends.",
        ],
    },
    {
        id: "indiranagar",
        name: "Indiranagar",
        district: "Central-east Bangalore",
        blurb: "Old Bangalore streets carrying the city's most alive evenings.",
        longBlurb:
            "Tree-lined avenues, independent floors above shopfronts, and a furnished rental market built for people who move fast and light.",
        avgRent: 46000,
        rentRange: "₹26,000 – ₹78,000",
        listings: 1120,
        availability: "Strong",
        propertyTypes: [
            { label: "Independent floors", share: 48 },
            { label: "Apartments", share: 44 },
            { label: "Studios", share: 8 },
        ],
        furnishing: [
            { label: "Fully furnished", share: 46 },
            { label: "Semi-furnished", share: 40 },
            { label: "Unfurnished", share: 14 },
        ],
        bhkMix: [
            { label: "1 BHK", share: 30 },
            { label: "2 BHK", share: 44 },
            { label: "3 BHK", share: 26 },
        ],
        lifestyleFit: ["professional", "couple"],
        traits: ["active", "furnished", "choices"],
        nearby: ["Domlur", "Ulsoor", "CV Raman Nagar", "Koramangala"],
        coords: { x: 60, y: 44 },
        clusters: [
            { label: "12th Main · furnished 1 BHK", x: 57, y: 41 },
            { label: "Defence Colony · 2–3 BHK", x: 64, y: 47 },
            { label: "CMH Road · studios", x: 58, y: 49 },
        ],
        dayInLife: {
            morning: "Sunlight through gulmohar, bakeries opening their shutters.",
            workday: "Short hops to central offices; co-working floors within walking distance.",
            evening: "Rooftops, record bars, and streets that stay busy past midnight.",
            weekend: "Boutique browsing, long dinners, friends who never need directions.",
        },
        imagine: [
            "Everything you need within a ten-minute walk.",
            "A furnished home you can move into with two suitcases.",
            "Evenings that never feel like a plan.",
        ],
    },
    {
        id: "jayanagar",
        name: "Jayanagar",
        district: "South Bangalore",
        blurb: "Planned blocks, banyan shade, and homes with room to breathe.",
        longBlurb:
            "The old south, laid out in calm grids. Larger unfurnished homes, longer leases, neighbours who know your name.",
        avgRent: 28000,
        rentRange: "₹14,000 – ₹48,000",
        listings: 960,
        availability: "Steady",
        propertyTypes: [
            { label: "Independent floors", share: 55 },
            { label: "Apartments", share: 38 },
            { label: "Villas", share: 7 },
        ],
        furnishing: [
            { label: "Unfurnished", share: 52 },
            { label: "Semi-furnished", share: 38 },
            { label: "Fully furnished", share: 10 },
        ],
        bhkMix: [
            { label: "1 BHK", share: 18 },
            { label: "2 BHK", share: 42 },
            { label: "3 BHK", share: 40 },
        ],
        lifestyleFit: ["family", "couple"],
        traits: ["quiet", "spacious", "affordable"],
        nearby: ["JP Nagar", "Basavanagudi", "BTM Layout", "Banashankari"],
        coords: { x: 42, y: 68 },
        clusters: [
            { label: "4th Block · 2–3 BHK floors", x: 39, y: 65 },
            { label: "9th Block · family homes", x: 45, y: 72 },
            { label: "Tilaknagar · budget 1 BHK", x: 46, y: 64 },
        ],
        dayInLife: {
            morning: "Temple bells, flower carts, filter coffee in steel tumblers.",
            workday: "Quiet enough to work from the balcony; easy roads south and central.",
            evening: "Walks under old trees, 4th Block shopping, early dinners.",
            weekend: "Lalbagh mornings and markets that have been there for decades.",
        },
        imagine: [
            "A home with an extra room you didn't expect.",
            "Streets that go quiet by ten.",
            "Rent that leaves something behind each month.",
        ],
    },
    {
        id: "whitefield",
        name: "Whitefield",
        district: "East Bangalore",
        blurb: "Gated calm beside the tech corridor, with the widest choice of new homes.",
        longBlurb:
            "Large new-build inventory, generous floor plans and amenity-heavy societies — the easiest place to find a home that matches a spec.",
        avgRent: 30000,
        rentRange: "₹15,000 – ₹60,000",
        listings: 2260,
        availability: "Very strong",
        propertyTypes: [
            { label: "Apartments", share: 78 },
            { label: "Villas & row houses", share: 15 },
            { label: "Independent floors", share: 7 },
        ],
        furnishing: [
            { label: "Semi-furnished", share: 58 },
            { label: "Fully furnished", share: 24 },
            { label: "Unfurnished", share: 18 },
        ],
        bhkMix: [
            { label: "1 BHK", share: 14 },
            { label: "2 BHK", share: 44 },
            { label: "3 BHK", share: 42 },
        ],
        lifestyleFit: ["professional", "family", "couple"],
        traits: ["choices", "spacious", "quiet"],
        nearby: ["Marathahalli", "Brookefield", "Varthur", "KR Puram"],
        coords: { x: 82, y: 40 },
        clusters: [
            { label: "ITPL Road · 2–3 BHK", x: 79, y: 36 },
            { label: "Varthur Road · villas", x: 86, y: 45 },
            { label: "Brookefield · furnished", x: 76, y: 43 },
        ],
        dayInLife: {
            morning: "Clubhouse laps, school buses, coffee on a wide balcony.",
            workday: "Tech parks a shuttle ride away; meetings that end before traffic starts.",
            evening: "Lakefront walks, mall dinners, quiet gated lanes.",
            weekend: "Pools, courts, and a car ride to anywhere east.",
        },
        imagine: [
            "More square feet than the same rent buys elsewhere.",
            "A shortlist that's never empty.",
            "Weekday evenings that actually feel free.",
        ],
    },
    {
        id: "koramangala",
        name: "Koramangala",
        district: "South-east Bangalore",
        blurb: "The city's start-up heart — furnished, fast, endlessly social.",
        longBlurb:
            "Compact furnished homes above busy streets, priced for people who trade space for proximity.",
        avgRent: 42000,
        rentRange: "₹22,000 – ₹72,000",
        listings: 1310,
        availability: "Strong",
        propertyTypes: [
            { label: "Apartments", share: 52 },
            { label: "Independent floors", share: 38 },
            { label: "Studios", share: 10 },
        ],
        furnishing: [
            { label: "Fully furnished", share: 44 },
            { label: "Semi-furnished", share: 42 },
            { label: "Unfurnished", share: 14 },
        ],
        bhkMix: [
            { label: "1 BHK", share: 32 },
            { label: "2 BHK", share: 44 },
            { label: "3 BHK", share: 24 },
        ],
        lifestyleFit: ["student", "professional", "couple"],
        traits: ["active", "furnished", "choices"],
        nearby: ["HSR Layout", "BTM Layout", "Ejipura", "Indiranagar"],
        coords: { x: 54, y: 56 },
        clusters: [
            { label: "5th Block · studios", x: 51, y: 53 },
            { label: "6th Block · furnished 2 BHK", x: 57, y: 58 },
            { label: "80 Feet Road · sharing", x: 53, y: 60 },
        ],
        dayInLife: {
            morning: "Espresso queues and standing meetings on the pavement.",
            workday: "Offices within walking distance; lunch is a decision, not a trip.",
            evening: "Pop-ups, bookstores, food streets that don't close early.",
            weekend: "Football at the turf, brunch that runs into dinner.",
        },
        imagine: [
            "Walking to work more days than not.",
            "A furnished flat that's ready on day one.",
            "Never eating the same dinner twice.",
        ],
    },
    {
        id: "electronic-city",
        name: "Electronic City",
        district: "South Bangalore",
        blurb: "The most rent you'll ever get back — space, quiet and short office runs.",
        longBlurb:
            "Newer societies and independent floors at the lowest ticket sizes in the city, built around the southern tech campuses.",
        avgRent: 19000,
        rentRange: "₹9,000 – ₹34,000",
        listings: 1580,
        availability: "Very strong",
        propertyTypes: [
            { label: "Apartments", share: 70 },
            { label: "Independent floors", share: 24 },
            { label: "Villas", share: 6 },
        ],
        furnishing: [
            { label: "Semi-furnished", share: 56 },
            { label: "Unfurnished", share: 28 },
            { label: "Fully furnished", share: 16 },
        ],
        bhkMix: [
            { label: "1 BHK", share: 30 },
            { label: "2 BHK", share: 46 },
            { label: "3 BHK", share: 24 },
        ],
        lifestyleFit: ["student", "professional", "family"],
        traits: ["affordable", "choices", "spacious", "quiet"],
        nearby: ["Bommasandra", "Chandapura", "Hosa Road", "Begur"],
        coords: { x: 50, y: 88 },
        clusters: [
            { label: "Phase 1 · 1–2 BHK", x: 47, y: 85 },
            { label: "Neeladri Road · budget", x: 53, y: 90 },
            { label: "Hosa Road · new builds", x: 55, y: 83 },
        ],
        dayInLife: {
            morning: "Campus shuttles, tea stalls, an unhurried start.",
            workday: "Ten minutes to the gate — the shortest commute in Bangalore.",
            evening: "Society courts, quiet roads, groceries downstairs.",
            weekend: "Drives out south, or a slow day at home you can afford.",
        },
        imagine: [
            "Rent that costs half of what the north pays.",
            "A commute measured in minutes.",
            "Room for a desk, a bike and a spare bed.",
        ],
    },
    {
        id: "hebbal",
        name: "Hebbal",
        district: "North Bangalore",
        blurb: "Lakeside north, built for airport runs and long-term leases.",
        longBlurb:
            "High-rise living around the lake and Manyata, with a steady supply of larger family homes.",
        avgRent: 34000,
        rentRange: "₹16,000 – ₹58,000",
        listings: 890,
        availability: "Steady",
        propertyTypes: [
            { label: "Apartments", share: 74 },
            { label: "Independent floors", share: 20 },
            { label: "Villas", share: 6 },
        ],
        furnishing: [
            { label: "Semi-furnished", share: 52 },
            { label: "Unfurnished", share: 30 },
            { label: "Fully furnished", share: 18 },
        ],
        bhkMix: [
            { label: "1 BHK", share: 16 },
            { label: "2 BHK", share: 44 },
            { label: "3 BHK", share: 40 },
        ],
        lifestyleFit: ["professional", "family", "couple"],
        traits: ["quiet", "spacious", "choices"],
        nearby: ["Manyata Tech Park", "Yelahanka", "RT Nagar", "Thanisandra"],
        coords: { x: 50, y: 22 },
        clusters: [
            { label: "Lakeside towers · 3 BHK", x: 47, y: 19 },
            { label: "Thanisandra · 2 BHK", x: 55, y: 25 },
            { label: "RT Nagar · budget floors", x: 45, y: 27 },
        ],
        dayInLife: {
            morning: "Mist over the lake, flyover traffic somewhere below you.",
            workday: "Manyata in one straight line; airport in under forty minutes.",
            evening: "Lake walks, high-floor sunsets, quiet lifts.",
            weekend: "North Bangalore drives, big-format shopping, slow Sundays.",
        },
        imagine: [
            "A window that looks over water.",
            "The easiest airport run in the city.",
            "Enough space for a family to grow into.",
        ],
    },
    {
        id: "banashankari",
        name: "Banashankari",
        district: "South-west Bangalore",
        blurb: "An under-noticed south with real space and honest rents.",
        longBlurb:
            "Older independent houses and newer floors, priced well below the eastern corridor and unusually quiet for the size.",
        avgRent: 22000,
        rentRange: "₹10,000 – ₹38,000",
        listings: 1040,
        availability: "Strong",
        propertyTypes: [
            { label: "Independent floors", share: 58 },
            { label: "Apartments", share: 36 },
            { label: "Villas", share: 6 },
        ],
        furnishing: [
            { label: "Unfurnished", share: 48 },
            { label: "Semi-furnished", share: 42 },
            { label: "Fully furnished", share: 10 },
        ],
        bhkMix: [
            { label: "1 BHK", share: 26 },
            { label: "2 BHK", share: 44 },
            { label: "3 BHK", share: 30 },
        ],
        lifestyleFit: ["student", "family", "couple"],
        traits: ["affordable", "quiet", "spacious"],
        nearby: ["Jayanagar", "JP Nagar", "Uttarahalli", "Kathriguppe"],
        coords: { x: 32, y: 76 },
        clusters: [
            { label: "BSK 2nd Stage · floors", x: 29, y: 73 },
            { label: "Kathriguppe · 2 BHK", x: 35, y: 79 },
            { label: "Padmanabhanagar · houses", x: 31, y: 82 },
        ],
        dayInLife: {
            morning: "Temple queues, bakery smell, streets that wake up early.",
            workday: "Metro south to the centre; work-from-home floors with real balconies.",
            evening: "Park benches, roadside chaat, no honking after nine.",
            weekend: "Turahalli trails, family lunches, markets on foot.",
        },
        imagine: [
            "A three-bedroom for a two-bedroom price.",
            "Neighbours instead of lobbies.",
            "Green edges of the city ten minutes away.",
        ],
    },
];

/** Known Bangalore work/study anchors, used only to interpret free text. */
const workAnchors: { name: string; keys: string[]; near: string[] }[] = [
    { name: "Koramangala", keys: ["koramangala"], near: ["koramangala", "hsr-layout", "indiranagar"] },
    { name: "Whitefield", keys: ["whitefield", "itpl", "brookefield"], near: ["whitefield", "hsr-layout", "indiranagar"] },
    { name: "Electronic City", keys: ["electronic city", "e city", "ecity", "bommasandra", "infosys", "wipro"], near: ["electronic-city", "banashankari", "jayanagar"] },
    { name: "Manyata Tech Park", keys: ["manyata", "manyatha", "thanisandra", "nagawara"], near: ["hebbal", "jayanagar", "indiranagar"] },
    { name: "HSR Layout", keys: ["hsr"], near: ["hsr-layout", "koramangala", "electronic-city"] },
    { name: "Hebbal", keys: ["hebbal", "yelahanka", "airport"], near: ["hebbal", "jayanagar", "whitefield"] },
    { name: "Jayanagar", keys: ["jayanagar", "basavanagudi"], near: ["jayanagar", "banashankari", "hsr-layout"] },
    { name: "MG Road", keys: ["mg road", "cbd", "shivajinagar", "richmond", "cunningham"], near: ["indiranagar", "jayanagar", "koramangala"] },
    { name: "Sarjapur Road", keys: ["sarjapur", "bellandur", "ecospace", "embassy tech"], near: ["hsr-layout", "whitefield", "koramangala"] },
    { name: "Marathahalli", keys: ["marathahalli", "kundalahalli"], near: ["whitefield", "hsr-layout", "indiranagar"] },
    { name: "Bannerghatta Road", keys: ["bannerghatta", "jp nagar", "arekere"], near: ["jayanagar", "banashankari", "electronic-city"] },
    { name: "Christ University", keys: ["christ", "dairy circle", "hosur road"], near: ["koramangala", "jayanagar", "hsr-layout"] },
    { name: "Bangalore University", keys: ["bangalore university", "jnanabharathi", "mysore road", "rv college", "pes"], near: ["banashankari", "jayanagar", "electronic-city"] },
    { name: "IIM Bangalore", keys: ["iim"], near: ["banashankari", "jayanagar", "electronic-city"] },
    { name: "Domlur", keys: ["domlur", "old airport road", "indiranagar", "ulsoor"], near: ["indiranagar", "koramangala", "whitefield"] },
];

export const workAreas = workAnchors.map((w) => ({
    name: w.name,
}));

function anchorFor(text?: string) {
    if (!text) return null;
    const t = text.trim().toLowerCase();
    if (!t) return null;
    return (
        workAnchors.find((a) => a.keys.some((k) => t.includes(k))) ??
        workAnchors.find((a) => t.includes(a.name.toLowerCase())) ??
        null
    );
}

export function isRemote(text?: string) {
    return !!text && /remote|home|wfh|anywhere|freelanc/.test(text.trim().toLowerCase());
}

/** A short, honest line about the daily run — no invented distances. */
export function commuteNote(l: Locality, workArea?: string): string {
    const place = workArea?.trim();
    if (!place) return l.dayInLife.workday;
    if (isRemote(place)) {
        return `Working from home, ${l.name} gives you ${l.longBlurb.split(",")[0]?.toLowerCase().trim()} to look at between calls.`;
    }
    const anchor = anchorFor(place);
    const idx = anchor ? anchor.near.indexOf(l.id) : -1;
    if (idx === 0) {
        return `${place} is right on your doorstep — most people here make that run without leaving the neighbourhood.`;
    }
    if (idx > 0) {
        return `Convenient if your routine revolves around ${place}; it's one of the runs people from ${l.name} do every day.`;
    }
    return `${place} is a proper cross-city run from ${l.name} — worth it only if you'd rather come home to ${l.nearby[0]}'s side of town.`;
}

/** Distinct personality lines — no real-estate boilerplate. */
export const personality: Record<string, string> = {
    "hsr-layout":
        "Sector roads you can actually walk at night, bakeries that know regulars, and a young crowd that treats the neighbourhood like a campus.",
    indiranagar:
        "Gulmohar shade over old independent houses, shopfronts below flats, and streets that stay awake long after the rest of the city folds.",
    jayanagar:
        "Tree-lined roads, older homes, and a neighbourhood that slows down after dark.",
    whitefield:
        "Wide roads, gate guards who wave, and evenings measured in clubhouse laps rather than restaurant queues.",
    koramangala:
        "Small flats above loud lanes, laptops in every café window, and a permanent sense that something is being started nearby.",
    "electronic-city":
        "Newer buildings, uncomplicated streets, and a rhythm set entirely by the campuses at the end of the road.",
    hebbal:
        "High floors over a lake, mist in the mornings, and lifts that are quiet because everyone leaves early.",
    banashankari:
        "Old south Bangalore that never bothered performing — bakeries, temple lanes, and houses with more room than you'd expect.",
};

export type Reason = string;

export type Match = {
    locality: Locality;
    reasons: Reason[];
};

export const matchLabels = ["Your best match", "Worth exploring", "Hidden gem"];

export function inr(n: number) {
    return `₹${n.toLocaleString("en-IN")}`;
}

export function byId(id: string) {
    return localities.find((l) => l.id === id);
}
