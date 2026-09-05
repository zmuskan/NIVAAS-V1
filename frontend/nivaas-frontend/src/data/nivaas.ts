export type Answers = {
    name: string;
    budget?: BudgetKey;
    workArea?: string;
    priorities: PriorityKey[];
    lifestyle?: LifestyleKey;
};

export type PriorityKey =
    | "student"
    | "family"
    | "affordable"
    | "active";

export type LifestyleKey = "student" | "professional" | "couple" | "family";
export type BudgetKey = "under15" | "15to25" | "25to40" | "40to60" | "60plus";

export const budgetSlider = {
    min: 8000,
    max: 80000,
    step: 1000,
} as const;

export const budgetOptions: { key: BudgetKey; label: string; value: number }[] = [
    { key: "under15", label: "Under 15k", value: 15000 },
    { key: "15to25", label: "15k - 25k", value: 25000 },
    { key: "25to40", label: "25k - 40k", value: 40000 },
    { key: "40to60", label: "40k - 60k", value: 60000 },
    { key: "60plus", label: "60k+", value: 80000 },
];

export function budgetFeel(v: number): string {
    if (v <= 14000) return "Careful with rent, and happy to be.";
    if (v <= 24000) return "Sensible. Space matters more than the address.";
    if (v <= 40000) return "Comfortable - you'd like the walk to be nice too.";
    if (v <= 60000) return "You'd rather live where the evenings happen.";
    return "You want the home to be the easy part.";
}

export const priorityOptions: { key: PriorityKey; label: string }[] = [
    { key: "affordable", label: "Affordable Rent" },
    { key: "family", label: "Short Commute" },
    { key: "active", label: "Active Lifestyle" },
    { key: "student", label: "High Availability" },
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
    avgRent?: number;
    minRent?: number;
    maxRent?: number;
    listingCount?: number;
    highlights?: string[];
    propertyCount?: number;
    overallScore?: number;
    inventoryScore?: number;
    densityScore?: number;
    centroidLat?: number;
    centroidLon?: number;
};

export function isRemote(text?: string) {
    return !!text && /remote|home|wfh|anywhere|freelanc/.test(text.trim().toLowerCase());
}

export function commuteNote(l: Locality, workArea?: string): string {
    const place = workArea?.trim();
    if (!place) return "Commute information unavailable.";
    if (isRemote(place)) return `Working from home in ${l.name}.`;
    return `Commute information for ${l.name} and ${place} is unavailable.`;
}

export type Reason = string;

export type Match = {
    locality: Locality;
    reasons: Reason[];
};

export const matchLabels = ["Your best match", "Worth exploring", "Hidden gem"];

export function inr(n: number) {
    return `Rs ${n.toLocaleString("en-IN")}`;
}
