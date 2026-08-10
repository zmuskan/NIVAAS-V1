import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export interface MetroStation {
    id?: string | number;
    name: string;
    lat: number;
    lng: number;
}

interface MetroMapProps {
    stations: MetroStation[];
    loading?: boolean;
}

const center: [number, number] = [12.9716, 77.5946];

const metroIcon = new L.Icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    iconRetinaUrl:
        "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
    shadowUrl:
        "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

export function MetroMap({
    stations,
    loading = false,
}: MetroMapProps) {
    return (
        <div className="relative h-[420px] overflow-hidden rounded-2xl border border-white/10">
            <MapContainer
                center={center}
                zoom={11}
                scrollWheelZoom={false}
                className="h-full w-full"
            >
                <TileLayer
                    attribution="© OpenStreetMap contributors"
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {stations.map((station) => (
                    <Marker
                        key={station.id ?? `${station.lat}-${station.lng}`}
                        position={[station.lat, station.lng]}
                        icon={metroIcon}
                    >
                        <Popup>{station.name}</Popup>
                    </Marker>
                ))}
            </MapContainer>

            {loading && (
                <div className="absolute inset-0 flex items-center justify-center bg-[#0B0D11]/60">
                    <p className="text-sm text-white">
                        Loading Metro Stations...
                    </p>
                </div>
            )}
        </div>
    );
}
