import { useMemo } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import type { Locality } from "../../data/nivaas";

// Vite/webpack don't resolve Leaflet's default marker image paths
// automatically — point the default icon at the bundled assets so pins
// render correctly instead of showing broken images.
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

const defaultIcon = L.icon({
    iconUrl: markerIcon,
    iconRetinaUrl: markerIcon2x,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
});

/**
 * Locality centroid coordinates are optional on the backend model until
 * every row has been backfilled. Widening the type locally (rather than
 * requiring the shared `Locality` type to carry them) keeps this component
 * safe to drop in regardless of where the backend is in that rollout.
 */
type LocalityWithCentroid = Locality & {
    centroidLat?: number;
    centroidLon?: number;
};

export function AreaMap({ locality }: { locality: Locality }) {
    const loc = locality as LocalityWithCentroid;

    const center = useMemo<[number, number] | null>(() => {
        if (typeof loc.centroidLat !== "number" || typeof loc.centroidLon !== "number") {
            return null;
        }
        return [loc.centroidLat, loc.centroidLon];
    }, [loc.centroidLat, loc.centroidLon]);

    if (!center) {
        return (
            <div className="flex h-72 flex-col items-center justify-center rounded-3xl border border-white/10 bg-white/5 p-8 text-center">
                <div className="text-5xl">📍</div>

                <h3 className="mt-4 text-lg text-foreground">
                    Location Intelligence Coming Soon
                </h3>

                <p className="mt-3 max-w-sm text-sm text-muted-foreground">
                    NIVAAS currently tracks rental activity, pricing and inventory
                    for this locality. Interactive location mapping is being added
                    as more geographic data becomes available.
                </p>
            </div>
        );
    }

    return (
        <div className="h-[420px] overflow-hidden rounded-2xl border border-white/10">
            <MapContainer
                center={center}
                zoom={13}
                zoomControl={true}
                scrollWheelZoom={false}
                className="h-full w-full"
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={center} icon={defaultIcon}>
                    <Popup>
                        <div>
                            <strong>{locality.name}</strong>
                            <br />
                            Rental activity centre
                        </div>
                    </Popup>
                </Marker>
            </MapContainer>
        </div>
    );
}
