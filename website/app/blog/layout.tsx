// ABOUTME: Blog layout with consistent styling and navigation
// ABOUTME: Wraps all blog posts with proper formatting and SEO structure

import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function BlogLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background">
      <div className="container max-w-4xl mx-auto px-4 py-12">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors mb-8"
        >
          <ArrowLeft className="size-4" />
          Back to Home
        </Link>

        <article className="prose prose-lg dark:prose-invert max-w-none">
          {children}
        </article>
      </div>
    </div>
  );
}
