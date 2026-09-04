"use client";

import { useEffect, useState } from "react";
import { fetchHubs, fetchPrediction, Hub, PredictionData } from "@/lib/api";
import {
  Anchor,
  CloudLightning,
  Radio,
  Activity,
  RefreshCw,
  Crosshair,
  Radar,
  AlertOctagon,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
} from "recharts";

export default function AegisTerminal() {
  const [hubs, setHubs] = useState<Hub[]>([]);
  const [selectedHub, setSelectedHub] = useState<string>("EG_SUE");
  const [prediction, setPrediction] = useState<PredictionData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchHubs().then((data) => {
      setHubs(data.hubs);
      if (data.hubs.length > 0) setSelectedHub(data.hubs[0].id);
    });
  }, []);

  useEffect(() => {
    if (!selectedHub) return;
    setLoading(true);
    fetchPrediction(selectedHub).then((data) => {
      setPrediction(data);
      setLoading(false);
    });
  }, [selectedHub]);

  const chartData = prediction
    ? Object.entries(prediction.shap_contributions).map(([key, value]) => ({
        name: key.replace(/_/g, " ").toUpperCase(),
        impact: value,
      }))
    : [];

  // Dynamic Theme Colors based on Anomaly Score
  const getTheme = (score: number) => {
    if (score >= 75)
      return {
        color: "text-rose-500",
        glow: "shadow-[0_0_40px_rgba(244,63,94,0.4)]",
        border: "border-rose-500/50",
        bg: "bg-rose-500/10",
        hex: "#f43f5e",
      };
    if (score >= 40)
      return {
        color: "text-amber-400",
        glow: "shadow-[0_0_40px_rgba(251,191,36,0.3)]",
        border: "border-amber-400/50",
        bg: "bg-amber-400/10",
        hex: "#fbbf24",
      };
    return {
      color: "text-cyan-400",
      glow: "shadow-[0_0_40px_rgba(34,211,238,0.3)]",
      border: "border-cyan-400/50",
      bg: "bg-cyan-400/10",
      hex: "#22d3ee",
    };
  };

  const theme = prediction ? getTheme(prediction.anomaly_score) : getTheme(0);

  return (
    <div className="min-h-screen bg-[#050505] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-950/20 via-[#050505] to-[#050505] text-slate-300 font-sans p-4 sm:p-8 selection:bg-cyan-500/30">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Terminal Header */}
        <header className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-white/10">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Radar className="w-8 h-8 text-cyan-400 animate-[spin_4s_linear_infinite]" />
              <h1 className="text-4xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-indigo-400 to-fuchsia-500">
                AEGIS
              </h1>
            </div>
            <p className="text-xs font-mono text-slate-500 tracking-widest uppercase">
              Unsupervised Anomaly Detection // Real-time Telemetry
            </p>
          </div>

          <div className="flex items-center gap-3 bg-white/5 p-1.5 rounded-xl border border-white/10 backdrop-blur-md">
            <select
              value={selectedHub}
              onChange={(e) => setSelectedHub(e.target.value)}
              className="bg-transparent text-cyan-50 font-mono text-sm px-4 py-2 focus:outline-none cursor-pointer appearance-none"
            >
              {hubs.map((hub) => (
                <option
                  key={hub.id}
                  value={hub.id}
                  className="bg-slate-900 text-white"
                >
                  [{hub.id}] {hub.name}
                </option>
              ))}
            </select>
            <button
              onClick={() => {
                setLoading(true);
                fetchPrediction(selectedHub).then((data) => {
                  setPrediction(data);
                  setLoading(false);
                });
              }}
              className="p-2 bg-white/5 hover:bg-cyan-500/20 rounded-lg text-cyan-400 transition-all"
            >
              <RefreshCw
                className={`w-4 h-4 ${loading ? "animate-spin" : ""}`}
              />
            </button>
          </div>
        </header>

        {prediction && (
          <div className="space-y-6">
            {/* Top Array: Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {/* Master Risk Index - Spans 2 cols */}
              <div
                className={`col-span-1 md:col-span-2 relative overflow-hidden rounded-3xl bg-black/40 border ${theme.border} backdrop-blur-xl p-8 ${theme.glow} transition-all duration-500 flex flex-col justify-between`}
              >
                <div className="flex justify-between items-start mb-4">
                  <span className="font-mono text-xs text-slate-400 tracking-widest uppercase">
                    Isolation Forest Score
                  </span>
                  <div
                    className={`px-3 py-1 text-[10px] font-black uppercase tracking-widest rounded-full border ${theme.border} ${theme.bg} ${theme.color} flex items-center gap-2`}
                  >
                    <Activity className="w-3 h-3" /> {prediction.status}
                  </div>
                </div>
                <div className="flex items-baseline gap-2">
                  <span
                    className={`text-8xl font-black tracking-tighter ${theme.color}`}
                  >
                    {prediction.anomaly_score}
                  </span>
                  <span className="text-xl text-slate-600 font-mono">/100</span>
                </div>
              </div>

              {/* Telemetry: Port */}
              <div className="bg-white/[0.02] border border-white/5 rounded-3xl p-6 backdrop-blur-md flex flex-col justify-between hover:bg-white/[0.04] transition-colors">
                <div className="flex justify-between items-start">
                  <span className="font-mono text-[10px] text-slate-500 tracking-widest uppercase">
                    Congestion Array
                  </span>
                  <Anchor className="w-4 h-4 text-indigo-400" />
                </div>
                <div>
                  <div className="text-4xl font-light text-white mb-1">
                    {prediction.features.port_congestion_score}
                  </div>
                  <div className="text-xs font-mono text-indigo-400/80">
                    Δ VOL:{" "}
                    {(prediction.features.port_volume_drop_pct * 100).toFixed(
                      1,
                    )}
                    %
                  </div>
                </div>
              </div>

              {/* Telemetry: Weather & News Combo */}
              <div className="flex flex-col gap-4">
                <div className="flex-1 bg-white/[0.02] border border-white/5 rounded-2xl p-4 backdrop-blur-md flex items-center justify-between">
                  <div>
                    <span className="block font-mono text-[9px] text-slate-500 tracking-widest uppercase mb-1">
                      Meteo Severity
                    </span>
                    <span className="text-2xl font-light text-white">
                      {prediction.features.weather_severity_score}
                    </span>
                  </div>
                  <CloudLightning className="w-6 h-6 text-fuchsia-400 opacity-50" />
                </div>
                <div className="flex-1 bg-white/[0.02] border border-white/5 rounded-2xl p-4 backdrop-blur-md flex items-center justify-between">
                  <div>
                    <span className="block font-mono text-[9px] text-slate-500 tracking-widest uppercase mb-1">
                      GDELT Incident
                    </span>
                    <span className="text-2xl font-light text-white">
                      {prediction.features.news_risk_score}
                    </span>
                  </div>
                  <Radio className="w-6 h-6 text-amber-400 opacity-50" />
                </div>
              </div>
            </div>

            {/* Lower Array: Analytics & Playbook */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* SHAP Diagnostics */}
              <div className="lg:col-span-2 bg-white/[0.02] border border-white/5 rounded-3xl p-6 backdrop-blur-md">
                <div className="flex items-center gap-2 mb-6">
                  <Crosshair className="w-4 h-4 text-cyan-400" />
                  <h3 className="font-mono text-xs text-slate-300 tracking-widest uppercase">
                    SHAP Decision Matrix
                  </h3>
                </div>

                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={chartData}
                      layout="vertical"
                      margin={{ top: 0, right: 20, left: 110, bottom: 0 }}
                    >
                      <XAxis
                        type="number"
                        stroke="#334155"
                        fontSize={10}
                        tickFormatter={(val) => val.toFixed(2)}
                      />
                      <YAxis
                        dataKey="name"
                        type="category"
                        stroke="#94a3b8"
                        fontSize={9}
                        width={100}
                        axisLine={false}
                        tickLine={false}
                      />
                      <Tooltip
                        cursor={{ fill: "rgba(255,255,255,0.05)" }}
                        contentStyle={{
                          backgroundColor: "#0f172a",
                          border: "1px solid rgba(34,211,238,0.2)",
                          borderRadius: "12px",
                          fontFamily: "monospace",
                          fontSize: "11px",
                        }}
                      />
                      <ReferenceLine
                        x={0}
                        stroke="#475569"
                        strokeDasharray="3 3"
                      />
                      <Bar dataKey="impact" radius={[0, 4, 4, 0]} barSize={12}>
                        {chartData.map((entry, index) => (
                          <Cell
                            key={`cell-${index}`}
                            fill={entry.impact > 0 ? "#f43f5e" : "#22d3ee"}
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <div className="flex justify-end gap-6 mt-4 font-mono text-[9px] text-slate-500 uppercase tracking-widest">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-rose-500 shadow-[0_0_10px_#f43f5e]"></span>{" "}
                    Escalates Risk
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_10px_#22d3ee]"></span>{" "}
                    Mitigates Risk
                  </div>
                </div>
              </div>

              {/* Automated Directive */}
              <div className="bg-black/40 border border-white/5 rounded-3xl p-6 backdrop-blur-xl flex flex-col relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-5">
                  <AlertOctagon className="w-32 h-32" />
                </div>

                <h3 className="font-mono text-xs text-slate-500 tracking-widest uppercase mb-4">
                  Directive Node
                </h3>

                <div className="flex-1 font-mono text-sm text-slate-300 leading-relaxed z-10">
                  <span className="text-cyan-500">&gt; EXECUTE_PROTOCOL:</span>{" "}
                  <br />
                  <br />
                  <span className={theme.color}>
                    {prediction.recommendation}
                  </span>
                </div>

                <div className="mt-6 pt-4 border-t border-white/10 z-10">
                  <div className="flex justify-between items-center font-mono text-[9px] text-slate-500 uppercase">
                    <span>Target: {prediction.hub_id}</span>
                    <span>
                      Sync:{" "}
                      {new Date(prediction.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
