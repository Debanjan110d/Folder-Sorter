"use client";

import { useState } from "react";
import Link from "next/link";
import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";
import { Copy, Check, Terminal, ShieldAlert, CheckCircle, Info } from "lucide-react";

export default function InstallPage() {
  const [copiedWin, setCopiedWin] = useState(false);
  const [copiedPip, setCopiedPip] = useState(false);
  const [activeTab, setActiveTab] = useState<"win" | "mac" | "pip">("win");

  const copyWinCommand = () => {
    navigator.clipboard.writeText("irm https://folder-sorter.vercel.app/install.ps1 | iex");
    setCopiedWin(true);
    setTimeout(() => setCopiedWin(false), 2000);
  };

  const copyPipCommand = () => {
    navigator.clipboard.writeText("pip install -e .");
    setCopiedPip(true);
    setTimeout(() => setCopiedPip(false), 2000);
  };

  return (
    <>
      <Navbar />

      <main className="flex-grow bg-[#030712] text-gray-100 py-12 lg:py-20 selection:bg-indigo-500/30">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h1 className="text-3xl font-extrabold tracking-tight sm:text-5xl text-white">
              Installation Guide
            </h1>
            <p className="mt-4 text-gray-400">
              Get Folder Sorter up and running on your system with a single execution or compile directly from source code.
            </p>
          </div>

          {/* Installation Option Tabs */}
          <div className="flex border-b border-gray-800 mb-8">
            <button
              onClick={() => setActiveTab("win")}
              className={`pb-4 px-6 text-sm font-semibold transition-all border-b-2 ${
                activeTab === "win"
                  ? "border-indigo-500 text-white font-bold"
                  : "border-transparent text-gray-500 hover:text-gray-300"
              }`}
            >
              Windows (PowerShell)
            </button>
            <button
              onClick={() => setActiveTab("mac")}
              className={`pb-4 px-6 text-sm font-semibold transition-all border-b-2 ${
                activeTab === "mac"
                  ? "border-indigo-500 text-white font-bold"
                  : "border-transparent text-gray-500 hover:text-gray-300"
              }`}
            >
              macOS / Linux (Bash)
            </button>
            <button
              onClick={() => setActiveTab("pip")}
              className={`pb-4 px-6 text-sm font-semibold transition-all border-b-2 ${
                activeTab === "pip"
                  ? "border-indigo-500 text-white font-bold"
                  : "border-transparent text-gray-500 hover:text-gray-300"
              }`}
            >
              Development (Pip)
            </button>
          </div>

          {/* Tab Contents */}
          <div className="bg-[#070b19] border border-gray-800 rounded-xl p-6 shadow-2xl backdrop-blur-md">
            {activeTab === "win" && (
              <div>
                <h2 className="text-xl font-bold text-white mb-2">PowerShell One-Command Installation</h2>
                <p className="text-gray-400 text-sm mb-6 leading-relaxed">
                  Recommended for standard users. Downloads the pre-compiled binary directly from the latest GitHub Release and installs it into local application folder, making it available globally from terminal prompts. No development tools needed.
                </p>

                <div className="flex flex-col gap-2 rounded-lg border border-gray-900 bg-black/40 p-4 font-mono text-sm sm:text-base mb-6">
                  <div className="flex items-center justify-between text-xs text-gray-500 font-semibold mb-1">
                    <span>POWERSHELL CORE COMMAND</span>
                    <span className="text-green-500">✅ PRODUCTION READY</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-200 select-all break-all">
                      irm https://folder-sorter.vercel.app/install.ps1 | iex
                    </span>
                    <button
                      onClick={copyWinCommand}
                      className="ml-4 flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-gray-800 bg-[#0d111d] text-gray-400 transition-all hover:bg-gray-800 hover:text-white active:scale-95"
                    >
                      {copiedWin ? <Check className="h-4 w-4 text-green-400" /> : <Copy className="h-4 w-4" />}
                    </button>
                  </div>
                </div>

                <div className="border-t border-gray-900 pt-6 mt-6">
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4">What does this script do?</h3>
                  <ul className="space-y-3 text-sm text-gray-400">
                    <li className="flex gap-2.5">
                      <span className="text-indigo-400 font-bold">1.</span>
                      <span>Fetches latest release version tag from GitHub API.</span>
                    </li>
                    <li className="flex gap-2.5">
                      <span className="text-indigo-400 font-bold">2.</span>
                      <span>Downloads compiled Windows binary `folder-sorter-windows.zip`.</span>
                    </li>
                    <li className="flex gap-2.5">
                      <span className="text-indigo-400 font-bold">3.</span>
                      <span>Extracts and relocates the executable directly inside `%LOCALAPPDATA%\FolderSorter\`.</span>
                    </li>
                    <li className="flex gap-2.5">
                      <span className="text-indigo-400 font-bold">4.</span>
                      <span>Adds directory to the User PATH environment variable.</span>
                    </li>
                    <li className="flex gap-2.5">
                      <span className="text-indigo-400 font-bold">5.</span>
                      <span>Runs `folder-sorter doctor` validation checklist.</span>
                    </li>
                  </ul>
                </div>
              </div>
            )}

            {activeTab === "mac" && (
              <div>
                <h2 className="text-xl font-bold text-white mb-2">macOS / Linux Installer (Bash)</h2>
                <div className="flex items-center gap-2 border border-yellow-500/20 bg-yellow-500/5 rounded-lg p-3 text-xs text-yellow-500 font-medium mb-6">
                  <Info className="h-4 w-4 shrink-0" />
                  <span>Linux and macOS prebuilt binaries are postponed until future releases. Standard source code installation is recommended for non-Windows platforms.</span>
                </div>

                <p className="text-gray-400 text-sm mb-6 leading-relaxed">
                  Once macOS and Linux releases are stable, they will be installed globally with the following command:
                </p>

                <div className="flex flex-col gap-2 rounded-lg border border-gray-900 bg-black/40 p-4 font-mono text-sm sm:text-base opacity-60">
                  <div className="flex items-center justify-between text-xs text-gray-500 font-semibold mb-1">
                    <span>BASH SCRIPT COMMAND</span>
                    <span className="text-yellow-500">🚧 PLANNED FOR FUTURE</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 select-all break-all">
                      curl -fsSL https://folder-sorter.vercel.app/install.sh | bash
                    </span>
                    <button
                      disabled
                      className="ml-4 flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-gray-800 bg-[#0d111d]/50 text-gray-600"
                    >
                      <Copy className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "pip" && (
              <div>
                <h2 className="text-xl font-bold text-white mb-2">Python Pip Developer Mode Installation</h2>
                <p className="text-gray-400 text-sm mb-6 leading-relaxed">
                  Recommended for developers who want to run the python script directly or customize folder grouping patterns. Requires Python `&gt;= 3.8` and Git.
                </p>

                <div className="space-y-6">
                  <div>
                    <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Step 1: Clone the GitHub Repository</h3>
                    <pre className="rounded bg-black/40 p-3 text-xs text-gray-300 border border-gray-900">
                      git clone https://github.com/Debanjan110d/Folder-Sorter.git
                      {"\n"}cd Folder-Sorter
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Step 2: Install Package in Editable Mode</h3>
                    <div className="flex items-center justify-between rounded bg-black/40 p-3 text-xs text-gray-300 border border-gray-900 font-mono">
                      <span>pip install -e .</span>
                      <button
                        onClick={copyPipCommand}
                        className="ml-4 flex h-8 w-8 shrink-0 items-center justify-center rounded border border-gray-800 bg-[#0d111d] text-gray-400 transition-all hover:bg-gray-800 hover:text-white active:scale-95"
                      >
                        {copiedPip ? <Check className="h-3 w-3 text-green-400" /> : <Copy className="h-3 w-3" />}
                      </button>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Step 3: Run Self-Diagnostics Doctor</h3>
                    <pre className="rounded bg-black/40 p-3 text-xs text-gray-300 border border-gray-900">
                      folder-sorter doctor
                    </pre>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
}
