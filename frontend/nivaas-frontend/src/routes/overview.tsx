import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Building2, Map, MapPin, Train } from "lucide-react";

import { KpiCard, KpiCardSkeleton } from "@/components/overview/kpi-card";
import { MetroMap, type MetroStation } from "@/components/overview/metro-map";

const API = import.meta.env.VITE_API_BASE_URL;

interface AnalyticsResponse {
    localities?: number;
    wards?: number;
    metroStations?: number;
    listings?: number;
    metroStationList?: MetroStation[];
}

async function fetchAnalytics() {
    const { data } = await axios.get(`${API}/analytics`);
    return data;
}

export function Overview() {
    const { data, isLoading } = useQuery({
        queryKey: ["analytics"],
        queryFn: fetchAnalytics,
    });

    const analytics = (data ?? {}) as AnalyticsResponse;

    return (
        <div className="min-h-screen bg-ink px-8 py-10">

            <div className="mx-auto max-w-7xl">

                <h1 className="text-5xl font-bold text-white">
                    Bangalore Rental Intelligence Platform
                </h1>

                <p className="mt-4 max-w-3xl text-white/60">
                    AI-powered rental intelligence built on FastAPI, PostgreSQL,
                    PostGIS and real Bangalore geospatial datasets.
                </p>

                <div className="mt-12 grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">

                    {isLoading ? (
                        <>
                            <KpiCardSkeleton />
                            <KpiCardSkeleton />
                            <KpiCardSkeleton />
                            <KpiCardSkeleton />
                        </>
                    ) : (
                        <>
                            <KpiCard
                                label="Localities"
                                value={analytics.localities}
                                icon={MapPin}
                            />

                            <KpiCard
                                label="Metro Stations"
                                value={analytics.metroStations}
                                icon={Train}
                            />

                            <KpiCard
                                label="BBMP Wards"
                                value={analytics.wards}
                                icon={Map}
                            />

                            <KpiCard
                                label="Listings"
                                value={analytics.listings}
                                icon={Building2}
                            />
                        </>
                    )}

                </div>

                <div className="mt-10">

                    <MetroMap
                        loading={isLoading}
                        stations={analytics.metroStationList ?? []}
                    />

                </div>

            </div>

        </div>
    );
}
