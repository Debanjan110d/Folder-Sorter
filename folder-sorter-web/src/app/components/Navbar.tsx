"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { FolderOpen, Menu, X } from "lucide-react";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [stars, setStars] = useState<number | null>(2);

  useEffect(() => {
    fetch("https://api.github.com/repos/Debanjan110d/Folder-Sorter")
      .then((res) => res.json())
      .then((data) => {
        if (data && typeof data.stargazers_count === "number") {
          setStars(data.stargazers_count);
        }
      })
      .catch(() => {});
  }, []);

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-800 bg-[#030712]/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2 font-bold text-white transition-opacity hover:opacity-90">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20">
                <FolderOpen className="h-5 w-5 text-white" />
              </div>
              <span className="bg-gradient-to-r from-white via-gray-100 to-gray-400 bg-clip-text text-xl tracking-tight text-transparent">
                Folder Sorter
              </span>
            </Link>
          </div>

          {/* Desktop Nav */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-8">
              <Link href="/install" className="text-sm font-medium text-gray-300 transition-colors hover:text-white">
                Install
              </Link>
              <Link href="/docs" className="text-sm font-medium text-gray-300 transition-colors hover:text-white">
                Docs
              </Link>
              <Link href="/roadmap" className="text-sm font-medium text-gray-300 transition-colors hover:text-white">
                Roadmap
              </Link>
              <span className="h-4 w-[1px] bg-gray-800" />
              <a
                href="https://github.com/Debanjan110d/Folder-Sorter"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm font-medium text-gray-400 transition-colors hover:text-white"
              >
                <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
                <span>GitHub</span>
                {stars !== null && (
                  <span className="flex items-center gap-0.5 rounded-full bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 text-[10px] font-bold text-amber-400">
                    ★ {stars}
                  </span>
                )}
              </a>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center rounded-md p-2 text-gray-400 transition-colors hover:bg-gray-800 hover:text-white"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="border-b border-gray-800 bg-[#030712] md:hidden">
          <div className="space-y-1 px-2 pt-2 pb-4 sm:px-3">
            <Link
              href="/install"
              onClick={() => setIsOpen(false)}
              className="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-800 hover:text-white"
            >
              Install
            </Link>
            <Link
              href="/docs"
              onClick={() => setIsOpen(false)}
              className="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-800 hover:text-white"
            >
              Docs
            </Link>
            <Link
              href="/roadmap"
              onClick={() => setIsOpen(false)}
              className="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-800 hover:text-white"
            >
              Roadmap
            </Link>
            <a
              href="https://github.com/Debanjan110d/Folder-Sorter"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-800 hover:text-white"
            >
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
              <span>GitHub</span>
              {stars !== null && (
                <span className="flex items-center gap-0.5 rounded-full bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 text-[10px] font-bold text-amber-400">
                  ★ {stars}
                </span>
              )}
            </a>
          </div>
        </div>
      )}
    </nav>
  );
}
