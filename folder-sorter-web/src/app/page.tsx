"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";
import {
  FolderOpen,
  Copy,
  Check,
  Terminal,
  ShieldCheck,
  Undo2,
  Play,
  ArrowRight,
  Settings,
  Sparkles,
  HelpCircle,
  Clock
} from "lucide-react";

export default function Home() {
  const [copied, setCopied] = useState(false);
  const [terminalTab, setTerminalTab] = useState<"menu" | "sort" | "undo" | "doctor">("menu");
  const [downloads, setDownloads] = useState<number | null>(null);

  const copyCommand = () => {
    navigator.clipboard.writeText("irm https://folder-sorter.vercel.app/install.ps1 | iex");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  useEffect(() => {
    fetch("https://api.github.com/repos/Debanjan110d/Folder-Sorter/releases")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          let count = 0;
          data.forEach((release: any) => {
            if (release.assets && Array.isArray(release.assets)) {
              release.assets.forEach((asset: any) => {
                count += asset.download_count || 0;
              });
            }
          });
          setDownloads(count);
        }
      })
      .catch(() => {});
  }, []);

  return (
    <>
      <Navbar />

      <main className="flex-grow bg-[#030712] text-gray-100 selection:bg-indigo-500/30">
        {/* Hero Section */}
        <section className="relative overflow-hidden pt-20 pb-16 lg:pt-32 lg:pb-24">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(99,102,241,0.08),transparent_40%)]" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(168,85,247,0.05),transparent_40%)]" />

          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center relative z-10">
            {/* Version Badge */}
            <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/30 bg-indigo-500/5 px-3 py-1 text-xs font-semibold text-indigo-400 backdrop-blur-md mb-6 hover:bg-indigo-500/10 transition-colors">
              <Sparkles className="h-3 w-3" />
              <span>Version 1.0.3 Stable Windows Release</span>
              {downloads !== null && (
                <>
                  <span className="h-3 w-[1px] bg-indigo-500/30" />
                  <span className="text-gray-400 font-medium">{downloads} Installs</span>
                </>
              )}
            </div>

            {/* Title */}
            <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl lg:text-7xl">
              <span className="block text-white mb-2">Instantly Organize Messy</span>
              <span className="block bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent pb-1">
                Folders in Seconds
              </span>
            </h1>

            {/* Subtitle */}
            <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-400 sm:text-xl">
              A professional, lightning-fast CLI utility that categorizes, sorts, and structures your directories dynamically with safety-first undo operations.
            </p>

            {/* Quick Install command block */}
            <div className="mx-auto mt-10 max-w-xl">
              <div className="flex flex-col gap-2 rounded-lg border border-gray-800 bg-[#070b19] p-3 text-left shadow-2xl backdrop-blur-md">
                <div className="flex items-center justify-between px-2 text-xs font-medium text-gray-500">
                  <span>POWERSHELL INSTALLER</span>
                  <span className="text-indigo-400 font-semibold">Windows x64 Only</span>
                </div>
                <div className="flex items-center justify-between rounded-md bg-black/40 p-3 font-mono text-sm sm:text-base border border-gray-900/50">
                  <span className="text-gray-300 break-all select-all">
                    irm https://folder-sorter.vercel.app/install.ps1 | iex
                  </span>
                  <button
                    onClick={copyCommand}
                    className="ml-4 flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-gray-800 bg-[#0d111d] text-gray-400 transition-all hover:bg-gray-800 hover:text-white active:scale-95"
                    title="Copy command"
                  >
                    {copied ? <Check className="h-4 w-4 text-green-400" /> : <Copy className="h-4 w-4" />}
                  </button>
                </div>
              </div>
            </div>

            {/* CTAs */}
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <Link
                href="/install"
                className="flex items-center gap-2 rounded-lg bg-indigo-600 px-6 py-3 font-semibold text-white transition-all hover:bg-indigo-500 hover:shadow-lg hover:shadow-indigo-500/25 active:scale-98"
              >
                <span>Install Guide</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href="/docs"
                className="rounded-lg border border-gray-800 bg-[#0d111d]/80 px-6 py-3 font-semibold text-gray-300 transition-all hover:bg-gray-800 hover:text-white active:scale-98"
              >
                Read Documentation
              </Link>
            </div>
          </div>
        </section>

        {/* Visual CLI Interactive Mockup Section */}
        <section className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 pb-24">
          <div className="rounded-xl border border-gray-800 bg-[#050814] shadow-2xl overflow-hidden">
            {/* Terminal Top bar */}
            <div className="flex items-center justify-between border-b border-gray-900 bg-gray-950 px-4 py-3">
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded-full bg-red-500/80" />
                <span className="h-3 w-3 rounded-full bg-yellow-500/80" />
                <span className="h-3 w-3 rounded-full bg-green-500/80" />
                <span className="ml-2 font-mono text-xs text-gray-500">folder-sorter-terminal</span>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setTerminalTab("menu")}
                  className={`rounded px-2.5 py-1 font-mono text-xs transition-colors ${
                    terminalTab === "menu" ? "bg-indigo-600/30 text-indigo-400 border border-indigo-500/20" : "text-gray-500 hover:text-gray-300"
                  }`}
                >
                  interactive
                </button>
                <button
                  onClick={() => setTerminalTab("sort")}
                  className={`rounded px-2.5 py-1 font-mono text-xs transition-colors ${
                    terminalTab === "sort" ? "bg-indigo-600/30 text-indigo-400 border border-indigo-500/20" : "text-gray-500 hover:text-gray-300"
                  }`}
                >
                  sort
                </button>
                <button
                  onClick={() => setTerminalTab("undo")}
                  className={`rounded px-2.5 py-1 font-mono text-xs transition-colors ${
                    terminalTab === "undo" ? "bg-indigo-600/30 text-indigo-400 border border-indigo-500/20" : "text-gray-500 hover:text-gray-300"
                  }`}
                >
                  undo
                </button>
                <button
                  onClick={() => setTerminalTab("doctor")}
                  className={`rounded px-2.5 py-1 font-mono text-xs transition-colors ${
                    terminalTab === "doctor" ? "bg-indigo-600/30 text-indigo-400 border border-indigo-500/20" : "text-gray-500 hover:text-gray-300"
                  }`}
                >
                  doctor
                </button>
              </div>
            </div>

            {/* Terminal Window content */}
            <div className="p-6 font-mono text-sm leading-relaxed overflow-x-auto min-h-[340px] select-text">
              {terminalTab === "menu" && (
                <div>
                  <div className="text-gray-500">$ folder-sorter</div>
                  <div className="text-[#3b82f6] font-bold mt-2">┌────────────────────────────────────────────────────────┐</div>
                  <div className="text-[#3b82f6] font-bold">│                     <span className="text-[#06b6d4]">Folder Sorter CLI</span>                  │</div>
                  <div className="text-[#3b82f6] font-bold">│           <span className="text-[#22c55e]">Organize and manage messy folders with ease</span>          │</div>
                  <div className="text-[#3b82f6] font-bold">└────────────────────────────────────────────────────────┘</div>
                  <div className="text-[#d946ef] font-bold mt-3">Option  Action / Command     Description</div>
                  <div className="text-[#d946ef] font-bold">──────  ────────────────     ───────────</div>
                  <div>  <span className="text-[#06b6d4]">1</span>     Smart Sort           Organize files by type categories (Images, Code...)</div>
                  <div>  <span className="text-[#06b6d4]">2</span>     Sort By Month        Organize files chronologically by Year/Month</div>
                  <div>  <span className="text-[#06b6d4]">3</span>     Undo Last Sort       Restore files moved during the last sorting run</div>
                  <div>  <span className="text-[#06b6d4]">4</span>     Doctor Check         Check environment health, permissions & deps</div>
                  <div>  <span className="text-[#06b6d4]">5</span>     Configure Mappings   View or customize file extension category mappings</div>
                  <div>  <span className="text-[#06b6d4]">6</span>     CLI Reference        Show direct non-interactive terminal commands</div>
                  <div>  <span className="text-[#06b6d4]">0</span>     Exit Program         Close the folder-sorter tool</div>
                  <div className="text-yellow-400 font-semibold mt-4">Choose option [0-6] (default: 1): </div>
                </div>
              )}

              {terminalTab === "sort" && (
                <div>
                  <div className="text-gray-500">$ folder-sorter sort . --mode by-type --recursive</div>
                  <div className="text-cyan-400 mt-2">Scanning target folder: D:\Downloads</div>
                  <div className="text-cyan-400">Loading custom category mapping rules...</div>
                  <div className="text-white mt-2">📁 Found 24 files to categorize. Starting sort...</div>
                  <div className="text-[#22c55e] mt-1">✓ Moved: 'invoice_1204.pdf' ➔ 'Documents/invoice_1204.pdf'</div>
                  <div className="text-[#22c55e]">✓ Moved: 'vacation_photo.png' ➔ 'Images/vacation_photo.png' (1080p PNG)</div>
                  <div className="text-[#22c55e]">✓ Moved: 'setup.exe' ➔ 'Applications/setup.exe'</div>
                  <div className="text-[#22c55e]">✓ Moved: 'src/main.py' ➔ 'Code/main.py'</div>
                  <div className="text-[#22c55e]">✓ Moved: 'archive.zip' ➔ 'Archives/archive.zip'</div>
                  <div className="text-indigo-400 font-bold mt-3">Sorting session completed!</div>
                  <div className="text-gray-400">Total operations: 24 files successfully organized.</div>
                  <div className="text-gray-500">Run 'folder-sorter undo' to revert these changes.</div>
                </div>
              )}

              {terminalTab === "undo" && (
                <div>
                  <div className="text-gray-500">$ folder-sorter undo</div>
                  <div className="text-yellow-400 mt-2">⚠️ Reversing the last sort operation (Run ID: f184a)...</div>
                  <div className="text-white">Reading sorting history from local SQLite database...</div>
                  <div className="text-[#22c55e] mt-2">✓ Restored: 'Documents/invoice_1204.pdf' ➔ './invoice_1204.pdf'</div>
                  <div className="text-[#22c55e]">✓ Restored: 'Images/vacation_photo.png' ➔ './vacation_photo.png'</div>
                  <div className="text-[#22c55e]">✓ Restored: 'Applications/setup.exe' ➔ './setup.exe'</div>
                  <div className="text-[#22c55e]">✓ Restored: 'Code/main.py' ➔ 'src/main.py'</div>
                  <div className="text-[#22c55e]">✓ Restored: 'Archives/archive.zip' ➔ './archive.zip'</div>
                  <div className="text-[#22c55e] font-bold mt-3">✓ Reversion completed! All 24 files restored to original locations.</div>
                </div>
              )}

              {terminalTab === "doctor" && (
                <div>
                  <div className="text-gray-500">$ folder-sorter doctor</div>
                  <div className="text-[#22c55e] border border-[#22c55e]/30 bg-[#22c55e]/5 rounded p-3 font-semibold text-center mb-4">
                    [bold green]Folder Sorter - Diagnostic Doctor[/bold green]
                    <br />
                    <span className="text-xs font-normal opacity-85">Checking environment health and configurations...</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 border-b border-gray-900 pb-1 text-xs text-gray-500">
                    <span>Component Check</span>
                    <span>Details</span>
                    <span className="text-right">Status</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 py-1 text-xs">
                    <span className="font-semibold text-white">Python Runtime</span>
                    <span className="text-gray-400">Python 3.11.2 (Windows)</span>
                    <span className="text-right text-[#22c55e] font-bold">PASS</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 py-1 text-xs">
                    <span className="font-semibold text-white">App Config Directory</span>
                    <span className="text-gray-400 text-xs truncate">AppData/Local/FolderSorter</span>
                    <span className="text-right text-[#22c55e] font-bold">PASS</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 py-1 text-xs">
                    <span className="font-semibold text-white">Pillow Library</span>
                    <span className="text-gray-400">Pillow 10.1.0 (Supported)</span>
                    <span className="text-right text-[#22c55e] font-bold">PASS</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 py-1 text-xs">
                    <span className="font-semibold text-white">Database Log Check</span>
                    <span className="text-gray-400">History Database OK</span>
                    <span className="text-right text-[#22c55e] font-bold">PASS</span>
                  </div>
                  <div className="text-[#22c55e] font-bold mt-4">🎉 All checks passed! Folder Sorter is healthy and ready to go.</div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Feature Cards Grid */}
        <section className="bg-gradient-to-b from-[#030712] to-[#070b19] py-24">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
                Engineered for Safety and Control
              </h2>
              <p className="mx-auto mt-4 max-w-2xl text-gray-400">
                A simple execution that solves cluttered download folders, document dumps, and visual media archives.
              </p>
            </div>

            <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {/* Feature 1 */}
              <div className="group rounded-xl border border-gray-800 bg-[#0b1021] p-6 transition-all hover:border-indigo-500/50 hover:bg-[#0f162e]">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-indigo-500/10 text-indigo-400 transition-colors group-hover:bg-indigo-500/20">
                  <Terminal className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">Smart Type Sorting</h3>
                <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                  Categorize files into Images, Documents, Code, Archives, and Applications. Sub-sorts images by resolution (4K, 1080p, 720p) and format.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="group rounded-xl border border-gray-800 bg-[#0b1021] p-6 transition-all hover:border-purple-500/50 hover:bg-[#0f162e]">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-purple-500/10 text-purple-400 transition-colors group-hover:bg-purple-500/20">
                  <Undo2 className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">Sequential Undo Reversion</h3>
                <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                  Every run is logged into a local history database. Revert the last sort operation at any time to restore files exactly where they were.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="group rounded-xl border border-gray-800 bg-[#0b1021] p-6 transition-all hover:border-pink-500/50 hover:bg-[#0f162e]">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-pink-500/10 text-pink-400 transition-colors group-hover:bg-pink-500/20">
                  <ShieldCheck className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">Diagnostics Doctor</h3>
                <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                  Verify environment paths, database access, Pillow dependencies, and local workspace directory permissions immediately.
                </p>
              </div>

              {/* Feature 4 */}
              <div className="group rounded-xl border border-gray-800 bg-[#0b1021] p-6 transition-all hover:border-cyan-500/50 hover:bg-[#0f162e]">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-cyan-500/10 text-cyan-400 transition-colors group-hover:bg-cyan-500/20">
                  <Settings className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">Dynamic Configurations</h3>
                <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                  Customize global extension mappings directly through simple CLI mapping commands, saved under a global `config.json` file.
                </p>
              </div>

              {/* Feature 5 */}
              <div className="group rounded-xl border border-gray-800 bg-[#0b1021] p-6 transition-all hover:border-yellow-500/50 hover:bg-[#0f162e]">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-yellow-500/10 text-yellow-400 transition-colors group-hover:bg-yellow-500/20">
                  <Play className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">Dry Run Mode</h3>
                <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                  Preview operations before committing. View exact source-target directories on terminal console output logs without moving files.
                </p>
              </div>

              {/* Feature 6 */}
              <div className="group rounded-xl border border-gray-800 bg-[#0b1021] p-6 transition-all hover:border-emerald-500/50 hover:bg-[#0f162e]">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400 transition-colors group-hover:bg-emerald-500/20">
                  <Clock className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-white">Chronological Sorting</h3>
                <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                  Select date mode to sort files into nested folders grouped by Year and Month, ideal for camera rolls and screenshot folders.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Explain what the installer does */}
        <section className="bg-[#030712] py-20 border-t border-gray-900">
          <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-extrabold text-white text-center mb-12">
              Windows Installation Walkthrough
            </h2>
            <div className="relative border-l border-gray-800 pl-8 ml-4 space-y-10">
              <div className="relative">
                <div className="absolute -left-12 top-0 flex h-8 w-8 items-center justify-center rounded-full bg-indigo-500 text-white font-semibold text-sm">
                  1
                </div>
                <h3 className="text-lg font-semibold text-white">Query Release Version</h3>
                <p className="text-gray-400 text-sm mt-1">
                  The installer scripts fetch the latest release tag from the official GitHub Release API, ensuring you download the most up-to-date stable build.
                </p>
              </div>
              <div className="relative">
                <div className="absolute -left-12 top-0 flex h-8 w-8 items-center justify-center rounded-full bg-indigo-500 text-white font-semibold text-sm">
                  2
                </div>
                <h3 className="text-lg font-semibold text-white">Binary Package Download</h3>
                <p className="text-gray-400 text-sm mt-1">
                  Downloads the pre-compiled executable package `folder-sorter-windows.zip` directly from GitHub Releases.
                </p>
              </div>
              <div className="relative">
                <div className="absolute -left-12 top-0 flex h-8 w-8 items-center justify-center rounded-full bg-indigo-500 text-white font-semibold text-sm">
                  3
                </div>
                <h3 className="text-lg font-semibold text-white">Extract & Install</h3>
                <p className="text-gray-400 text-sm mt-1">
                  Extracts `folder-sorter.exe` and moves it safely to your local user directory: `%LOCALAPPDATA%\FolderSorter\`.
                </p>
              </div>
              <div className="relative">
                <div className="absolute -left-12 top-0 flex h-8 w-8 items-center justify-center rounded-full bg-indigo-500 text-white font-semibold text-sm">
                  4
                </div>
                <h3 className="text-lg font-semibold text-white">Environment PATH Configuration</h3>
                <p className="text-gray-400 text-sm mt-1">
                  Checks and adds the folder to your user Environment variables, enabling the `folder-sorter` command from any terminal prompt.
                </p>
              </div>
              <div className="relative">
                <div className="absolute -left-12 top-0 flex h-8 w-8 items-center justify-center rounded-full bg-indigo-500 text-white font-semibold text-sm">
                  5
                </div>
                <h3 className="text-lg font-semibold text-white">Diagnostics & Completion</h3>
                <p className="text-gray-400 text-sm mt-1">
                  Registers autocomplete options, executes the self-diagnostics checks via doctor command, and displays a summary of the healthy installation.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
}
