import Link from "next/link";

export default function Footer() {
  return (
    <footer className="mt-auto border-t border-gray-800 bg-[#030712] py-8 text-gray-500">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="flex h-6 w-6 items-center justify-center rounded-md overflow-hidden bg-gradient-to-tr from-indigo-500 to-purple-600">
              <img src="/folder_sorter_icon.png" alt="Folder Sorter Logo" className="h-full w-full object-cover" />
            </div>
            <span className="font-semibold text-gray-400 text-sm">Folder Sorter</span>
          </div>

          {/* Links */}
          <div className="flex flex-wrap justify-center gap-x-8 gap-y-2 text-sm">
            <Link href="/install" className="hover:text-gray-300">
              Install Guide
            </Link>
            <Link href="/docs" className="hover:text-gray-300">
              Documentation
            </Link>
            <Link href="/roadmap" className="hover:text-gray-300">
              Roadmap
            </Link>
            <a
              href="https://github.com/Debanjan110d/Folder-Sorter"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 hover:text-gray-300"
            >
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
              <span>GitHub</span>
            </a>
          </div>

          {/* Creator & Copyright */}
          <div className="flex flex-col items-center gap-2 md:items-end text-sm">
            <div>
              Created by{" "}
              <a
                href="https://github.com/Debanjan110d"
                target="_blank"
                rel="noopener noreferrer"
                className="font-semibold text-gray-300 hover:text-white transition-colors"
              >
                Debanjan
              </a>
            </div>
            <div className="flex items-center gap-2">
              <a
                href="https://github.com/Debanjan110d"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 rounded bg-[#0d111d] hover:bg-gray-800 border border-gray-800 px-2 py-0.5 text-xs text-gray-300 transition-colors"
              >
                <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
                <span>Follow @Debanjan110d</span>
              </a>
              <span className="text-gray-700">|</span>
              <span className="text-xs text-gray-600">&copy; {new Date().getFullYear()} MIT License</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
