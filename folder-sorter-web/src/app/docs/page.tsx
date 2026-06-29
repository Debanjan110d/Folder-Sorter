"use client";

import { useState } from "react";
import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";
import { Terminal, Settings, ShieldCheck, Undo2, Play, BookOpen, AlertCircle, HelpCircle, Key } from "lucide-react";

export default function DocsPage() {
  const [activeSection, setActiveSection] = useState("getting-started");

  const sections = [
    { id: "getting-started", label: "Getting Started", icon: BookOpen },
    { id: "commands", label: "Commands & Subcommands", icon: Terminal },
    { id: "configuration", label: "Custom Configuration", icon: Settings },
    { id: "undo", label: "Undo System", icon: Undo2 },
    { id: "doctor", label: "Doctor Diagnostics", icon: ShieldCheck },
    { id: "faq", label: "Frequently Asked Questions", icon: HelpCircle },
    { id: "troubleshooting", label: "Troubleshooting & PATH", icon: AlertCircle }
  ];

  const scrollTo = (id: string) => {
    setActiveSection(id);
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <>
      <Navbar />

      <main className="flex-grow bg-[#030712] text-gray-100 selection:bg-indigo-500/30">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
          <div className="flex flex-col lg:flex-row gap-12">
            {/* Sidebar Navigation */}
            <aside className="lg:w-64 shrink-0">
              <div className="sticky top-24 space-y-1">
                <div className="text-xs font-bold text-gray-500 uppercase tracking-wider px-3 mb-3">Documentation</div>
                {sections.map((sec) => {
                  const Icon = sec.icon;
                  return (
                    <button
                      key={sec.id}
                      onClick={() => scrollTo(sec.id)}
                      className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm font-medium transition-all ${
                        activeSection === sec.id
                          ? "bg-indigo-600/10 text-indigo-400 border border-indigo-500/20 font-bold"
                          : "text-gray-400 border border-transparent hover:bg-gray-800/40 hover:text-gray-200"
                      }`}
                    >
                      <Icon className="h-4 w-4 shrink-0" />
                      <span>{sec.label}</span>
                    </button>
                  );
                })}
              </div>
            </aside>

            {/* Main Content Area */}
            <div className="flex-1 max-w-3xl space-y-16">
              {/* Getting Started */}
              <section id="getting-started" className="scroll-mt-24">
                <h1 className="text-3xl font-extrabold text-white mb-4">Getting Started</h1>
                <p className="text-gray-400 leading-relaxed mb-6">
                  Folder Sorter is an open-source CLI program written in Python that helps developers, photographers, and general PC users maintain clean folder systems. It acts as an automated sorting butler, scanning files, grouping them by rules, and cleanly placing them into destination categories.
                </p>
                <div className="bg-[#0b1021] border border-gray-850 rounded-xl p-5 mb-6">
                  <h3 className="text-sm font-bold text-white mb-2">How to launch:</h3>
                  <p className="text-gray-400 text-sm mb-4">
                    After completing the one-command installation, run the utility without arguments to enter the **Interactive Menu Mode**:
                  </p>
                  <pre className="rounded bg-black/40 p-3 text-xs text-indigo-400 border border-gray-900 font-mono">
                    folder-sorter
                  </pre>
                </div>
                <p className="text-gray-400 leading-relaxed">
                  Interactive mode guides you through selecting target directories, configuring recursive subdirectory traversal, and performing dry runs without having to remember any command-line options.
                </p>
              </section>

              {/* Commands & Subcommands */}
              <section id="commands" className="scroll-mt-24">
                <h2 className="text-2xl font-extrabold text-white mb-4">Commands & Subcommands</h2>
                <p className="text-gray-400 leading-relaxed mb-6">
                  Use subcommands directly from PowerShell or Command Prompt for direct execution or to integrate Folder Sorter into automated background shell scripts.
                </p>

                <div className="space-y-8">
                  <div className="border-l-2 border-indigo-500 pl-4 space-y-2">
                    <h3 className="font-bold text-white text-md">sort [DIRECTORY]</h3>
                    <p className="text-gray-400 text-sm">Organizes target directory (defaults to current directory). Options:</p>
                    <ul className="text-xs text-gray-500 space-y-1 list-disc list-inside">
                      <li><code className="text-gray-300">-m, --mode [by-type|by-date]</code>: Sorting mode. Default is <code className="text-gray-300">by-type</code>.</li>
                      <li><code className="text-gray-300">-d, --dry-run</code>: Show moves in log without writing changes.</li>
                      <li><code className="text-gray-300">-r, --recursive</code>: Traverses subdirectories recursively.</li>
                      <li><code className="text-gray-300">-v, --verbose</code>: Display verbose file move operations.</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-purple-500 pl-4 space-y-2">
                    <h3 className="font-bold text-white text-md">undo</h3>
                    <p className="text-gray-400 text-sm">Reverse the last folder sorting run. Re-scans sqlite database moves and puts everything back exactly where it was found.</p>
                  </div>

                  <div className="border-l-2 border-pink-500 pl-4 space-y-2">
                    <h3 className="font-bold text-white text-md">doctor</h3>
                    <p className="text-gray-400 text-sm">Run write diagnostics checks, SQLite database health checks, and Python package dependency validation.</p>
                  </div>

                  <div className="border-l-2 border-cyan-500 pl-4 space-y-2">
                    <h3 className="font-bold text-white text-md">config</h3>
                    <p className="text-gray-400 text-sm">Manage configuration variables. Subcommands: <code className="text-gray-300">show</code>, <code className="text-gray-300">add [category] [extension]</code>, <code className="text-gray-300">remove [category] [extension]</code>.</p>
                  </div>
                </div>
              </section>

              {/* Custom Configuration */}
              <section id="configuration" className="scroll-mt-24">
                <h2 className="text-2xl font-extrabold text-white mb-4">Custom Configuration</h2>
                <p className="text-gray-400 leading-relaxed mb-4">
                  Folder Sorter uses default extension mappings to group files, but you can dynamically customize mappings using CLI commands or by editing the JSON configuration file directly.
                </p>
                <p className="text-gray-400 leading-relaxed mb-6">
                  Configurations are saved globally under your home directory:
                  <code className="bg-[#0b1021] text-indigo-400 border border-gray-800 rounded px-1.5 py-0.5 ml-1 text-xs sm:text-sm font-mono">
                    ~/.folder-sorter/config.json
                  </code>
                </p>

                <div className="bg-[#0b1021] border border-gray-850 rounded-xl p-5 space-y-4">
                  <div>
                    <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2">View active mapping rules:</h4>
                    <pre className="rounded bg-black/40 p-2.5 text-xs text-gray-300 font-mono border border-gray-900">
                      folder-sorter config show
                    </pre>
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Add a new extension mapping:</h4>
                    <pre className="rounded bg-black/40 p-2.5 text-xs text-gray-300 font-mono border border-gray-900">
                      folder-sorter config add Code .go
                    </pre>
                  </div>
                </div>
              </section>

              {/* Undo System */}
              <section id="undo" className="scroll-mt-24">
                <h2 className="text-2xl font-extrabold text-white mb-4">Undo System</h2>
                <p className="text-gray-400 leading-relaxed mb-6">
                  Mistakes happen. If you sorted the wrong directory, Folder Sorter has an integrated database safety net. When files are moved, a record containing the old path, new path, and transaction timestamp is logged into a local SQLite database under `~/.folder-sorter/history.json` or `history.db`.
                </p>
                <div className="border border-indigo-500/20 bg-indigo-500/5 rounded-xl p-5 text-sm text-gray-400 leading-relaxed">
                  <span className="font-bold text-white block mb-1">💡 Idempotent Safety</span>
                  To run a dry run of the undo operation, run `folder-sorter undo --dry-run`. This shows you what files would move without actually changing the filesystem, confirming it's safe to run the actual restoration.
                </div>
              </section>

              {/* Doctor Diagnostics */}
              <section id="doctor" className="scroll-mt-24">
                <h2 className="text-2xl font-extrabold text-white mb-4">Doctor Diagnostics</h2>
                <p className="text-gray-400 leading-relaxed mb-6">
                  If Folder Sorter fails or throws permission errors, run the diagnostic doctor:
                </p>
                <pre className="rounded bg-black/40 p-4 text-sm text-white font-mono border border-gray-900 mb-6">
                  folder-sorter doctor
                </pre>
                <p className="text-gray-400 leading-relaxed">
                  The doctor command performs a validation checklist on Python runtime version, folder read/write permissions, database consistency, and additional libraries (Pillow for image resolution sorting).
                </p>
              </section>

              {/* FAQ */}
              <section id="faq" className="scroll-mt-24">
                <h2 className="text-2xl font-extrabold text-white mb-4">Frequently Asked Questions</h2>
                <div className="space-y-6">
                  <div>
                    <h4 className="font-semibold text-white text-sm">Will Folder Sorter overwrite my existing files?</h4>
                    <p className="text-gray-400 text-sm mt-1">
                      No. If a file with the same name already exists in the destination category folder, Folder Sorter automatically renames the incoming file (e.g. `document_1.pdf`) to avoid data collisions.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-white text-sm">Does the tool require an active internet connection?</h4>
                    <p className="text-gray-400 text-sm mt-1">
                      Only during checking for updates. All sorting, undo transactions, and custom configuration modifications are executed locally on your hard drive.
                    </p>
                  </div>
                </div>
              </section>

              {/* Troubleshooting */}
              <section id="troubleshooting" className="scroll-mt-24 pb-20">
                <h2 className="text-2xl font-extrabold text-white mb-4">Troubleshooting</h2>
                <div className="space-y-6 text-sm text-gray-400 leading-relaxed">
                  <div>
                    <h3 className="font-bold text-white text-base">PATH Variables</h3>
                    <p className="mt-1">
                      If PowerShell displays `folder-sorter: command not found` after a successful install, close and reopen your PowerShell window. The new PATH updates will only be loaded by terminal prompts on system initialization.
                    </p>
                  </div>

                  <div>
                    <h3 className="font-bold text-white text-base">Antivirus False Positives</h3>
                    <p className="mt-1">
                      PyInstaller wraps the Python executable inside a single binary which might trigger false flags on default Windows Defender scans. If this occurs, allowlist the directory `%LOCALAPPDATA%\FolderSorter\` in your security center.
                    </p>
                  </div>
                </div>
              </section>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
}
