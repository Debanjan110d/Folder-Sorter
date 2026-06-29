import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";
import { CheckCircle2, CircleDot, Clock, Milestone } from "lucide-react";

export default function RoadmapPage() {
  const items = [
    {
      version: "v1.0.3",
      title: "Windows Release & Vercel Migration",
      date: "June 2026",
      status: "released",
      desc: "Polished production-ready Windows x64 binary installer, complete migration of web/scripts hosting to Vercel, and direct integration with GitHub Release binaries.",
      details: ["Windows binary-only installer install.ps1", "Vercel landing page & documentation", "Automatic version bumps and checks"]
    },
    {
      version: "v1.1.0",
      title: "Linux & macOS Executables",
      date: "Q3 2026",
      status: "planned",
      desc: "Re-enable GitHub Actions cross-compilation pipeline to deliver native executable packages for Linux x64, Linux ARM64, macOS Intel, and Apple Silicon.",
      details: ["Bash installer script install.sh", "Static executables packaged via PyInstaller", "Cross-platform path diagnostics"]
    },
    {
      version: "v1.2.0",
      title: "Automatic Dynamic Upgrades",
      date: "Q4 2026",
      status: "planned",
      desc: "Implement fully automated background update command so users can upgrade their Folder Sorter binary directly through terminal.",
      details: ["folder-sorter update direct execution", "SHA256 signature auto-verification", "Rollback support for failed upgrades"]
    },
    {
      version: "v2.0.0",
      title: "Plugin System & Web dashboard",
      date: "2027",
      status: "planned",
      desc: "Architect a custom sorting plugin system allowing users to write Python scripts for custom sorting rules, along with a clean web browser diagnostic dashboard.",
      details: ["Custom python rule hooks", "Browser-based file grouping preview", "Cloud synchronization of user categories"]
    }
  ];

  return (
    <>
      <Navbar />

      <main className="flex-grow bg-[#030712] text-gray-100 py-12 lg:py-20 selection:bg-indigo-500/30">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h1 className="text-3xl font-extrabold tracking-tight sm:text-5xl text-white flex items-center justify-center gap-3">
              <Milestone className="h-10 w-10 text-indigo-500" />
              <span>Project Roadmap</span>
            </h1>
            <p className="mt-4 text-gray-400">
              Follow along with our development schedule. Windows x64 support is production-ready; Linux, macOS, and advanced features are in active planning.
            </p>
          </div>

          {/* Roadmap Timeline */}
          <div className="relative border-l border-gray-800 ml-4 space-y-12 pb-8">
            {items.map((item, idx) => (
              <div key={idx} className="relative pl-8">
                {/* Timeline Dot Icon */}
                <div className="absolute -left-4 top-1.5">
                  {item.status === "released" ? (
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 shadow-lg shadow-indigo-500/10">
                      <CheckCircle2 className="h-5 w-5" />
                    </div>
                  ) : (
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-900 text-gray-500 border border-gray-800">
                      <CircleDot className="h-4 w-4 text-indigo-500/50" />
                    </div>
                  )}
                </div>

                {/* Content Block */}
                <div className="bg-[#070b19] border border-gray-800 rounded-xl p-6 shadow-2xl backdrop-blur-md">
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                        {item.version}
                      </span>
                      <h3 className="text-lg font-bold text-white">{item.title}</h3>
                    </div>
                    <span className="text-xs text-gray-500 font-semibold">{item.date}</span>
                  </div>

                  <p className="text-sm text-gray-400 leading-relaxed mb-4">{item.desc}</p>

                  <div className="border-t border-gray-900 pt-4">
                    <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Key Deliverables</h4>
                    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1 text-xs text-gray-400">
                      {item.details.map((detail, dIdx) => (
                        <li key={dIdx} className="flex items-center gap-2">
                          <span className="h-1 w-1 rounded-full bg-indigo-500" />
                          <span>{detail}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
}
