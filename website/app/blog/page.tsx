// ABOUTME: Blog listing page showing all articles
// ABOUTME: SEO-optimized with metadata and article previews

import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Calendar, Clock } from "lucide-react";
import { blogPosts } from "@/lib/blog-posts";

export const metadata = {
  title: "Blog - OpenDraft | AI Thesis Writing Guides & Tips",
  description: "Learn how to write academic theses with AI. Expert guides on thesis writing, AI agents, citations, and research automation. Free tutorials for students and researchers.",
  keywords: "thesis writing blog, AI thesis guide, academic writing tips, dissertation help, research paper tutorial",
};

export default function BlogPage() {
  return (
    <div className="container max-w-6xl mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          OpenDraft Blog
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Expert guides on AI-powered thesis writing, academic research automation, and citation management
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {blogPosts.map((post) => (
          <Link key={post.slug} href={`/blog/${post.slug}`}>
            <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <div className="flex items-center gap-2 mb-2">
                  <Badge>{post.category}</Badge>
                  <span className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Clock className="size-3" />
                    {post.readTime}
                  </span>
                </div>
                <CardTitle className="line-clamp-2">{post.title}</CardTitle>
                <CardDescription className="flex items-center gap-2 text-sm">
                  <Calendar className="size-3" />
                  {new Date(post.date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground line-clamp-3">
                  {post.description}
                </p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      {blogPosts.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted-foreground">More articles coming soon!</p>
        </div>
      )}
    </div>
  );
}
